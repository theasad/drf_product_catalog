# Generated by Django 4.0.4 on 2022-05-20 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='position',
            field=models.PositiveIntegerField(default=1, verbose_name='Position'),
        ),
    ]
