# Generated by Django 5.1.4 on 2024-12-20 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_menuitem_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]
