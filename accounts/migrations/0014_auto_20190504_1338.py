# Generated by Django 2.0.7 on 2019-05-04 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20190504_1300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='status',
        ),
        migrations.AddField(
            model_name='user',
            name='email_confirmed',
            field=models.BooleanField(default=False, verbose_name='email confirmed'),
        ),
    ]
