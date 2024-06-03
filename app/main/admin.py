from django.contrib import admin

from .models import Buyer, Container, Order, Product, ProductGroup, UploadedFloridayFile


class UploadedFloridayFileAdmin(admin.ModelAdmin):
    list_display = ("name", "uploaded_at", "rows")


class FieldAdmin(admin.ModelAdmin):
    list_display = ("name", "fust")


class BuyerAdmin(admin.ModelAdmin):
    list_display = ("name", "buyer_id")


class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "vbn_code")


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "group", "length", "heads")


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "buyer",
        "buyer_reference",
        "bundles",
        "amount_per_bundle",
        "amount",
        "price_per_piece",
        "price",
        "date",
        "delivery_date",
    )


admin.site.register(UploadedFloridayFile, UploadedFloridayFileAdmin)
admin.site.register(Container, FieldAdmin)
admin.site.register(Buyer, BuyerAdmin)
admin.site.register(ProductGroup, ProductGroupAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
