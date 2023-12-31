# Generated by Django 4.2.2 on 2023-06-17 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0009_auction_photos"),
    ]

    operations = [
        migrations.AddField(
            model_name="auction",
            name="auction_category",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="categories",
                to="auctions.category",
            ),
        ),
    ]
