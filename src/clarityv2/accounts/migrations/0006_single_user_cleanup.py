from django.db import migrations

# Apps removed from the project long ago whose tables, migration records and
# content types were left behind in the database.
REMOVED_APPS = ('account', 'axes', 'blog', 'portfolio', 'sites', 'socialaccount', 'taggit')

ORPHAN_TABLES = (
    'account_emailconfirmation',
    'account_emailaddress',
    'axes_accessattempt',
    'axes_accesslog',
    'blog_blogpost',
    'portfolio_entry',
    'socialaccount_socialtoken',
    'socialaccount_socialapp_sites',
    'socialaccount_socialaccount',
    'socialaccount_socialapp',
    'taggit_taggeditem',
    'taggit_tag',
    'django_site',
)


def delete_removed_apps_metadata(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'ContentType')
    # Cascades to the stale auth permissions.
    ContentType.objects.filter(app_label__in=REMOVED_APPS).delete()


def delete_external_users(apps, schema_editor):
    """
    Client logins existed so customers could view their billing data. The admin
    is the only remaining surface, so non-staff accounts have no purpose.
    """
    User = apps.get_model('accounts', 'User')
    User.objects.filter(is_staff=False).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_adminuser_vat_number'),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('crm', '0014_remove_user'),
        ('work_entries', '0004_remove_user'),
    ]

    operations = [
        # One statement so foreign keys between the orphan tables do not block the drop.
        migrations.RunSQL(
            'DROP TABLE IF EXISTS %s;' % ', '.join(ORPHAN_TABLES),
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            "DELETE FROM django_migrations WHERE app IN (%s);" % ', '.join("'%s'" % app for app in REMOVED_APPS),
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RunPython(delete_removed_apps_metadata, migrations.RunPython.noop),
        migrations.RunPython(delete_external_users, migrations.RunPython.noop),
    ]
