# Generated by Django 2.0.2 on 2018-10-07 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studdybuddy', '0004_auto_20181001_0349'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='slack_handle',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
