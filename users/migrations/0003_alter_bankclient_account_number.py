# Generated by Django 4.1.7 on 2023-05-24 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_rename_client_bankclient"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bankclient",
            name="account_number",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
