# Generated by Django 3.0.7 on 2020-06-12 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20200615_2204'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
