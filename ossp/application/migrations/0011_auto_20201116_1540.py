# Generated by Django 3.1.2 on 2020-11-16 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0010_auto_20201116_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decision',
            name='application_by_commissioner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='decision', to='application.applicationbycommissioner', verbose_name='заявка'),
        ),
    ]