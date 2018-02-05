from django.db import migrations


def create_userprofile(apps, schema_editor):
    User = apps.get_model('users', 'User')
    for row in User.objects.all():
        row.save()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20180125_1725'),
    ]

    operations = [
        # omit reverse_code=... if you don't want the migration to be reversible.
        migrations.RunPython(
            create_userprofile,
            reverse_code=migrations.RunPython.noop),
    ]