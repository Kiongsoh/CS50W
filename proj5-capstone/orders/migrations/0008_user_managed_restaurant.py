# Generated by Django 5.0.3 on 2024-11-04 08:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='managed_restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managers', to='orders.restaurant'),
        ),
    ]