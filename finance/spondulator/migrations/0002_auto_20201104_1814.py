# Generated by Django 3.1.2 on 2020-11-04 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spondulator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cash',
            name='in_hand_money',
            field=models.IntegerField(default=10000),
        ),
        migrations.AddField(
            model_name='cash',
            name='net_profit',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='purchase',
            name='bought_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='purchase',
            name='price',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='purchase',
            name='shares',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='purchase',
            name='stock',
            field=models.CharField(max_length=5, null=True),
        ),
    ]