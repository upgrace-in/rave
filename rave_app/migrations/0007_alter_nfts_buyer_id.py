# Generated by Django 3.2.6 on 2021-11-20 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rave_app', '0006_nfts_wallet_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nfts',
            name='buyer_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]