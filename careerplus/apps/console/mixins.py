import logging

from django.utils import timezone

from emailers.email import SendMail
from emailers.tasks import send_email_task
from emailers.sms import SendSMS
from order.models import OrderItem


class ActionUserMixin(object):

    def assign_single_orderitem(self, orderitem_list=[], assigned_to=None, user=None, data={}):
        orderitem_objs = OrderItem.objects.filter(id__in=orderitem_list).select_related('order')
        for obj in orderitem_objs:
            obj.assigned_to = assigned_to
            obj.assigned_by = user
            obj.save()

            # mail to user about writer information
            to_emails = [obj.order.email]
            email_data = {}
            email_data.update({
                "username": obj.order.first_name if obj.order.first_name else obj.order.candidate_id,
                "writer_name": assigned_to.name,
                "writer_email": assigned_to.email,
                "subject": "Your developed document has been shared with our expert",
                "oi": obj,

            })
            mail_type = 'ALLOCATED_TO_WRITER'
            
            try:
                SendMail().send(to_emails, mail_type, email_data)
            except Exception as e:
                logging.getLogger('email_log').error("%s - %s - %s" % (str(to_emails), str(mail_type), str(e)))

            if obj.delivery_service.name == 'SuperExpress':
                try:
                    SendSMS().send(sms_type=mail_type, data=email_data)
                except Exception as e:
                    logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

            obj.orderitemoperation_set.create(
                oi_status=1,
                last_oi_status=obj.oi_status,
                assigned_to=obj.assigned_to,
                added_by=user
            )

    def assign_orderitem(self, orderitem_list=[], assigned_to=None, user=None, data={}):
        orderitem_objs = OrderItem.objects.filter(id__in=orderitem_list).select_related('order')
        for obj in orderitem_objs:
            if not obj.assigned_to:
                obj.assigned_to = assigned_to
                obj.assigned_by = user
                obj.save()

                obj.orderitemoperation_set.create(
                    oi_status=1,
                    last_oi_status=obj.oi_status,
                    assigned_to=obj.assigned_to,
                    added_by=user
                )

                # mail to user about writer information
                to_emails = [obj.order.email]
                email_sets = list(obj.emailorderitemoperation_set.all().values_list('email_oi_status',flat=True).distinct())
                mail_type = 'ALLOCATED_TO_WRITER'
                email_data = {}
                email_data.update({
                    "username": obj.order.first_name if obj.order.first_name else obj.order.candidate_id,
                    "writer_name": assigned_to.name,
                    "writer_email": assigned_to.email,
                    "subject": "Your developed document has been shared with our expert",
                    "oi": obj,
                })
                self.product_flow_wise_mail(orderitem_obj=obj, to_emails=to_emails, mail_type=mail_type, data=email_data)
                try:
                    SendSMS().send(sms_type=mail_type, data=email_data)
                except Exception as e:
                    logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                # sms to writer in case of express and super express delivery

                addons = []
                variations = []
                combos = []

                if not obj.parent and obj.product.type_flow in [1, 12, 13]:
                    addons = obj.order.orderitems.filter(
                        parent=obj,
                        product__type_flow__in=[1, 12, 13], is_addon=True)
                    variations = obj.order.orderitems.filter(
                        parent=obj.parent, is_variation=True)

                elif obj.is_addon and obj.parent.product.type_flow in [1, 12, 13]:
                    addons = obj.order.orderitems.filter(
                        parent=obj.parent,
                        product__type_flow__in=[1, 12, 13], is_addon=True)
                    if not obj.parent.no_process:
                        addons = addons | obj.order.orderitems.filter(pk=obj.parent.pk)

                    variations = obj.order.orderitems.filter(
                        parent=obj.parent, is_variation=True)

                    combos = obj.order.orderitems.filter(
                        parent=obj.parent,
                        product__type_flow__in=[1, 12, 13],
                        is_combo=True)

                elif obj.is_variation:
                    variations = obj.order.orderitems.filter(
                        parent=obj.parent, is_variation=True)
                    addons = obj.order.orderitems.filter(
                        parent=obj.parent,
                        product__type_flow__in=[1, 12, 13],
                        is_addon=True)

                elif obj.is_combo and obj.product.type_flow in [1, 12, 13]:
                    addons = obj.order.orderitems.filter(
                        parent=obj.parent,
                        product__type_flow__in=[1, 12, 13],
                        is_addon=True)

                for oi in addons:
                    if not oi.assigned_to:
                        oi.assigned_to = assigned_to
                        oi.assigned_by = user
                        oi.save()

                        oi.orderitemoperation_set.create(
                            oi_status=1,
                            last_oi_status=obj.oi_status,
                            assigned_to=obj.assigned_to,
                            added_by=user
                        )

                        # mail to user about writer information
                        to_emails = [oi.order.email]
                        mail_type = 'ALLOCATED_TO_WRITER'
                        email_data = {}
                        email_data.update({
                            "username": oi.order.first_name if oi.order.first_name else oi.order.candidate_id,
                            "writer_name": assigned_to.name,
                            "writer_email": assigned_to.email,
                            "subject": "Your developed document has been shared with our expert",
                            "oi": oi,
                        })
                        self.product_flow_wise_mail(orderitem_obj=oi, to_emails=to_emails, mail_type=mail_type, data=email_data)
                        if oi.delivery_service.name == 'SuperExpress':
                            try:
                                SendSMS().send(sms_type=mail_type, data=email_data)
                            except Exception as e:
                                logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                        # sms to writer in case of express and super express delivery

                for oi in variations:
                    if not oi.assigned_to:
                        oi.assigned_to = assigned_to
                        oi.assigned_by = user
                        oi.save()

                        oi.orderitemoperation_set.create(
                            oi_status=1,
                            last_oi_status=obj.oi_status,
                            assigned_to=obj.assigned_to,
                            added_by=user
                        )

                        # mail to user about writer information
                        to_emails = [oi.order.email]
                        mail_type = 'ALLOCATED_TO_WRITER'
                        email_data = {}
                        email_data.update({
                            "username": oi.order.first_name if oi.order.first_name else oi.order.candidate_id,
                            "writer_name": assigned_to.name,
                            "writer_email": assigned_to.email,
                            "subject": "Your developed document has been shared with our expert",
                            "oi": oi,
                        })
                        self.product_flow_wise_mail(orderitem_obj=oi, to_emails=to_emails, mail_type=mail_type, data=email_data)
                        if obj.delivery_service.name == 'SuperExpress':
                            try:
                                SendSMS().send(sms_type=mail_type, data=email_data)
                            except Exception as e:
                                logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                        # sms to writer in case of express and super express delivery

                for oi in combos:
                    if not oi.assigned_to:
                        oi.assigned_to = assigned_to
                        oi.assigned_by = user
                        oi.save()

                        oi.orderitemoperation_set.create(
                            oi_status=1,
                            last_oi_status=obj.oi_status,
                            assigned_to=obj.assigned_to,
                            added_by=user
                        )

                        # mail to user about writer information
                        to_emails = [oi.order.email]
                        mail_type = 'ALLOCATED_TO_WRITER'
                        email_data = {}
                        email_data.update({
                            "username": obj.order.first_name + ' ' + obj.order.last_name,
                            "writer_name": assigned_to.name,
                            "writer_email": assigned_to.email,
                            "subject": "Your developed document has been shared with our expert",
                            "oi": oi,
                        })
                        self.product_flow_wise_mail(orderitem_obj=oi, to_emails=to_emails, mail_type=mail_type, data=email_data)
                        if obj.delivery_service.name == 'SuperExpress':
                            try:
                                SendSMS().send(sms_type=mail_type, data=email_data)
                            except Exception as e:
                                logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                        # sms to writer in case of express and super express delivery

    def upload_candidate_resume(self, oi=None, data={}, user=None):
        oi_resume = data.get('candidate_resume', '')
        if oi and oi_resume:
            oi.oi_resume = oi_resume
            last_oi_status = oi.oi_status
            oi.oi_status = 5
            oi.last_oi_status = 3
            oi.save()
            oi.orderitemoperation_set.create(
                oi_status=3,
                oi_resume=oi.oi_resume,
                last_oi_status=last_oi_status,
                assigned_to=oi.assigned_to,
                added_by=user)

            oi.orderitemoperation_set.create(
                oi_status=oi.oi_status,
                last_oi_status=oi.last_oi_status,
                assigned_to=oi.assigned_to,
                added_by=user)

    def upload_draft_orderitem(self, oi=None, data={}, user=None):
        oi_draft = data.get('oi_draft', '')
        message_dict = {'display_message': "", }
        if oi and oi_draft and user and user.is_active:
            if oi.product.type_flow in [2, 10]:
                last_oi_status = oi.last_oi_status
                oi.oi_status = 4  # closed orderitem
                oi.oi_draft = oi_draft
                oi.draft_counter += 1
                oi.last_oi_status = 6
                oi.closed_on = timezone.now()
                oi.save()
                message_dict['display_message'] = 'Document uploaded and orderitem closed Successfully.'

                oi.orderitemoperation_set.create(
                    oi_draft=oi.oi_draft,
                    draft_counter=1,
                    oi_status=6,
                    last_oi_status=last_oi_status,
                    assigned_to=oi.assigned_to,
                    added_by=user)

                oi.orderitemoperation_set.create(
                    oi_status=oi.oi_status,
                    last_oi_status=oi.last_oi_status,
                    assigned_to=oi.assigned_to,
                    added_by=user)

                # mail and sms to candidate
                to_emails = [oi.order.email]
                email_dict = {}
                email_dict.update({

                    "info": 'Your service has been processed',
                    "subject": 'Your service has been processed',
                    "name": oi.order.first_name + ' ' + oi.order.last_name,
                    "mobile": oi.order.mobile,
                })

                mail_type = 'COURSE_CLOSER_MAIL'
                try:
                    SendMail().send(to_emails, mail_type, email_dict)
                except Exception as e:
                    logging.getLogger('email_log').error("%s - %s - %s" % (str(to_emails), str(e), str(mail_type)))

                try:
                    SendSMS().send(sms_type=mail_type, data=email_dict)
                except Exception as e:
                    logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

            elif oi.product.type_flow == 6:
                if oi.oi_status == 81:
                    last_oi_status = oi.last_oi_status
                    oi.oi_status = 4  # Closed oi
                    oi.oi_draft = oi_draft
                    oi.draft_counter += 1
                    oi.last_oi_status = 6
                    oi.closed_on = timezone.now()
                    oi.save()
                    message_dict['display_message'] = 'Reporting document uploaded and orderitem closed successfully.'

                    oi.orderitemoperation_set.create(
                        oi_draft=oi.oi_draft,
                        draft_counter=2,
                        oi_status=6,
                        last_oi_status=last_oi_status,
                        assigned_to=oi.assigned_to,
                        added_by=user)

                    oi.orderitemoperation_set.create(
                        oi_status=oi.oi_status,
                        last_oi_status=oi.last_oi_status,
                        assigned_to=oi.assigned_to,
                        added_by=user)
                else:
                    last_oi_status = oi.last_oi_status
                    oi.oi_status = 81  # Varification reports
                    oi.oi_draft = oi_draft
                    oi.draft_counter += 1
                    oi.last_oi_status = 22
                    oi.save()
                    message_dict['display_message'] = 'Document uploaded successfully.'

                    oi.orderitemoperation_set.create(
                        oi_draft=oi.oi_draft,
                        draft_counter=oi.draft_counter,
                        oi_status=oi.oi_status,
                        last_oi_status=oi.last_oi_status,
                        assigned_to=oi.assigned_to,
                        added_by=user)

            else:
                last_status = oi.oi_status
                oi.oi_draft = oi_draft
                oi.oi_status = 23  # pending Approval
                oi.last_oi_status = last_status
                oi.draft_added_on = timezone.now()
                oi.save()
                message_dict['display_message'] = 'Draft uploaded Successfully.'
                oi.orderitemoperation_set.create(
                    oi_draft=oi.oi_draft,
                    draft_counter=oi.draft_counter + 1,
                    oi_status=22,
                    last_oi_status=last_status,
                    assigned_to=oi.assigned_to,
                    added_by=user)
                oi.orderitemoperation_set.create(
                    oi_status=oi.oi_status,
                    last_oi_status=22,
                    assigned_to=oi.assigned_to,
                    added_by=user)
        else:
            message_dict['display_message'] = 'User is not active or draft or orderitem obj not found'
        return message_dict
    
    def product_flow_wise_mail(self, orderitem_obj=None, to_emails=[], mail_type=None, data={}):
        email_sets = list(orderitem_obj.emailorderitemoperation_set.all().values_list('email_oi_status',flat=True).distinct())
        if orderitem_obj.product.type_flow == 1 and 28 not in email_sets:             
            send_email_task.delay(to_emails, mail_type, data, status=28, oi=orderitem_obj.pk)

        elif orderitem_obj.product.type_flow == 12 and 141 not in email_sets:             
            send_email_task.delay(to_emails, mail_type, data, status=141, oi=orderitem_obj.pk)

        elif orderitem_obj.product.type_flow == 13 and 151 not in email_sets:             
            send_email_task.delay(to_emails, mail_type, data, status=151, oi=orderitem_obj.pk)

        elif orderitem_obj.product.type_flow == 8 and 101 not in email_sets:             
            send_email_task.delay(to_emails, mail_type, data, status=108, oi=orderitem_obj.pk)

        elif orderitem_obj.product.type_flow == 3 and 41 not in email_sets:             
            send_email_task.delay(to_emails, mail_type, data, status=41, oi=orderitem_obj.pk)

        elif orderitem_obj.product.type_flow == 4 and 61 not in email_sets:             
            send_email_task.delay(to_emails, mail_type, data, status=61, oi=orderitem_obj.pk)
        else:
            pass
