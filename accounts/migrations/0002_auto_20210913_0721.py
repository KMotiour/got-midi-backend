# Generated by Django 3.2.6 on 2021-09-13 07:21

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newusers',
            name='first_name',
            field=models.CharField(max_length=50, verbose_name='First_name'),
        ),
        migrations.AlterField(
            model_name='newusers',
            name='last_name',
            field=models.CharField(max_length=50, verbose_name='Last_name'),
        ),
        migrations.AlterField(
            model_name='newusers',
            name='profilePic',
            field=models.ImageField(default='default.jpg', upload_to=accounts.models.upload_Music),
        ),
    ]
