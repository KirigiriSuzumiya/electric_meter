# Generated by Django 3.2.13 on 2022-06-24 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.DecimalField(blank=True, decimal_places=4, max_digits=100, null=True)),
                ('info', models.TextField(blank=True, max_length=1000, null=True)),
                ('image', models.CharField(max_length=1000)),
                ('upload_time', models.DateTimeField()),
            ],
        ),
    ]