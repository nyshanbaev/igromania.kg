# Generated by Django 4.1.7 on 2023-02-24 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
