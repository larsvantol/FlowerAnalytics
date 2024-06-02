from django.urls import path

from .model_views import (
    amount_products_per_product_group_per_buyer,
    amount_products_sold_per_product_group,
    amount_sold_per_product,
    histogram_of_product_prices,
    price_over_time_per_product,
    price_per_product,
    price_per_product_stats,
    price_products_sold_per_product_group,
    turnover_per_week,
)
from .views import (
    delete_floriday_file,
    inzichten,
    klanten,
    producten,
    search,
    upload_file,
    zoeken,
)

view_urlpatters = [
    path("", zoeken, name="index"),
    path("Klanten", klanten, name="klanten"),
    path("Producten", producten, name="producten"),
    path("Inzichten", inzichten, name="inzichten"),
    path("upload/", upload_file, name="upload"),
]

api_urlpatterns = [
    path(
        "api/amount_products_per_product_group_per_buyer/<int:buyer_id>",
        amount_products_per_product_group_per_buyer,
        name="amount_products_per_product_group_per_buyer",
    ),
    path(
        "api/amount_products_sold_per_product_group",
        amount_products_sold_per_product_group,
        name="amount_products_sold_per_product_group",
    ),
    path(
        "api/price_products_sold_per_product_group",
        price_products_sold_per_product_group,
        name="price_products_sold_per_product_group",
    ),
    path(
        "api/amount_sold_per_product/<int:product_group_id>",
        amount_sold_per_product,
        name="amount_sold_per_product",
    ),
    path(
        "api/price_per_product/<int:product_group_id>",
        price_per_product,
        name="price_per_product",
    ),
    path(
        "api/price_over_time_per_product/<int:product_id>",
        price_over_time_per_product,
        name="price_over_time_per_product",
    ),
    path("api/turnover_per_week", turnover_per_week, name="turnover_per_week"),
    path(
        "api/price_per_product_stats/<int:product_id>",
        price_per_product_stats,
        name="price_per_product_stats",
    ),
    path(
        "api/histogram_of_product_prices/<int:product_id>",
        histogram_of_product_prices,
        name="histogram_of_product_prices",
    ),
    path("api/search/<str:search_query>", search, name="search"),
    path("api/search/", search, name="search"),
    path(
        "api/delete/floriday/<int:floriday_file_id>",
        delete_floriday_file,
        name="delete_floriday_file",
    ),
]

urlpatterns = view_urlpatters + api_urlpatterns
