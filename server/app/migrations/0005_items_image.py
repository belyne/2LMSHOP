# Generated by Django 4.2.7 on 2023-12-11 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_items_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='image',
            field=models.ImageField(null=True, upload_to='pics'),
        ),
    ]
