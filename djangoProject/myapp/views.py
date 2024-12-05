from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseBadRequest
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from decimal import Decimal
from django.shortcuts import render

# Create your views here.


@csrf_exempt
def product_detail(request, product_id):
    print("1")
    if request.method == 'GET':
        try:
            product = Product.objects.get(id=product_id)
            return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'available': product.available
            })
        except Product.DoesNotExist:
            return HttpResponseBadRequest(f"404 Not Found: Product with id {product_id} does not exist.")
    else:
        return HttpResponseBadRequest(f"400 Bad Request: Method '{request.method}' not allowed.")

@csrf_exempt
def product_list(request):
    print("2")
    if request.method == 'GET':
        products = list(Product.objects.values('id', 'name', 'price', 'available'))
        return JsonResponse(products, safe=False)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            price = data.get('price')
            available = data.get('available')

            if not name or price is None:
                return HttpResponseBadRequest(f"400 Bad Request: {"Missing 'name' or 'price' field in request body."}")

            if Decimal(str(price)) < 0:
                return HttpResponseBadRequest(f"400 Bad Request: {"'price' must be a positive value."}")

            product = Product(name=name,
            price=Decimal(str(price)), available=available)
            product.full_clean()
            product.save()
            return JsonResponse({'id': product.id,
                             'name': product.name,
                             'price': float(product.price),
                             'available': product.available},
                            status=201)

        except json.JSONDecodeError:
            return HttpResponseBadRequest(f"400 Bad Request: {"Invalid JSON format."}")
        except ValidationError as e:
            return HttpResponseBadRequest(f"Validation Error: {str(e)}")

    else:
        return HttpResponseBadRequest(f"400 Bad Request: Method '{request.method}' not allowed.")




