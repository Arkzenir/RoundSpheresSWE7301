#! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
import requests
from django.views.decorators.csrf import csrf_exempt
import stripe
from .models import ProductModel

# This test secret API key is a placeholder. Don't include personal details in requests with this key.
# To see your test secret API key embedded in code samples, sign in to your Stripe account.
# You can also find your test secret API key at https://dashboard.stripe.com/test/apikeys.
stripe.api_key = settings.STRIPE_SECRET_KEY


YOUR_DOMAIN = 'http://localhost:4242'

def loadCheckout(requests):
    return render(requests, 'checkout.html')



@csrf_exempt
def checkout(requests):
    
    try:
        checkout_session = stripe.checkout.Session.create(
            ui_mode='embedded',
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price_data': {
                        'currency': 'gbp',
                        'product_data': {'name': 'RoundSphere'},
                        'unit_amount': 15000
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            return_url='http://localhost:8000/checkout_success'
        )
    except Exception as e:
        return str(e)

    return JsonResponse({'clientSecret': checkout_session.client_secret})

def success(request):
    return render(request, 'success.html', {
        'message': 'Thank you for your purchase!',
    })


# def success(request):
#     print(request.POST)
#     return render(request, 'success')



# @csrf_exempt
# def checkout(request):
#     if request.method == "POST":
#         # Debug POST data
#         print("POST data:", request.POST)

#         try:
#             # Retrieve quantities from the form
#             quantities = {
#                 key.split('[')[1].split(']')[0]: int(value)
#                 for key, value in request.POST.items() if 'quantities' in key
#             }
#             print("Quantities: ", quantities)

#             # Filter out products with zero quantity
#             selected_products = {int(k): v for k, v in quantities.items() if v > 0}
#             if not selected_products:
#                 return JsonResponse({'error': 'No products selected'}, status=400)

#             # Prepare line items for Stripe
#             line_items = []
#             for product_id, quantity in selected_products.items():
#                 try:
#                     product = ProductModel.objects.get(id=product_id)
#                     line_items.append({
#                         'price_data': {
#                             'currency': 'gbp',
#                             'product_data': {
#                                 'name': product.name,
#                                 'images': [request.build_absolute_uri(product.image.url)] if product.image else [],
#                             },
#                             'unit_amount': int(product.price * 100),  # Convert to pence for Stripe
#                         },
#                         'quantity': quantity,
#                     })
#                 except ProductModel.DoesNotExist:
#                     return JsonResponse({'error': f'Product with ID {product_id} not found'}, status=400)

#             # Create a Stripe Checkout session
#             session = stripe.checkout.Session.create(
#                 payment_method_types=['card'],
#                 line_items=line_items,
#                 mode='payment',
#                 success_url=request.build_absolute_uri('/success/'),
#                 cancel_url=request.build_absolute_uri('/cancel/'),
#             )
#             # Redirect the user to Stripe's payment page
#             return JsonResponse({'url': session.url})
#         except Exception as e:
#             print(f"Error during checkout: {e}")
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Invalid request method'}, status=405)

# def success(request):
#     return render(request, 'success.html', {
#         'message': 'Thank you for your purchase!',
#     })