# Generated by Django 5.0.10 on 2025-02-28 10:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("zerver", "0683_alter_realm_can_manage_billing_group"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="is_billing_admin",
        ),
    ]
