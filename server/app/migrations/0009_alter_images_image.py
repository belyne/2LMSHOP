# Generated by Django 4.2.7 on 2023-12-12 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_remove_items_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.FileField(null=True, upload_to='pics'),
        ),
    ]