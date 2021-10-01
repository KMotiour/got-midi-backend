# Generated by Django 3.2.6 on 2021-09-14 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_aboutus_conturctus_legal_termsandcondition'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aboutUs', models.TextField()),
                ('contactUs', models.TextField()),
                ('legal', models.TextField()),
                ('termsAndCondition', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='AboutUs',
        ),
        migrations.DeleteModel(
            name='ConturctUs',
        ),
        migrations.DeleteModel(
            name='legal',
        ),
        migrations.DeleteModel(
            name='TermsAndCondition',
        ),
    ]