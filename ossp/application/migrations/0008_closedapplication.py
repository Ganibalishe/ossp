# Generated by Django 3.1.2 on 2020-11-01 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0007_auto_20201101_1203'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClosedApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('application_by_commissioner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.applicationbycommissioner', verbose_name='заявка')),
            ],
            options={
                'verbose_name': 'закрытая заявка',
                'verbose_name_plural': 'закрытые заявки',
            },
        ),
    ]
