# Generated by Django 4.2.5 on 2023-11-30 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page1', '0024_order_ready_to_deliver'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='razorpay_order_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]