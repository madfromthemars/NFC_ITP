# Generated by Django 4.2.3 on 2023-08-07 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.JSONField(max_length=255, null=True),
        ),
    ]
