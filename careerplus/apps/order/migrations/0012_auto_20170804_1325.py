# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-04 07:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_auto_20170801_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='is_addon',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='last_oi_status',
            field=models.PositiveIntegerField(choices=[(0, 'Default'), (1, 'Assigned'), (2, 'Resume upload is pending'), (3, 'Resume Uploded'), (4, 'Closed'), (5, 'Service is under progress'), (6, 'Services has been processed'), (10, 'On Hold by Vendor'), (11, 'Archived'), (12, 'Unhold by Vendor'), (13, 'Shine Resume'), (21, 'Upload Draft'), (22, 'Draft Uploaded'), (23, 'Pending Approval'), (24, 'Approved'), (25, 'Rejected By Admin'), (26, 'Rejected By Candidate'), (27, 'Service has been processed and Document is finalized'), (28, 'Feature profile initiated'), (29, 'Feature profile expired'), (43, 'Linkedin Draft Create'), (44, 'Linkedin Draft Created'), (45, 'Linkedin Pending Approval'), (46, 'Linkedin Approved'), (47, 'Linkedin Rejected By Admin'), (48, 'Linkedi Rejected By Candidate'), (49, 'Couselling form is pending'), (61, 'Service will be initiated once resume is finalized'), (62, 'Resume Boosted'), (81, 'Pending Varification Reports'), (82, 'Service is initiated'), (101, 'To start learning , it is mandatory to take this test'), (121, 'Service has been processed and Final document is ready'), (141, 'Your profile to be shared with interviewer is pending'), (142, 'Round one is not expired'), (143, 'Round one is expired')], default=0, verbose_name='Last Operation Status'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='oi_status',
            field=models.PositiveIntegerField(choices=[(0, 'Default'), (1, 'Assigned'), (2, 'Resume upload is pending'), (3, 'Resume Uploded'), (4, 'Closed'), (5, 'Service is under progress'), (6, 'Services has been processed'), (10, 'On Hold by Vendor'), (11, 'Archived'), (12, 'Unhold by Vendor'), (13, 'Shine Resume'), (21, 'Upload Draft'), (22, 'Draft Uploaded'), (23, 'Pending Approval'), (24, 'Approved'), (25, 'Rejected By Admin'), (26, 'Rejected By Candidate'), (27, 'Service has been processed and Document is finalized'), (28, 'Feature profile initiated'), (29, 'Feature profile expired'), (43, 'Linkedin Draft Create'), (44, 'Linkedin Draft Created'), (45, 'Linkedin Pending Approval'), (46, 'Linkedin Approved'), (47, 'Linkedin Rejected By Admin'), (48, 'Linkedi Rejected By Candidate'), (49, 'Couselling form is pending'), (61, 'Service will be initiated once resume is finalized'), (62, 'Resume Boosted'), (81, 'Pending Varification Reports'), (82, 'Service is initiated'), (101, 'To start learning , it is mandatory to take this test'), (121, 'Service has been processed and Final document is ready'), (141, 'Your profile to be shared with interviewer is pending'), (142, 'Round one is not expired'), (143, 'Round one is expired')], default=0, verbose_name='Operation Status'),
        ),
        migrations.AlterField(
            model_name='orderitemoperation',
            name='last_oi_status',
            field=models.PositiveIntegerField(choices=[(0, 'Default'), (1, 'Assigned'), (2, 'Resume upload is pending'), (3, 'Resume Uploded'), (4, 'Closed'), (5, 'Service is under progress'), (6, 'Services has been processed'), (10, 'On Hold by Vendor'), (11, 'Archived'), (12, 'Unhold by Vendor'), (13, 'Shine Resume'), (21, 'Upload Draft'), (22, 'Draft Uploaded'), (23, 'Pending Approval'), (24, 'Approved'), (25, 'Rejected By Admin'), (26, 'Rejected By Candidate'), (27, 'Service has been processed and Document is finalized'), (28, 'Feature profile initiated'), (29, 'Feature profile expired'), (43, 'Linkedin Draft Create'), (44, 'Linkedin Draft Created'), (45, 'Linkedin Pending Approval'), (46, 'Linkedin Approved'), (47, 'Linkedin Rejected By Admin'), (48, 'Linkedi Rejected By Candidate'), (49, 'Couselling form is pending'), (61, 'Service will be initiated once resume is finalized'), (62, 'Resume Boosted'), (81, 'Pending Varification Reports'), (82, 'Service is initiated'), (101, 'To start learning , it is mandatory to take this test'), (121, 'Service has been processed and Final document is ready'), (141, 'Your profile to be shared with interviewer is pending'), (142, 'Round one is not expired'), (143, 'Round one is expired')], default=0, verbose_name='Last Operation Status'),
        ),
        migrations.AlterField(
            model_name='orderitemoperation',
            name='oi_status',
            field=models.PositiveIntegerField(choices=[(0, 'Default'), (1, 'Assigned'), (2, 'Resume upload is pending'), (3, 'Resume Uploded'), (4, 'Closed'), (5, 'Service is under progress'), (6, 'Services has been processed'), (10, 'On Hold by Vendor'), (11, 'Archived'), (12, 'Unhold by Vendor'), (13, 'Shine Resume'), (21, 'Upload Draft'), (22, 'Draft Uploaded'), (23, 'Pending Approval'), (24, 'Approved'), (25, 'Rejected By Admin'), (26, 'Rejected By Candidate'), (27, 'Service has been processed and Document is finalized'), (28, 'Feature profile initiated'), (29, 'Feature profile expired'), (43, 'Linkedin Draft Create'), (44, 'Linkedin Draft Created'), (45, 'Linkedin Pending Approval'), (46, 'Linkedin Approved'), (47, 'Linkedin Rejected By Admin'), (48, 'Linkedi Rejected By Candidate'), (49, 'Couselling form is pending'), (61, 'Service will be initiated once resume is finalized'), (62, 'Resume Boosted'), (81, 'Pending Varification Reports'), (82, 'Service is initiated'), (101, 'To start learning , it is mandatory to take this test'), (121, 'Service has been processed and Final document is ready'), (141, 'Your profile to be shared with interviewer is pending'), (142, 'Round one is not expired'), (143, 'Round one is expired')], default=0, verbose_name='Operation Status'),
        ),
    ]
