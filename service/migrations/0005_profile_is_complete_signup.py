# Generated by Django 3.0.7 on 2020-10-03 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_productsforcheckout_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_complete_signup',
            field=models.BooleanField(default=False),
        ),
    ]