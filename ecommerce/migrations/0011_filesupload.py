# Generated by Django 3.2.7 on 2021-11-08 11:13

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0010_merge_20211108_1054'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilesUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(default='settings.MEDIA_ROOT/media/default_file.txt', storage=django.core.files.storage.FileSystemStorage(location='/home/shashank/Desktop/fcs/media'), upload_to='documents')),
            ],
        ),
    ]
