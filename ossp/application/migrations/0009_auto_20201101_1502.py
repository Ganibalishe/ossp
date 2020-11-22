# Generated by Django 3.1.2 on 2020-11-01 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0008_closedapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='closedapplication',
            name='comment',
            field=models.TextField(default='', verbose_name='комментрарий'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='applicationbycommissioner',
            name='status',
            field=models.CharField(choices=[('new', 'новая'), ('sent', 'отправлена'), ('in_work', 'в работе'), ('decision', 'принято решение'), ('service_provided', 'услуга оказана'), ('closed', 'закрыта')], default='new', max_length=25, verbose_name='статус'),
        ),
    ]