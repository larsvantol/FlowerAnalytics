"""Parses a file object and returns a list with dictionaries of the parsed data."""

import csv
import re
import time
from datetime import datetime
from itertools import count

from .models import Buyer, Container, Order, Product, ProductGroup, UploadedFloridayFile
from .product_parsers import parse_product


def parse_date(date_str):
    # 27-12-2023 01:00
    # 1-1-2023 01:00
    # Test if string is in correct format with regex
    if not re.match(r"\d{1,2}-\d{1,2}-\d{4} \d{2}:\d{2}", date_str):
        raise ValueError(f"Invalid date format: {date_str}")
    date = time.strptime(date_str, "%d-%m-%Y %H:%M")
    # If year is not 2023 raise error
    if date.tm_year != 2023:
        raise ValueError(f"Invalid year: {date.tm_year}")
    return datetime.fromtimestamp(time.mktime(date))


def create_product(product_data):
    group = ProductGroup.objects.get(vbn_code=product_data["VBN productcode"])
    parsed_product = parse_product(product_data)
    product = Product(
        name=parsed_product["name"],
        code=product_data["Artikelcode"],
        group=group,
        length=parsed_product["length"],
        heads=parsed_product["heads"],
    )
    product.save()
    return product


def get_product(product_data):
    product = Product.objects.get(code=product_data["Artikelcode"])
    return product


def get_or_create_product(product_data):
    try:
        product = get_product(product_data)
    except Product.DoesNotExist:
        product = create_product(product_data)
    return product


def create_buyer(buyer_data):
    buyer_id = buyer_data["Klantnummer"] if buyer_data["Klantnummer"] else None
    buyer = Buyer(
        name=buyer_data["Klant"],
        buyer_id=buyer_id,
    )
    buyer.save()
    return buyer


def get_buyer(buyer_data):
    if buyer_data["Klantnummer"] != "":
        buyer = Buyer.objects.get(buyer_id=buyer_data["Klantnummer"])
    else:
        buyer = Buyer.objects.get(name=buyer_data["Klant"])
    return buyer


def get_or_create_buyer(buyer_data):
    try:
        buyer = get_buyer(buyer_data)
    except Buyer.DoesNotExist:
        buyer = create_buyer(buyer_data)
    return buyer


def create_field(field_data):
    field = Container(
        name=field_data["Fustcode"],
        fust=field_data["Fustcode"],
    )
    field.save()
    return field


def get_field(field_data):
    field = Container.objects.get(fust=field_data["Fustcode"])
    return field


def get_or_create_field(field_data):
    try:
        field = get_field(field_data)
    except Container.DoesNotExist:
        field = create_field(field_data)
    return field


def create_order(floriday, order_data):
    product = get_or_create_product(order_data)
    buyer = get_or_create_buyer(order_data)
    field = get_or_create_field(order_data)

    date = parse_date(order_data["Besteld"])
    delivery_date = parse_date(order_data["Levering"]) if order_data["Levering"] else None
    price_per_piece = order_data["Prijs per stuk"].replace(",", ".")
    price = order_data["Totale prijs"].replace(",", ".")

    order = Order(
        product=product,
        buyer=buyer,
        buyer_reference=order_data["Klant referentie"],
        bundles=order_data["Aantal fust"],
        amount_per_bundle=order_data["Aantal stuks per fust"],
        amount=order_data["Aantal stuks"],
        price_per_piece=price_per_piece,
        price=price,
        date=date,
        delivery_date=delivery_date,
        channel=order_data["Verkoopkanaal"],
        field=field,
        created_by_floriday_file=floriday,
    )
    order.save()
    return order


def remap(fieldnames):
    price_count = count(1)
    return [
        "Eigenschap{}".format(next(price_count)) if f.startswith("Eigenschap") else f
        for f in fieldnames
    ]


def handle_uploaded_file(file):
    # Create UploadedFloridayFile object
    uploaded_file = UploadedFloridayFile(name=file.name, rows=0)
    uploaded_file.save()
    # Reads the full file into memory, not suitable for large files
    decoded_file = file.read().decode("utf-8").splitlines()
    reader = csv.reader(decoded_file, delimiter=";")
    fieldnames = remap(next(reader))
    data = []
    for row in reader:
        data.append(dict(zip(fieldnames, row)))

    if len(data) == 0:
        raise ValueError("No data found in file")
    else:
        uploaded_file.rows = len(data)
        uploaded_file.save()
    for row in data:
        create_order(uploaded_file, row)
