from datetime import date, timedelta

import numpy as np
from django.http import JsonResponse

from .models import Buyer, Container, Order, Product, ProductGroup


def orders_per_product_group(product_group_id: int, n: int | str = 10, order: str = "desc"):
    order_by = order_by if order == "asc" else "-date"
    if n == "all":
        return Order.objects.filter(product__group_id=product_group_id).order_by(order_by)
    return Order.objects.filter(product__group_id=product_group_id).order_by(order_by)[:n]


def orders_per_product(product_id: int, n: int | str = 10, order: str = "desc"):
    order_by = "date" if order == "asc" else "-date"
    if n == "all":
        return Order.objects.filter(product_id=product_id).order_by(order_by)
    return Order.objects.filter(product_id=product_id).order_by(order_by)[:n]


def orders_per_buyer(buyer_id: int, n: int | str = 10, order: str = "desc"):
    order_by = "date" if order == "asc" else "-date"
    if n == "all":
        return Order.objects.filter(buyer_id=buyer_id).order_by(order_by)
    return Order.objects.filter(buyer_id=buyer_id).order_by(order_by)[:n]


def amount_products_per_product_group_per_buyer(request, buyer_id: int):
    result = {"result": []}
    for product_group in ProductGroup.objects.all().order_by("name"):
        amount = 0
        for order in Order.objects.filter(buyer_id=buyer_id, product__group_id=product_group.pk):
            amount += order.amount
        result["result"].append(
            {
                "label": product_group.name,
                "amount": amount,
            }
        )
    return JsonResponse(result)


def amount_products_sold_per_product_group(request):
    result = {"result": []}
    for product_group in ProductGroup.objects.all().order_by("name"):
        amount = 0
        for order in Order.objects.filter(product__group_id=product_group.pk):
            amount += order.amount
        result["result"].append(
            {
                "label": product_group.name,
                "amount": amount,
            }
        )
    return JsonResponse(result)


def amount_sold_per_product(request, product_group_id: int):
    result = {"result": []}
    for product in Product.objects.filter(group_id=product_group_id).order_by("name"):
        amount = 0
        for order in Order.objects.filter(product_id=product.pk):
            amount += order.amount
        result["result"].append(
            {
                "label": product.name,
                "amount": amount,
            }
        )
    return JsonResponse(result)


def price_products_sold_per_product_group(request):
    result = {"result": []}
    for product_group in ProductGroup.objects.all().order_by("name"):
        price = 0
        for order in Order.objects.filter(product__group_id=product_group.pk):
            price += order.price
        result["result"].append(
            {
                "label": product_group.name,
                "amount": price,
            }
        )
    return JsonResponse(result)


def price_per_product(request, product_group_id: int):
    result = {"result": []}
    for product in Product.objects.filter(group_id=product_group_id).order_by("name"):
        price = 0
        for order in Order.objects.filter(product_id=product.pk):
            price += order.price
        result["result"].append(
            {
                "label": product.name,
                "amount": price,
            }
        )
    return JsonResponse(result)


def price_over_time_per_product(request, product_id: int):
    result = {"result": []}
    for order in Order.objects.filter(product_id=product_id).order_by("date"):
        result["result"].append(
            {
                "date": order.date,
                "price": order.price_per_piece,
                "amount": order.amount,
            }
        )
    return JsonResponse(result)


def turnover_per_week(request):
    first_week = date(2023, 1, 4)  # Always in the first week
    last_week = date(2023, 12, 28)  # Always in the last week
    first_day_of_first_week = first_week - timedelta(days=first_week.weekday())
    last_day_of_last_week = last_week + timedelta(days=(6 - last_week.weekday()))

    turnover_per_week = {}

    for order in Order.objects.filter(date__range=[first_day_of_first_week, last_day_of_last_week]):
        week = order.date - timedelta(
            days=order.date.weekday(),
            hours=order.date.hour,
            minutes=order.date.minute,
            seconds=order.date.second,
            microseconds=order.date.microsecond,
        )
        if week not in turnover_per_week:
            turnover_per_week[week] = 0
        turnover_per_week[week] += order.price

    result = {"result": []}
    for week, turnover in turnover_per_week.items():
        result["result"].append(
            {
                "week": week,
                "turnover": turnover,
            }
        )

    return JsonResponse(result)


def price_per_product_stats(request, product_id: int):
    prices = []

    for order in Order.objects.filter(product_id=product_id):
        prices.extend([order.price_per_piece] * order.amount)

    prices = np.array(prices, dtype=np.float64)

    result = {
        "result": {
            "label": Product.objects.get(pk=product_id).name,
            "average": np.average(prices),
            "minimum": np.min(prices),
            "maximum": np.max(prices),
            "median": np.median(prices),
            "std": np.std(prices),
            "amount": len(prices),
            "total": np.sum(prices),
            "quarter_1": np.percentile(prices, 25),
            "quarter_3": np.percentile(prices, 75),
        }
    }

    return JsonResponse(result)


def histogram_of_product_prices(request, product_id: int):
    prices = []

    for order in Order.objects.filter(product_id=product_id):
        prices.extend([order.price_per_piece] * order.amount)

    prices = np.array(prices, dtype=np.float64)

    n_bins = round(0.5 * np.sqrt(len(prices)))

    hist, bin_edges = np.histogram(prices, bins=n_bins)

    result = {
        "result": {
            "label": Product.objects.get(pk=product_id).name,
            "hist": hist.tolist(),
            "bin_edges": bin_edges.tolist(),
            "bin_size": bin_edges[1] - bin_edges[0],
            "average": np.average(prices),
            "std": np.std(prices),
            "quarter_1": np.percentile(prices, 25),
            "quarter_3": np.percentile(prices, 75),
            "eigth_1": np.percentile(prices, 12.5),
            "eigth_7": np.percentile(prices, 87.5),
        }
    }

    return JsonResponse(result)
