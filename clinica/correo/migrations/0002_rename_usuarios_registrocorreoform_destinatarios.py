# Generated by Django 4.2 on 2023-08-04 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('correo', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registrocorreoform',
            old_name='usuarios',
            new_name='destinatarios',
        ),
    ]
