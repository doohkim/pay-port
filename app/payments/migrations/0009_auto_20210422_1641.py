# Generated by Django 2.2.17 on 2021-04-22 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0008_auto_20210416_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='order_number',
            field=models.CharField(default='PAYGO164120660606', max_length=25, verbose_name='주문번호'),
        ),
    ]
