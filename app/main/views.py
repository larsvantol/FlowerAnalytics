from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Imaginary function to handle an uploaded file.
from .floriday_parser import handle_uploaded_file
from .forms import UploadFileForm
from .model_views import orders_per_buyer, orders_per_product, orders_per_product_group
from .models import Buyer, Product, ProductGroup, UploadedFloridayFile

WEBSITE_URLS = [
    {"name": "Zoeken", "url": "/", "icon": "search"},
    {"name": "Klanten", "url": "/Klanten", "icon": "storefront"},
    {"name": "Producten", "url": "/Producten", "icon": "deceased"},
    {"name": "Inzichten", "url": "/Inzichten", "icon": "monitoring"},
    {"name": "Upload", "url": "/upload", "icon": "upload_file"},
]


def zoeken(request):
    context = {
        "title": "Flower Analytics",
        "subtitle": "Zoeken",
        "icon": "search",
        "urls": WEBSITE_URLS,
    }
    return render(request, "zoeken.html", context)


def search(request, search_query=""):
    if not search_query or search_query == "":
        return JsonResponse(
            {"buyers": [], "products": [], "product_groups": [], "search_query": ""}
        )
    buyers = Buyer.objects.filter(name__icontains=search_query).order_by(
        "name"
    ) | Buyer.objects.filter(buyer_id__icontains=search_query).order_by("name")
    products = Product.objects.filter(name__icontains=search_query).order_by(
        "name"
    ) | Product.objects.filter(code__icontains=search_query).order_by("name")
    product_groups = ProductGroup.objects.filter(name__icontains=search_query).order_by(
        "name"
    ) | ProductGroup.objects.filter(vbn_code__icontains=search_query).order_by("name")
    search_result = {
        "buyers": [
            {"pk": buyer.pk, "name": buyer.name, "buyer_id": buyer.buyer_id} for buyer in buyers
        ],
        "products": [
            {"pk": product.pk, "name": product.name, "code": product.code} for product in products
        ],
        "product_groups": [
            {"pk": product_group.pk, "name": product_group.name, "vbn_code": product_group.vbn_code}
            for product_group in product_groups
        ],
        "search_query": search_query,
    }
    return JsonResponse(search_result)


def klanten(request):
    klant_id = request.GET.get("klant", "-1")
    selected_klant = Buyer.objects.get(id=klant_id) if klant_id and klant_id != "-1" else None
    buyers = [
        {
            "name": buyer.name,
            "pk": buyer.pk,
            "selected": "1" if buyer.pk == int(klant_id) else "0",
        }
        for buyer in Buyer.objects.all().order_by("name")
    ]
    orders = orders_per_buyer(int(klant_id), 10, "desc") if klant_id != "-1" else []
    context = {
        "title": "Flower Analytics",
        "subtitle": "Klanten",
        "icon": "storefront",
        "urls": WEBSITE_URLS,
        "klanten": buyers,
        "selected_klant": selected_klant,
        "orders": orders,
    }
    return render(request, "klanten.html", context)


def producten(request):
    selected_product_id = request.GET.get("product", "-1")
    selected_product_group_id = request.GET.get("product_group", "-1")
    product_groups = [
        {
            "name": product_group.name,
            "pk": product_group.pk,
            "color": product_group.color,
            "vbn_code": product_group.vbn_code,
            "selected": "1" if product_group.pk == int(selected_product_group_id) else "0",
        }
        for product_group in ProductGroup.objects.all().order_by("name")
    ]
    products = {
        group.pk: [
            {
                "name": product.name,
                "pk": product.pk,
                "selected": "1" if product.pk == int(selected_product_id) else "0",
            }
            for product in Product.objects.filter(group=group).order_by("name")
        ]
        for group in ProductGroup.objects.all().order_by("name")
    }
    selected_product = (
        Product.objects.get(id=selected_product_id)
        if selected_product_id and selected_product_id != "-1"
        else None
    )
    selected_product_group = (
        ProductGroup.objects.get(id=selected_product_group_id)
        if selected_product_group_id and selected_product_group_id != "-1"
        else None
    )
    if selected_product:
        orders = orders_per_product(int(selected_product_id), 10, "desc")
    elif selected_product_group:
        orders = orders_per_product_group(int(selected_product_group_id), 10, "desc")
    else:
        orders = []
    context = {
        "title": "Flower Analytics",
        "subtitle": "Producten",
        "icon": "deceased",
        "urls": WEBSITE_URLS,
        "product_groups": product_groups,
        "products": products,
        "selected_product": selected_product,
        "selected_product_group": selected_product_group,
        "orders": orders,
    }
    return render(request, "producten.html", context)


def inzichten(request):
    context = {
        "title": "Flower Analytics",
        "subtitle": "Inzichten",
        "icon": "monitoring",
        "urls": WEBSITE_URLS,
    }
    return render(request, "inzichten.html", context)


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"])
            return HttpResponseRedirect("/Producten")
        else:
            print(form.errors)
    else:
        form = UploadFileForm()
    context = {
        "title": "Flower Analytics",
        "subtitle": "Upload",
        "icon": "upload_file",
        "urls": WEBSITE_URLS,
        "form": form,
        "floriday_files": UploadedFloridayFile.objects.all().order_by("-uploaded_at"),
    }
    return render(request, "upload.html", context)


def delete_floriday_file(request, floriday_file_id):
    if request.method == "DELETE":
        floriday_file = UploadedFloridayFile.objects.get(id=floriday_file_id)
        floriday_file.delete()
        return JsonResponse({"status": "ok"})
    return JsonResponse(
        {"status": "error", "message": f"Only DELETE requests are allowed, not {request.method}"}
    )
