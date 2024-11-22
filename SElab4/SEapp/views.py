from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from decimal import Decimal


def hello_world(request):
    return HttpResponse("Hello, World!")

@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        products = list(Product.objects.values('id',
        'name', 'price', 'available'))
        return JsonResponse(products, safe=False)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON data.")

        name = data.get('name')
        price = data.get('price')
        available = data.get('available')

        if name is None or price is None or available is None:
            return HttpResponseBadRequest("Missing required fields: name, price, and/or available.")

        try:
            product = Product(
                name=name,
                price=Decimal(str(price)),
                available=available
            )
            product.full_clean()
            product.save()
        except ValidationError as e:
            return HttpResponseBadRequest(f"Validation error: {e.messages}")

        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'available': product.available
            },
            status = 201
            )
    else:
        return JsonResponse({'error': 'Method not allowed for this endpoint.'}, status=405)

@csrf_exempt
def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("Product not found.")

    if request.method == 'GET':
        product = Product.objects.get(id=product_id)
        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'available': product.available
            }
            )
    elif request.method == 'PATCH':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON data.")

        if 'name' in data:
            product.name = data['name']
        if 'price' in data:
            try:
                product.price = Decimal(str(data['price']))
            except Exception:
                return HttpResponseBadRequest("Invalid price value.")
        if 'available' in data:
            product.available = data['available']

        try:
            product.full_clean()
            product.save()
        except ValidationError as e:
            return HttpResponseBadRequest(f"Validation error: {e.messages}")

        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'available': product.available
            }
            )
    else:
        return HttpResponseBadRequest("Invalid request method.")