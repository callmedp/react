# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-03-06 06:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0052_merge_20180205_1552'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitem',
            options={'ordering': ['-created'], 'permissions': (('can_show_midout_queue', 'Can Show Midout Queue'), ('can_upload_candidate_resume', 'Can Upload Candidate resume'), ('can_show_inbox_queue', 'Can Show Writer Inbox Queue'), ('can_view_extra_field_inbox', 'Can View Extra Fields Of Writer Inbox'), ('writer_inbox_assigner', 'Writer Inbox Assigner'), ('writer_inbox_assignee', 'Writer Inbox Assignee'), ('can_view_order_item_detail', 'Can View Order Item Detail'), ('writer_assignment_linkedin_action', 'Can Assign to Other linkedin writer'), ('can_assigned_to_linkedin_writer', 'Can Assigned To This linkedin Writer'), ('can_show_linkedinrejectedbyadmin_queue', 'Can View Linkedin Rejected By Admin Queue'), ('can_show_linkedinrejectedbycandidate_queue', 'Can View LinkedinRejected By Candidate Queue'), ('can_show_linkedin_approval_queue', 'Can View Linkedin Approval Queue'), ('can_show_linkedin_approved_queue', 'Can View Linkedin Approved Queue'), ('can_show_linkedin_inbox_queue', 'Can View Linkedin Inbox Queue'), ('can_show_linkedin_writer_draft', 'Can View Linkedin Writer Draft'), ('can_show_linkedin_counselling_form', 'Can View Linkedin Counselling Form'), ('can_view_counselling_form_in_approval_queue', 'Can View Counselling Form In Approval Queue'), ('can_show_approval_queue', 'Can View Approval Queue'), ('can_view_all_approval_list', 'Can View All Approval List'), ('can_view_only_assigned_approval_list', 'Can View Only Assigned Approval List'), ('can_approve_or_reject_draft', 'Can Approve Or Reject Draft'), ('can_show_approved_queue', 'Can View Approved Queue'), ('can_view_all_approved_list', 'Can View All Approved List'), ('can_view_only_assigned_approved_list', 'Can View Only Assigned Approved List'), ('can_show_rejectedbyadmin_queue', 'Can View Rejected By Admin Queue'), ('can_view_all_rejectedbyadmin_list', 'Can View All Rejected by Admin List'), ('can_view_only_assigned_rejectedbyadmin_list', 'Can View Only Assigned Rejected By Admin List'), ('can_show_rejectedbycandidate_queue', 'Can View Rejected By Candidate Queue'), ('can_view_all_rejectedbycandidate_list', 'Can View All Rejected By Candidate List'), ('can_view_only_assigned_rejectedbycandidate_list', 'Can View Only Assigned Rejected By Candidate List'), ('can_show_allocated_queue', 'Can Show Allocated Queue'), ('can_view_all_allocated_list', 'Can View All Allocated List'), ('can_view_only_assigned_allocated_list', 'Can View Only Assigned Allocated List'), ('can_show_booster_queue', 'Can Show Booster Queue'), ('can_show_domestic_profile_update_queue', 'Can Show Domestic Profile Update Queue'), ('domestic_profile_update_assigner', 'Domestic Profile Update Assigner'), ('domestic_profile_update_assignee', 'Domestic Profile Update Assignee'), ('can_show_domestic_profile_approval_queue', 'Can Show Domestic Profile Approval Queue'), ('can_show_international_profile_update_queue', 'Can Show International Profile Update Queue'), ('international_profile_update_assigner', 'International Profile Update Assigner'), ('international_profile_update_assignee', 'International Profile Update Assignee'), ('can_show_international_profile_approval_queue', 'Can Show International Profile Approval Queue'), ('can_show_closed_oi_queue', 'Can Show Closed Orderitem Queue'), ('can_view_all_closed_oi_list', 'Can View All Closed Orderitem List'), ('can_view_only_assigned_closed_oi_list', 'Can View Only Assigned Closed Orderitem List'), ('can_show_partner_inbox_queue', 'Can Show Partner Inbox Queue'), ('show_test_status_fields', 'Show Test Status Field For Studymate'), ('can_show_hold_orderitem_queue', 'Can Show Hold Orderitem Queue'), ('can_show_varification_report_queue', 'Can Show Varification Report Queue'), ('oi_action_permission', 'OrderItem Action Permission'), ('oi_export_as_csv_permission', 'Order Item Export As CSV Permission')), 'verbose_name': 'Order Item', 'verbose_name_plural': 'Order Items'},
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='last_oi_status',
            field=models.PositiveIntegerField(choices=[(0, 'Default'), (1, 'Assigned'), (2, 'Resume upload is pending'), (3, 'Resume Uploaded'), (4, 'Closed'), (5, 'Service is under progress'), (6, 'Service has been processed'), (10, 'On Hold by Vendor'), (11, 'Archived'), (12, 'Unhold by Vendor'), (13, 'Shine Resume'), (21, 'Upload Draft'), (22, 'Draft Uploaded'), (23, 'Pending Approval'), (24, 'Approved'), (25, 'Rejected By Admin'), (26, 'Rejected By Candidate'), (27, 'Service has been processed and Document is finalized'), (28, 'Feature profile initiated'), (29, 'Feature profile expired'), (30, 'Feature profile updated'), (42, 'Counselling Form Submitted'), (44, 'Linkedin Draft Created'), (45, 'Linkedin Pending Approval'), (46, 'Linkedin Approved'), (47, 'Linkedin Rejected By Admin'), (48, 'Linkedi Rejected By Candidate'), (49, 'Couselling form is pending'), (61, 'Service will be initiated once resume is finalized'), (62, 'Resume Boosted'), (81, 'Pending Verification Reports'), (82, 'Service is initiated'), (101, 'To start learning , it is mandatory to take this test'), (121, 'Service has been processed and Final document is ready'), (141, 'Your profile to be shared with interviewer is pending'), (142, 'Round one is not expired'), (143, 'Round one is expired'), (161, 'Refund initiated'), (162, 'Refund under progress'), (163, 'Refunded'), (181, 'Waiting for input')], default=0, verbose_name='Last Operation Status'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='oi_status',
            field=models.PositiveIntegerField(choices=[(0, 'Default'), (1, 'Assigned'), (2, 'Resume upload is pending'), (3, 'Resume Uploaded'), (4, 'Closed'), (5, 'Service is under progress'), (6, 'Service has been processed'), (10, 'On Hold by Vendor'), (11, 'Archived'), (12, 'Unhold by Vendor'), (13, 'Shine Resume'), (21, 'Upload Draft'), (22, 'Draft Uploaded'), (23, 'Pending Approval'), (24, 'Approved'), (25, 'Rejected By Admin'), (26, 'Rejected By Candidate'), (27, 'Service has been processed and Document is finalized'), (28, 'Feature profile initiated'), (29, 'Feature profile expired'), (30, 'Feature profile updated'), (42, 'Counselling Form Submitted'), (44, 'Linkedin Draft Created'), (45, 'Linkedin Pending Approval'), (46, 'Linkedin Approved'), (47, 'Linkedin Rejected By Admin'), (48, 'Linkedi Rejected By Candidate'), (49, 'Couselling form is pending'), (61, 'Service will be initiated once resume is finalized'), (62, 'Resume Boosted'), (81, 'Pending Verification Reports'), (82, 'Service is initiated'), (101, 'To start learning , it is mandatory to take this test'), (121, 'Service has been processed and Final document is ready'), (141, 'Your profile to be shared with interviewer is pending'), (142, 'Round one is not expired'), (143, 'Round one is expired'), (161, 'Refund initiated'), (162, 'Refund under progress'), (163, 'Refunded'), (181, 'Waiting for input')], default=0, verbose_name='Operation Status'),
        ),
        migrations.AlterField(
            model_name='orderitemoperation',
            name='last_oi_status',
            field=models.PositiveIntegerField(choices=[(0, 'Default'), (1, 'Assigned'), (2, 'Resume upload is pending'), (3, 'Resume Uploaded'), (4, 'Closed'), (5, 'Service is under progress'), (6, 'Service has been processed'), (10, 'On Hold by Vendor'), (11, 'Archived'), (12, 'Unhold by Vendor'), (13, 'Shine Resume'), (21, 'Upload Draft'), (22, 'Draft Uploaded'), (23, 'Pending Approval'), (24, 'Approved'), (25, 'Rejected By Admin'), (26, 'Rejected By Candidate'), (27, 'Service has been processed and Document is finalized'), (28, 'Feature profile initiated'), (29, 'Feature profile expired'), (30, 'Feature profile updated'), (42, 'Counselling Form Submitted'), (44, 'Linkedin Draft Created'), (45, 'Linkedin Pending Approval'), (46, 'Linkedin Approved'), (47, 'Linkedin Rejected By Admin'), (48, 'Linkedi Rejected By Candidate'), (49, 'Couselling form is pending'), (61, 'Service will be initiated once resume is finalized'), (62, 'Resume Boosted'), (81, 'Pending Verification Reports'), (82, 'Service is initiated'), (101, 'To start learning , it is mandatory to take this test'), (121, 'Service has been processed and Final document is ready'), (141, 'Your profile to be shared with interviewer is pending'), (142, 'Round one is not expired'), (143, 'Round one is expired'), (161, 'Refund initiated'), (162, 'Refund under progress'), (163, 'Refunded'), (181, 'Waiting for input')], default=0, verbose_name='Last Operation Status'),
        ),
        migrations.AlterField(
            model_name='orderitemoperation',
            name='oi_status',
            field=models.PositiveIntegerField(choices=[(0, 'Default'), (1, 'Assigned'), (2, 'Resume upload is pending'), (3, 'Resume Uploaded'), (4, 'Closed'), (5, 'Service is under progress'), (6, 'Service has been processed'), (10, 'On Hold by Vendor'), (11, 'Archived'), (12, 'Unhold by Vendor'), (13, 'Shine Resume'), (21, 'Upload Draft'), (22, 'Draft Uploaded'), (23, 'Pending Approval'), (24, 'Approved'), (25, 'Rejected By Admin'), (26, 'Rejected By Candidate'), (27, 'Service has been processed and Document is finalized'), (28, 'Feature profile initiated'), (29, 'Feature profile expired'), (30, 'Feature profile updated'), (42, 'Counselling Form Submitted'), (44, 'Linkedin Draft Created'), (45, 'Linkedin Pending Approval'), (46, 'Linkedin Approved'), (47, 'Linkedin Rejected By Admin'), (48, 'Linkedi Rejected By Candidate'), (49, 'Couselling form is pending'), (61, 'Service will be initiated once resume is finalized'), (62, 'Resume Boosted'), (81, 'Pending Verification Reports'), (82, 'Service is initiated'), (101, 'To start learning , it is mandatory to take this test'), (121, 'Service has been processed and Final document is ready'), (141, 'Your profile to be shared with interviewer is pending'), (142, 'Round one is not expired'), (143, 'Round one is expired'), (161, 'Refund initiated'), (162, 'Refund under progress'), (163, 'Refunded'), (181, 'Waiting for input')], default=0, verbose_name='Operation Status'),
        ),
    ]
