from django.db import models


class MarketHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    item_amount = models.BigIntegerField()
    silver_amount = models.BigIntegerField()
    item_id = models.CharField(max_length=128)
    location = models.PositiveSmallIntegerField()
    quality = models.PositiveIntegerField()
    timestamp = models.DateTimeField()
    aggregation = models.IntegerField()

    class Meta:
        db_table = 'market_history'
        unique_together = (('item_id', 'quality', 'location', 'timestamp', 'aggregation'),)


class MarketOrders(models.Model):
    id = models.BigAutoField(primary_key=True)
    item_id = models.CharField(max_length=128, blank=True, null=True)
    location = models.PositiveSmallIntegerField()
    quality_level = models.PositiveIntegerField()
    enchantment_level = models.PositiveIntegerField()
    price = models.BigIntegerField()
    amount = models.PositiveIntegerField()
    auction_type = models.CharField(max_length=32, blank=True, null=True)
    expires = models.DateTimeField()
    albion_id = models.BigIntegerField(unique=True)
    initial_amount = models.PositiveIntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.item_id + " " + str(self.price) + " " + str(self.location)

    class Meta:
        db_table = 'market_orders'



class MarketStats(models.Model):
    id = models.BigAutoField(primary_key=True)
    item_id = models.CharField(max_length=128)
    location = models.PositiveSmallIntegerField()
    price_avg = models.DecimalField(max_digits=65, decimal_places=30)
    price_max = models.BigIntegerField()
    price_min = models.BigIntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        db_table = 'market_stats'
        unique_together = (('item_id', 'location', 'timestamp'),)
