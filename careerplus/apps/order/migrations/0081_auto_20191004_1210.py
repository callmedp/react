# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-10-04 06:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0080_merge_20190905_1231'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitem',
            options={'ordering': ['-created'], 'permissions': (('can_show_midout_queue', 'Can Show Midout Queue'), ('can_upload_candidate_resume', 'Can Upload Candidate resume'), ('can_show_inbox_queue', 'Can Show Writer Inbox Queue'), ('can_view_extra_field_inbox', 'Can View Extra Fields Of Writer Inbox'), ('writer_inbox_assigner', 'Writer Inbox Assigner'), ('writer_inbox_assignee', 'Writer Inbox Assignee'), ('can_view_order_item_detail', 'Can View Order Item Detail'), ('writer_assignment_linkedin_action', 'Can Assign to Other linkedin writer'), ('can_assigned_to_linkedin_writer', 'Can Assigned To This linkedin Writer'), ('can_show_linkedinrejectedbyadmin_queue', 'Can View Linkedin Rejected By Admin Queue'), ('can_show_linkedinrejectedbycandidate_queue', 'Can View LinkedinRejected By Candidate Queue'), ('can_show_linkedin_approval_queue', 'Can View Linkedin Approval Queue'), ('can_show_linkedin_approved_queue', 'Can View Linkedin Approved Queue'), ('can_show_linkedin_inbox_queue', 'Can View Linkedin Inbox Queue'), ('can_show_linkedin_writer_draft', 'Can View Linkedin Writer Draft'), ('can_show_linkedin_counselling_form', 'Can View Linkedin Counselling Form'), ('can_view_counselling_form_in_approval_queue', 'Can View Counselling Form In Approval Queue'), ('can_show_approval_queue', 'Can View Approval Queue'), ('can_view_all_approval_list', 'Can View All Approval List'), ('can_view_only_assigned_approval_list', 'Can View Only Assigned Approval List'), ('can_approve_or_reject_draft', 'Can Approve Or Reject Draft'), ('can_show_approved_queue', 'Can View Approved Queue'), ('can_view_all_approved_list', 'Can View All Approved List'), ('can_view_only_assigned_approved_list', 'Can View Only Assigned Approved List'), ('can_show_rejectedbyadmin_queue', 'Can View Rejected By Admin Queue'), ('can_view_all_rejectedbyadmin_list', 'Can View All Rejected by Admin List'), ('can_view_only_assigned_rejectedbyadmin_list', 'Can View Only Assigned Rejected By Admin List'), ('can_show_rejectedbycandidate_queue', 'Can View Rejected By Candidate Queue'), ('can_view_all_rejectedbycandidate_list', 'Can View All Rejected By Candidate List'), ('can_view_only_assigned_rejectedbycandidate_list', 'Can View Only Assigned Rejected By Candidate List'), ('can_show_allocated_queue', 'Can Show Allocated Queue'), ('can_view_all_allocated_list', 'Can View All Allocated List'), ('can_view_only_assigned_allocated_list', 'Can View Only Assigned Allocated List'), ('can_show_booster_queue', 'Can Show Booster Queue'), ('can_show_domestic_profile_update_queue', 'Can Show Domestic Profile Update Queue'), ('domestic_profile_update_assigner', 'Domestic Profile Update Assigner'), ('domestic_profile_update_assignee', 'Domestic Profile Update Assignee'), ('can_show_domestic_profile_initiated_queue', 'Can Show Domestic Profile Initiated Queue'), ('can_show_domestic_profile_approval_queue', 'Can Show Domestic Profile Approval Queue'), ('can_show_international_profile_update_queue', 'Can Show International Profile Update Queue'), ('international_profile_update_assigner', 'International Profile Update Assigner'), ('international_profile_update_assignee', 'International Profile Update Assignee'), ('can_show_international_profile_approval_queue', 'Can Show International Profile Approval Queue'), ('can_show_closed_oi_queue', 'Can Show Closed Orderitem Queue'), ('can_view_all_closed_oi_list', 'Can View All Closed Orderitem List'), ('can_view_only_assigned_closed_oi_list', 'Can View Only Assigned Closed Orderitem List'), ('can_show_partner_inbox_queue', 'Can Show Partner Inbox Queue'), ('show_test_status_fields', 'Show Test Status Field For Studymate'), ('can_show_hold_orderitem_queue', 'Can Show Hold Orderitem Queue'), ('can_show_varification_report_queue', 'Can Show Varification Report Queue'), ('oi_action_permission', 'OrderItem Action Permission'), ('oi_export_as_csv_permission', 'Order Item Export As CSV Permission'), ('can_generate_compliance_report', 'can create compliance report permmission'), ('can_view_assigned_jobs_on_the_move', 'Can view assigned jobs on the move'), ('can_assign_jobs_on_the_move', 'Can assign jobs on the move'), ('can_send_jobs_on_the_move', 'Can send assigned jobs on the move'), ('can_approve_jobs_on_the_move', 'Can Approve jobs on the move'), ('can_update_manual_links', 'Can Update Manual Links')), 'verbose_name': 'Order Item', 'verbose_name_plural': 'Order Items'},
        ),
    ]
