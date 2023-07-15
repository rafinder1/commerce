# Generated by Django 4.2.2 on 2023-06-17 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0002_auction_comment_bid"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bid",
            name="auction",
        ),
        migrations.RemoveField(
            model_name="bid",
            name="bidder",
        ),
        migrations.RemoveField(
            model_name="comment",
            name="auction",
        ),
        migrations.RemoveField(
            model_name="comment",
            name="commenter",
        ),
        migrations.DeleteModel(
            name="Auction",
        ),
        migrations.DeleteModel(
            name="Bid",
        ),
        migrations.DeleteModel(
            name="Comment",
        ),
    ]
