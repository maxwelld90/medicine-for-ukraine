# Generated by Django 4.0.3 on 2022-03-15 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0002_userrequest_storesession_screenshot_requesteditem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screenshot',
            name='filename',
            field=models.ImageField(upload_to='screenshots/'),
        ),
    ]
