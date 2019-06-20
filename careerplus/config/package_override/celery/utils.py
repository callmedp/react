#python imports
from __future__ import absolute_import, unicode_literals
import logging
from weakref import ref

#django imports

#local imports

#inter app imports

#third party imports
from kombu.five import buffer_t
from celery.worker import state
from celery.utils.time import timezone
from celery.utils.log import get_logger
from kombu.async.timer import to_timestamp
from celery.worker.request import Request
from celery.worker.state import task_reserved
from celery.worker.strategy import proto1_to_proto2
from celery.app.trace import trace_task, trace_task_ret
from celery.utils.functional import maybe, noop
from celery.exceptions import (
    Ignore, TaskRevokedError, InvalidTaskError,
    SoftTimeLimitExceeded, TimeLimitExceeded,
    WorkerLostError, Terminated, Retry, Reject,
)

task_ready = state.task_ready
revoked_tasks = state.revoked
logger = get_logger(__name__)
debug, info, warn, error = (logger.debug, logger.info,
                            logger.warning, logger.error)
_does_info = False
_does_debug = False

__all__ = ['default']

logger = get_logger(__name__)

def create_request_cls(base, task, pool, hostname, eventer,
                       ref=ref, revoked_tasks=revoked_tasks,
                       task_ready=task_ready, trace=trace_task_ret):
    default_time_limit = task.time_limit
    default_soft_time_limit = task.soft_time_limit
    apply_async = pool.apply_async
    acks_late = task.acks_late
    events = eventer and eventer.enabled

    class Request(base):

        def execute_using_pool(self, pool, **kwargs):
            task_id = self.id
            if (self.expires or task_id in revoked_tasks) and self.revoked():
                raise TaskRevokedError(task_id)

            time_limit, soft_time_limit = self.time_limits
            result = apply_async(
                trace,
                args=(self.type, task_id, self.request_dict, self.body,
                      self.content_type, self.content_encoding),
                accept_callback=self.on_accepted,
                timeout_callback=self.on_timeout,
                callback=self.on_success,
                error_callback=self.on_failure,
                soft_timeout=soft_time_limit or default_soft_time_limit,
                timeout=time_limit or default_time_limit,
                correlation_id=task_id,
            )
            # cannot create weakref to None
            # pylint: disable=attribute-defined-outside-init
            self._apply_result = maybe(ref, result)
            return result

        def on_success(self, failed__retval__runtime, **kwargs):
            failed, retval, runtime = failed__retval__runtime
            if failed:
                if isinstance(retval.exception, (
                        SystemExit, KeyboardInterrupt)):
                    raise retval.exception
                
                logging.getLogger('error_log').error(\
                    "Task {} failed. Reason : {}".format(task.name,retval.exception))

                return self.on_failure(retval, return_ok=True)
            task_ready(self)

            if acks_late:
                self.acknowledge()
            
            if events:
                self.send_event(
                    'task-succeeded', result=retval, runtime=runtime,
                )
            logging.getLogger('info_log').info("Task {} succeeded in {}".format(task.name,runtime))

    return Request


def default(task, app, consumer,
            info=logger.info, error=logger.error, task_reserved=task_reserved,
            to_system_tz=timezone.to_system, bytes=bytes, buffer_t=buffer_t,
            proto1_to_proto2=proto1_to_proto2):
    """Default task execution strategy.

    Note:
        Strategies are here as an optimization, so sadly
        it's not very easy to override.
    """
    hostname = consumer.hostname
    connection_errors = consumer.connection_errors
    _does_info = logger.isEnabledFor(logging.INFO)

    # task event related
    # (optimized to avoid calling request.send_event)
    eventer = consumer.event_dispatcher
    events = eventer and eventer.enabled
    send_event = eventer.send
    task_sends_events = events and task.send_events

    call_at = consumer.timer.call_at
    apply_eta_task = consumer.apply_eta_task
    rate_limits_enabled = not consumer.disable_rate_limits
    get_bucket = consumer.task_buckets.__getitem__
    handle = consumer.on_task_request
    limit_task = consumer._limit_task
    body_can_be_buffer = consumer.pool.body_can_be_buffer
    Req = create_request_cls(Request, task, consumer.pool, hostname, eventer)

    revoked_tasks = consumer.controller.state.revoked

    def task_message_handler(message, body, ack, reject, callbacks,
                             to_timestamp=to_timestamp):
        if body is None:
            body, headers, decoded, utc = (
                message.body, message.headers, False, app.uses_utc_timezone(),
            )
            if not body_can_be_buffer:
                body = bytes(body) if isinstance(body, buffer_t) else body
        else:
            body, headers, decoded, utc = proto1_to_proto2(message, body)

        req = Req(
            message,
            on_ack=ack, on_reject=reject, app=app, hostname=hostname,
            eventer=eventer, task=task, connection_errors=connection_errors,
            body=body, headers=headers, decoded=decoded, utc=utc,
        )
        
        logging.getLogger('info_log').info("Received task {}".format(req))

        if _does_info:
            info('Received task: %s', req)
        if (req.expires or req.id in revoked_tasks) and req.revoked():
            return

        if task_sends_events:
            send_event(
                'task-received',
                uuid=req.id, name=req.name,
                args=req.argsrepr, kwargs=req.kwargsrepr,
                root_id=req.root_id, parent_id=req.parent_id,
                retries=req.request_dict.get('retries', 0),
                eta=req.eta and req.eta.isoformat(),
                expires=req.expires and req.expires.isoformat(),
            )

        if req.eta:
            try:
                if req.utc:
                    eta = to_timestamp(to_system_tz(req.eta))
                else:
                    eta = to_timestamp(req.eta, app.timezone)
            except (OverflowError, ValueError) as exc:
                error("Couldn't convert ETA %r to timestamp: %r. Task: %r",
                      req.eta, exc, req.info(safe=True), exc_info=True)
                req.reject(requeue=False)
            else:
                consumer.qos.increment_eventually()
                call_at(eta, apply_eta_task, (req,), priority=6)
        else:
            if rate_limits_enabled:
                bucket = get_bucket(task.name)
                if bucket:
                    return limit_task(req, bucket, 1)
            task_reserved(req)
            if callbacks:
                [callback(req) for callback in callbacks]
            handle(req)

    return task_message_handler
