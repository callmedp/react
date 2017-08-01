import logging

from django.utils import timezone

from emailers.email import SendMail
from emailers.sms import SendSMS


class ActionUserMixin(object):

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
