# Generated by Django 2.1.1 on 2018-09-30 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studdybuddy', '0002_customuser_matcheduserid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='matchedUserID',
            field=models.CharField(max_length=200),
        ),
    ]
