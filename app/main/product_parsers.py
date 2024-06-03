"""Parsers for product data."""

from .models import Product

parsers = {}


def parse_property(property_str):
    # S22:010 -> "S22", 10
    code, value = property_str.split(":")
    return code, int(value)


def parse_properties(product_data):
    properties = {}
    for property_key in product_data.keys():
        if property_key.startswith("Eigenschap"):
            code, value = parse_property(product_data[property_key])
            properties[code] = value
    return properties


def parse_product(product_data):
    # Code    Omschrijving
    # S20     MN STLENGTE
    # S21     GEWICHT GEMIDDELD
    # S05     RIJPHEID
    # S56     TEELTWYZE
    # L11     STELEN BOS

    properties = parse_properties(product_data)
    length = properties.get("S20") if "S20" in properties else None
    heads = properties.get("L11") if "L11" in properties else None

    return {
        "name": product_data["Artikel"],
        "length": length,
        "heads": heads,
    }
