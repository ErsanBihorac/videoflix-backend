# Generated by Django 5.1.1 on 2024-10-11 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_alter_video_video_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='location',
        ),
    ]
