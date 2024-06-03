"""Models for the FlowerAnalytics app."""

from django.db import models


class UploadedFloridayFile(models.Model):
    name = models.CharField(max_length=30)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    rows = models.IntegerField()

    def __str__(self) -> str:
        return f"UploadedFloridayFile(name={self.name}, uploaded_at={self.uploaded_at}, rows={self.rows})"


class Container(models.Model):
    name = models.CharField(max_length=30)
    fust = models.IntegerField()

    def __str__(self) -> str:
        return f"Container(name={self.name}, fust={self.fust})"


class Buyer(models.Model):
    name = models.CharField(max_length=30)
    buyer_id = models.IntegerField(blank=True, null=True, unique=True)

    def __str__(self) -> str:
        return f"Buyer(name={self.name})"


class ProductGroup(models.Model):
    name = models.CharField(max_length=30)
    vbn_code = models.IntegerField()
    color = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f"ProductGroup(name={self.name})"


class Product(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=30)
    group = models.ForeignKey(ProductGroup, on_delete=models.CASCADE)
    length = models.FloatField(blank=True, null=True)
    heads = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return f"Product(name={self.name}, group={self.group}, length={self.length}, heads={self.heads})"


class Order(models.Model):
    channel_choices = [
        ("rfhclock", "RfhClock"),
        ("floramondo", "FloraMondo"),
    ]
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    buyer = models.ForeignKey(Buyer, on_delete=models.PROTECT)
    field = models.ForeignKey(Container, on_delete=models.PROTECT)
    buyer_reference = models.CharField(max_length=30, blank=True, null=True)
    bundles = models.IntegerField()
    amount_per_bundle = models.IntegerField()
    amount = models.IntegerField()
    price_per_piece = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    delivery_date = models.DateTimeField(blank=True, null=True)
    channel = models.CharField(max_length=10, choices=channel_choices)

    created_by_floriday_file = models.ForeignKey(UploadedFloridayFile, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Order(product={self.product}, buyer={self.buyer}, buyer_reference={self.buyer_reference}, bundles={self.bundles}, amount_per_bundle={self.amount_per_bundle}, amount={self.amount}, price_per_piece={self.price_per_piece}, price={self.price}, date={self.date}, delivery_date={self.delivery_date}, channel={self.channel})"
