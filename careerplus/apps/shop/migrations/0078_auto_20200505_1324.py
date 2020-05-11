# Generated by Django 2.2.10 on 2020-05-05 07:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_blog_position'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0077_auto_20200430_1649'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='job_title',
        ),
        migrations.AddField(
            model_name='productuserprofile',
            name='due_date_extended_by',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='productuserprofile',
            name='latest_education',
            field=models.PositiveSmallIntegerField(blank=True, choices=[('0', 'NA'), ('101', '10+2 or Below'), ('102', 'B.A'), ('103', 'B.Arch'), ('104', 'B.B.A / B.M.S'), ('105', 'B.C.A'), ('106', 'B.Com'), ('107', 'B.Ed'), ('108', 'B.Pharma'), ('109', 'B.Sc'), ('110', 'B.Tech/B.E'), ('111', 'BDS'), ('112', 'BHM'), ('113', 'BVSC'), ('114', 'C.A'), ('115', 'C.F.A'), ('116', 'C.S'), ('117', 'Diploma'), ('118', 'ICWA / CMA'), ('119', 'Integrated PG'), ('120', 'LL.M'), ('121', 'LLB'), ('122', 'M.A'), ('123', 'M.C.A'), ('124', 'M.Com'), ('125', 'M.Ed'), ('126', 'M.Pharma'), ('127', 'M.Sc'), ('128', 'M.Tech'), ('129', 'MBA/PGDM'), ('130', 'MBBS'), ('131', 'MD/MS'), ('132', 'MDS'), ('133', 'MMH'), ('134', 'MPHIL'), ('135', 'MVSC'), ('136', 'Other'), ('137', 'PG Diploma'), ('138', 'Ph.D/Doctorate'), ('139', 'BHMS'), ('140', 'BAMS'), ('141', 'B.P.Ed'), ('142', 'BPT'), ('143', 'BUMS'), ('144', 'CA (Intermediate)'), ('146', 'M.P.Ed')], null=True),
        ),
        migrations.CreateModel(
            name='BlogProductMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified_on', models.DateTimeField(auto_now=True, null=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Blog')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_blogproductmapping_created_by', related_query_name='shop_blogproductmappings', to=settings.AUTH_USER_MODEL)),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_blogproductmapping_last_modified_by', related_query_name='shop_blogproductmappings', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Product')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
    ]
