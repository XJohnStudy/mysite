# Generated by Django 2.2.4 on 2020-02-15 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likerecord',
            name='liked_time',
            field=models.DateField(auto_now_add=True),
        ),
    ]
