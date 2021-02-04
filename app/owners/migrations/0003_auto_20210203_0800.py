# Generated by Django 2.2.17 on 2021-02-03 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('owners', '0002_auto_20210203_0745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connectownermanager',
            name='manager',
            field=models.ForeignKey(help_text='매니저', on_delete=django.db.models.deletion.PROTECT, to='owners.PayGoComputationalManager'),
        ),
        migrations.AlterField(
            model_name='connectownermanager',
            name='owner',
            field=models.ForeignKey(help_text='사업자', on_delete=django.db.models.deletion.PROTECT, to='owners.Owner'),
        ),
    ]
