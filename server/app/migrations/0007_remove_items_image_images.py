# Generated by Django 4.2.7 on 2023-12-12 06:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_items_category_delete_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='items',
            name='image',
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='pics')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.items')),
            ],
        ),
    ]
