# Generated by Django 2.2.17 on 2021-02-14 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_openidclientpolicy'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OpenIDClientPolicy',
        ),
    ]
