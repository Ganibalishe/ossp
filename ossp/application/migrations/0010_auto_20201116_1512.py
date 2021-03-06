# Generated by Django 3.1.2 on 2020-11-16 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0009_auto_20201101_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationbycommissioner',
            name='application_by_dispatcher',
            field=models.ForeignKey(blank=True, help_text='указывается если заявка пришла от диспетчека', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='app_by_com', to='application.applicationbydispatcher', verbose_name='заявка от диспетчера'),
        ),
    ]
