# Generated by Django 3.1.6 on 2022-08-23 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20220820_0056'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='access_ressource_code',
            field=models.CharField(default='NoCode', max_length=30),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='recipient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_receiver', to='api.users'),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_sender', to='api.users'),
        ),
    ]