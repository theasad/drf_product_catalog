# Generated by Django 4.0.4 on 2022-05-20 18:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_productimage_position'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productimage',
            options={'ordering': ('position',), 'verbose_name': 'Image', 'verbose_name_plural': 'Images'},
        ),
    ]