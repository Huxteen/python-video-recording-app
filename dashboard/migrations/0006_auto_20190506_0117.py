# Generated by Django 2.0.7 on 2019-05-06 00:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_repayment_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='repayment',
            old_name='loan_id',
            new_name='id_loan',
        ),
    ]
