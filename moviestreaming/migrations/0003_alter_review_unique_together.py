# Generated by Django 3.2.5 on 2021-08-06 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moviestreaming', '0002_auto_20210806_0654'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('user', 'movie')},
        ),
    ]
