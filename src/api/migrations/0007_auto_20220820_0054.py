# Generated by Django 3.1.6 on 2022-08-20 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20220819_0128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='status',
            field=models.CharField(default='En Attente', max_length=10),
        ),
    ]
