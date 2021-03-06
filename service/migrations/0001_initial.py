# Generated by Django 3.0.7 on 2020-09-17 05:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.TextField(blank=True, max_length=500)),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('region', models.CharField(blank=True, max_length=30)),
                ('address', models.CharField(blank=True, max_length=40)),
                ('is_company', models.BooleanField(default=False)),
                ('is_manufacturer', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=40)),
                ('address', models.CharField(blank=True, max_length=40)),
                ('budget', models.IntegerField(default=0)),
                ('profile', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='service.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='ProductsForCheckout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Bitumen', 'Bitumen'), ('Cement', 'Cement'), ('Steel', 'Steel'), ('Admixture', 'Admixture'), ('Plywood', 'Plywood'), ('Tin', 'Tin'), ('Paint', 'Paint'), ('Machinery', 'Machinery')], default=None, max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('cart', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='service.Cart')),
                ('profile', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='service.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Bitumen', 'Bitumen'), ('Cement', 'Cement'), ('Steel', 'Steel'), ('Admixture', 'Admixture'), ('Plywood', 'Plywood'), ('Tin', 'Tin'), ('Paint', 'Paint'), ('Machinery', 'Machinery')], default=None, max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantityAvailable', models.IntegerField(default=0)),
                ('availability', models.BooleanField(default=True)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='EditedProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=20)),
                ('profile', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='service.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='profile',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='service.Profile'),
        ),
    ]
