# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-08 09:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0023_auto_20170905_1245'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='refundrequest',
            options={'ordering': ('-modified',), 'permissions': (('can_view_refund_request_queue', 'Can View Refund Request Queue'),)},
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='delivery_price_excl_tax',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Delivery Price (site price)'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='delivery_price_incl_tax',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Delivery Price (incl. tax excl Discount)'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='last_oi_status',
            field=models.PositiveIntegerField(choices=[(0, 'Default'), (1, 'Assigned'), (2, 'Resume upload is pending'), (3, 'Resume Uploaded'), (4, 'Closed'), (5, 'Service is under progress'), (6, 'Service has been processed'), (10, 'On Hold by Vendor'), (11, 'Archived'), (12, 'Unhold by Vendor'), (13, 'Shine Resume'), (21, 'Upload Draft'), (22, 'Draft Uploaded'), (23, 'Pending Approval'), (24, 'Approved'), (25, 'Rejected By Admin'), (26, 'Rejected By Candidate'), (27, 'Service has been processed and Document is finalized'), (28, 'Feature profile initiated'), (29, 'Feature profile expired'), (30, 'Feature profile updated'), (43, 'Linkedin Draft Create'), (44, 'Linkedin Draft Created'), (45, 'Linkedin Pending Approval'), (46, 'Linkedin Approved'), (47, 'Linkedin Rejected By Admin'), (48, 'Linkedi Rejected By Candidate'), (49, 'Couselling form is pending'), (61, 'Service will be initiated once resume is finalized'), (62, 'Resume Boosted'), (81, 'Pending Varification Reports'), (82, 'Service is initiated'), (101, 'To start learning , it is mandatory to take this test'), (121, 'Service has been processed and Final document is ready'), (141, 'Your profile to be shared with interviewer is pending'), (142, 'Round one is not expired'), (143, 'Round one is expired'), (161, 'Refund initiated'), (162, 'Refund under progress'), (163, 'Refunded')], default=0, verbose_name='Last Operation Status'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='oi_status',
            field=models.PositiveIntegerField(choices=[(0, 'Default'), (1, 'Assigned'), (2, 'Resume upload is pending'), (3, 'Resume Uploaded'), (4, 'Closed'), (5, 'Service is under progress'), (6, 'Service has been processed'), (10, 'On Hold by Vendor'), (11, 'Archived'), (12, 'Unhold by Vendor'), (13, 'Shine Resume'), (21, 'Upload Draft'), (22, 'Draft Uploaded'), (23, 'Pending Approval'), (24, 'Approved'), (25, 'Rejected By Admin'), (26, 'Rejected By Candidate'), (27, 'Service has been processed and Document is finalized'), (28, 'Feature profile initiated'), (29, 'Feature profile expired'), (30, 'Feature profile updated'), (43, 'Linkedin Draft Create'), (44, 'Linkedin Draft Created'), (45, 'Linkedin Pending Approval'), (46, 'Linkedin Approved'), (47, 'Linkedin Rejected By Admin'), (48, 'Linkedi Rejected By Candidate'), (49, 'Couselling form is pending'), (61, 'Service will be initiated once resume is finalized'), (62, 'Resume Boosted'), (81, 'Pending Varification Reports'), (82, 'Service is initiated'), (101, 'To start learning , it is mandatory to take this test'), (121, 'Service has been processed and Final document is ready'), (141, 'Your profile to be shared with interviewer is pending'), (142, 'Round one is not expired'), (143, 'Round one is expired'), (161, 'Refund initiated'), (162, 'Refund under progress'), (163, 'Refunded')], default=0, verbose_name='Operation Status'),
        ),
        migrations.AlterField(
            model_name='orderitemoperation',
            name='last_oi_status',
            field=models.PositiveIntegerField(choices=[(0, 'Default'), (1, 'Assigned'), (2, 'Resume upload is pending'), (3, 'Resume Uploaded'), (4, 'Closed'), (5, 'Service is under progress'), (6, 'Service has been processed'), (10, 'On Hold by Vendor'), (11, 'Archived'), (12, 'Unhold by Vendor'), (13, 'Shine Resume'), (21, 'Upload Draft'), (22, 'Draft Uploaded'), (23, 'Pending Approval'), (24, 'Approved'), (25, 'Rejected By Admin'), (26, 'Rejected By Candidate'), (27, 'Service has been processed and Document is finalized'), (28, 'Feature profile initiated'), (29, 'Feature profile expired'), (30, 'Feature profile updated'), (43, 'Linkedin Draft Create'), (44, 'Linkedin Draft Created'), (45, 'Linkedin Pending Approval'), (46, 'Linkedin Approved'), (47, 'Linkedin Rejected By Admin'), (48, 'Linkedi Rejected By Candidate'), (49, 'Couselling form is pending'), (61, 'Service will be initiated once resume is finalized'), (62, 'Resume Boosted'), (81, 'Pending Varification Reports'), (82, 'Service is initiated'), (101, 'To start learning , it is mandatory to take this test'), (121, 'Service has been processed and Final document is ready'), (141, 'Your profile to be shared with interviewer is pending'), (142, 'Round one is not expired'), (143, 'Round one is expired'), (161, 'Refund initiated'), (162, 'Refund under progress'), (163, 'Refunded')], default=0, verbose_name='Last Operation Status'),
        ),
        migrations.AlterField(
            model_name='orderitemoperation',
            name='oi_status',
            field=models.PositiveIntegerField(choices=[(0, 'Default'), (1, 'Assigned'), (2, 'Resume upload is pending'), (3, 'Resume Uploaded'), (4, 'Closed'), (5, 'Service is under progress'), (6, 'Service has been processed'), (10, 'On Hold by Vendor'), (11, 'Archived'), (12, 'Unhold by Vendor'), (13, 'Shine Resume'), (21, 'Upload Draft'), (22, 'Draft Uploaded'), (23, 'Pending Approval'), (24, 'Approved'), (25, 'Rejected By Admin'), (26, 'Rejected By Candidate'), (27, 'Service has been processed and Document is finalized'), (28, 'Feature profile initiated'), (29, 'Feature profile expired'), (30, 'Feature profile updated'), (43, 'Linkedin Draft Create'), (44, 'Linkedin Draft Created'), (45, 'Linkedin Pending Approval'), (46, 'Linkedin Approved'), (47, 'Linkedin Rejected By Admin'), (48, 'Linkedi Rejected By Candidate'), (49, 'Couselling form is pending'), (61, 'Service will be initiated once resume is finalized'), (62, 'Resume Boosted'), (81, 'Pending Varification Reports'), (82, 'Service is initiated'), (101, 'To start learning , it is mandatory to take this test'), (121, 'Service has been processed and Final document is ready'), (141, 'Your profile to be shared with interviewer is pending'), (142, 'Round one is not expired'), (143, 'Round one is expired'), (161, 'Refund initiated'), (162, 'Refund under progress'), (163, 'Refunded')], default=0, verbose_name='Operation Status'),
        ),
        migrations.AlterField(
            model_name='refunditem',
            name='type_refund',
            field=models.CharField(choices=[('select', 'Select Refund Type'), ('full', 'Full Refund'), ('partial', 'Partial Refund')], default='select', max_length=255),
        ),
        migrations.AlterField(
            model_name='refundoperation',
            name='last_status',
            field=models.PositiveIntegerField(choices=[(0, 'Default'), (1, 'Ops Head Approval'), (2, 'Ops Head Rejected'), (3, 'Business Head Approval'), (4, 'Business Head Rejected'), (5, 'Dept. Head Approval'), (6, 'Dept. Head Rejected'), (7, 'Finance Approval'), (8, 'Refund Approved'), (9, 'Refund Initiate'), (10, 'Refund under progress'), (11, 'Refunded'), (12, 'Request Updated'), (13, 'Cancel Request')], default=0, verbose_name='Last Status'),
        ),
        migrations.AlterField(
            model_name='refundoperation',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, 'Default'), (1, 'Ops Head Approval'), (2, 'Ops Head Rejected'), (3, 'Business Head Approval'), (4, 'Business Head Rejected'), (5, 'Dept. Head Approval'), (6, 'Dept. Head Rejected'), (7, 'Finance Approval'), (8, 'Refund Approved'), (9, 'Refund Initiate'), (10, 'Refund under progress'), (11, 'Refunded'), (12, 'Request Updated'), (13, 'Cancel Request')], default=0, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='refundrequest',
            name='last_status',
            field=models.PositiveIntegerField(choices=[(0, 'Default'), (1, 'Ops Head Approval'), (2, 'Ops Head Rejected'), (3, 'Business Head Approval'), (4, 'Business Head Rejected'), (5, 'Dept. Head Approval'), (6, 'Dept. Head Rejected'), (7, 'Finance Approval'), (8, 'Refund Approved'), (9, 'Refund Initiate'), (10, 'Refund under progress'), (11, 'Refunded'), (12, 'Request Updated'), (13, 'Cancel Request')], default=0, verbose_name='Last Status'),
        ),
        migrations.AlterField(
            model_name='refundrequest',
            name='refund_mode',
            field=models.CharField(choices=[('select', 'Select Mode'), ('neft', 'NEFT'), ('cheque', 'CHEQUE'), ('dd', 'DD')], default='select', max_length=255),
        ),
        migrations.AlterField(
            model_name='refundrequest',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, 'Default'), (1, 'Ops Head Approval'), (2, 'Ops Head Rejected'), (3, 'Business Head Approval'), (4, 'Business Head Rejected'), (5, 'Dept. Head Approval'), (6, 'Dept. Head Rejected'), (7, 'Finance Approval'), (8, 'Refund Approved'), (9, 'Refund Initiate'), (10, 'Refund under progress'), (11, 'Refunded'), (12, 'Request Updated'), (13, 'Cancel Request')], default=0, verbose_name='Status'),
        ),
    ]
