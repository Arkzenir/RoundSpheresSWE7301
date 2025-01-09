from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse, JsonResponse
from .models import membershipModel, ProductModel
from django.core.files.storage import default_storage
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
import random, stripe
from django.conf import settings
from urllib.parse import urlencode
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
import json
from django.views.decorators.csrf import csrf_exempt






def registration(request):
    try:
        if request.method == "POST":
            form = request.POST
            
            # Check if the email or username already exists
            if membershipModel.objects.filter(Email_address=form['Email_address']).exists():
                message = "Email is already registered."
                return render(request, "register.html", {"message": message})
            
            if membershipModel.objects.filter(User_name=form['User_name']).exists():
                message = "Username is already taken."
                return render(request, "register.html", {"message": message})
            
            # Save user data but mark as inactive
            verification_token = get_random_string(32)  # Generate a unique token
            saveData = membershipModel.objects.create(
                First_name=form['First_name'],
                Last_name=form['Last_name'],
                User_name=form['User_name'],
                Email_address=form['Email_address'],
                Password=make_password(form['Password']),
                is_active=False,  # Mark user as inactive initially
                verification_token=verification_token
            )
            
            # Send verification email
            verification_link = request.build_absolute_uri(f"/verify-email/{verification_token}/")
            send_mail(
                subject="Verify Your Account",
                message=f"Hi {form['First_name']},\n\nPlease verify your account by clicking the link below:\n\n{verification_link}\n\nThank you!",
                from_email="noreply@example.com",
                recipient_list=[form['Email_address']],
                fail_silently=False,
            )
            
            message = "Registration successful! Please check your email to verify your account."
            return render(request, "register.html", {"message": message})
        else:
            message = "Invalid request."
            return render(request, "register.html", {"message": message})
    except Exception as error:
        message = f"Something went wrong. Error: {error}"
        return render(request, "register.html", {"message": message})



def verify_email(request, token):
    try:
        # Find the user with the given token
        user = get_object_or_404(membershipModel, verification_token=token, is_active=False)
        
        # Activate the user's account
        user.is_active = True
        user.verification_token = None  # Clear the token after verification
        user.save()
        
        return HttpResponse("Your email has been verified successfully. You can now log in.")
    except Exception as error:
        return HttpResponse(f"Verification failed. Error: {error}")


# def registration(request):
#     try:
#         if request.method == "POST":
#             form = request.POST
#             saveData = membershipModel.objects.create(
#             First_name = form['First_name'],
#             Last_name = form['Last_name'],
#             User_name = form['User_name'],
#             Email_address = form['Email_address'],
#             Password = make_password(form['Password']),
#             )
#             message = "Success"
#             return redirect('/../login', {"message": message })
            
#         else:
#             message = "INVALID request"
#             return render(request, "register.html", {"message": message })
#     except Exception as error:
#         message = "something went wrong, please try again. Error: "
#         print(error)
#         return render(request, "register.html", {"message": message })

def updaterecord(request):
    try:
        id = 0
        if request.method == "POST":
            form = request.POST
            id = form['id']
            record = membershipModel.objects.get(id=id)
            record.First_name = form['First_name']
            record.Last_name = form['Last_name']
            record.User_name = form['User_name']
            record.Email_address = form['Email_address']
            record.Password =  make_password(form['Password']),
            record.save()
            message = "profile updated successfully"
            return redirect('/adminrecords/?id=' + str(id) + '&message=' + message)

        else:
            message = "INVALID request"
            return redirect('/adminupdate/?message=' + message)
    except Exception as error:
        message = "something went wrong, please try again. Error: "+str(error)
        return redirect('/adminupdate/?message=' + message)


def uploadimg(request):
    try:
        if request.method == "POST":
            # Fetch the 'id' safely from POST data
            form = request.POST
            id = form.get('id')  # Use .get() to avoid KeyError

            if not id:
                raise ValueError("Membership ID is missing from the request.")

            # Safely fetch the 'image_url' file
            try:
                uploadedfile = request.FILES["image_url"]
            except MultiValueDictKeyError:
                raise ValueError("No image file provided in the request.")

            # Handle file upload
            location = "user/"
            getextension = uploadedfile.name.split('.')
            randomname = str(random.randint(1, 999999999999))
            filename = randomname + "." + getextension[-1]  # Use the last part as the file extension
            path = location + filename

            # Save the uploaded file
            default_storage.save(path, uploadedfile)
            getlocation = default_storage.url(path)

            # Update the membership record
            record = membershipModel.objects.get(id=id)
            record.image_url = getlocation  # Assuming 'image_url' is a field in the membershipModel
            record.save()

            # Success message
            message = "Success"
            return redirect(f'/adminimg/?id={id}&message={message}')
    except Exception as error:
        # Safely handle errors and ensure 'id' is set
        message = f"Something went wrong, please try again. Error: {error}"
        id = locals().get('id', 'unknown')  # Set 'id' to 'unknown' if not defined
        return redirect(f'/adminimg/?id={id}&message={message}')


def uploadproductimg(request):
    try:
        if request.method == "POST":
            # Safely fetch the 'id' from POST data
            form = request.POST
            id = form.get('id')  # Use get to avoid KeyError

            # Ensure 'id' exists
            if not id:
                raise ValueError("Product ID is missing from the request.")

            # Safely fetch the 'image' from FILES
            try:
                uploadedfile = request.FILES["image"]
            except MultiValueDictKeyError:
                raise ValueError("No image file provided in the request.")

            # Handle file upload
            location = "user/"
            getextension = uploadedfile.name.split('.')
            randomname = str(random.randint(1, 999999999999))
            filename = randomname + "." + getextension[-1]  # Use the last part as extension
            path = location + filename

            # Save the file
            default_storage.save(path, uploadedfile)

            # Update the product record
            record = ProductModel.objects.get(id=id)
            record.image = path  # Assign to the image field
            record.save()

            # Success message
            message = "Success"
            return redirect(f'/adminproductimg/?id={id}&message={message}')
    except Exception as error:
        # Handle any errors
        message = f"Something went wrong, please try again. Error: {error}"
        # Ensure 'id' is available before using it in the redirect
        id = id if 'id' in locals() else 'unknown'
        return redirect(f'/adminproductimg/?id={id}&message={message}')


        
def login_view(request):
    print("login_view called")  # Debug message

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)
        print(password)

        # Check if email and password are provided
        if not email or not password:
            messages.error(request, "Both email and password are required.")
            return redirect('/login/')

        try:
            # Retrieve user by email
            user = membershipModel.objects.get(Email_address=email)

            # Verify the password
            if check_password(password, user.Password):
                # Save session data
                request.session['user_id'] = user.id
                request.session['first_name'] = user.First_name
                request.session['last_name'] = user.Last_name
                request.session['is_admin'] = user.is_admin  # Add the admin status to the session
                messages.success(request, f"Welcome {user.First_name}!")
                return redirect('/')  # Redirect to the home page
            else:
                messages.error(request, "Invalid credentials. Please try again.")
                return redirect('/login/')
        except membershipModel.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('/login/')
    
    return render(request, "login.html")  # Render the login form


# Set the Stripe secret key

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request):
    if request.method == "POST":
        # Get the cart total and convert to cents
        cart_total = request.POST.get('cart_total', 0.00)
        cart_total = float(cart_total) * 100  # Convert to cents for Stripe

        # Debugging: Print cart_total
        print(f"Cart Total: {cart_total}")

        # Initialize an empty list for line items
        line_items = []

        # Debugging: Check if cart_items are being passed
        cart_items = request.POST.getlist('cart_items')
        print(f"Cart Items: {cart_items}")

        # If you have actual cart items, loop through them to construct the line items
        for item in cart_items:
            try:
                # Debugging: Check individual item data
                print(f"Processing item: {item}")
                
                # Split the cart item into name, price, and quantity
                product_name, product_price, quantity = item.split('|')
                product_price = float(product_price) * 100  # Convert to cents
                quantity = int(quantity)

                # Add line item to the list
                line_items.append({
                    'price_data': {
                        'currency': 'gbp',
                        'product_data': {
                            'name': product_name,
                        },
                        'unit_amount': int(product_price),  # price in cents
                    },
                    'quantity': quantity,
                })

                # Debugging: Print the line item being added
                print(f"Line item added: {line_items[-1]}")

            except Exception as e:
                print(f"Error processing item: {e}")
        
        # Debugging: Print all line items
        print(f"Line items: {line_items}")

        if not line_items:
            return JsonResponse({'error': 'No valid line items found.'}, status=400)

        try:
            # Create the Stripe Checkout session with the line_items
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,  # Pass the line_items list
                mode='payment',
                success_url=request.build_absolute_uri('/checkout_success/'),
                cancel_url=request.build_absolute_uri('/cart/'),
            )

            # Return the session ID in response
            return JsonResponse({'sessionId': session.id})

        except Exception as e:
            # Debugging: Log any errors when creating session
            print(f"Error creating Stripe session: {e}")
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Invalid request method.'}, status=400)



# def create_checkout_session(request):
#     if request.method == "POST":
#         print("Received POST request for checkout session") 
#         # Example: Get cart total from the form
#         cart_total = request.POST.get('cart_total', 0.00)
#         cart_total = float(cart_total) * 100  # Stripe expects amounts in cents/pennies
        
#         # Assuming cart items are passed correctly from the frontend
#         cart_items = request.POST.getlist('cart_items')  # Get cart items if needed for more details

#         # Create a list of line items
#         line_items = []
#         for item in cart_items:
#             product = get_object_or_404(ProductModel, id=item['product_id'])
#             line_items.append({
#                 'price_data': {
#                     'currency': 'gbp',
#                     'product_data': {
#                         'name': product.name,
#                     },
#                     'unit_amount': int(item['total_price'] * 100),  # Convert to cents
#                 },
#                 'quantity': item['quantity'],
#             })

#         try:
#             # Create Stripe Checkout Session with multiple line items
#             session = stripe.checkout.Session.create(
#                 payment_method_types=['card'],
#                 line_items=line_items,
#                 mode='payment',
#                 success_url=request.build_absolute_uri('/checkout_success/'),
#                 cancel_url=request.build_absolute_uri('/cart/'),
#             )

#             return JsonResponse({'sessionId': session.id})

#         except Exception as e:
#             return JsonResponse({'error': str(e)})

#     return JsonResponse({'error': 'Invalid request method.'}, status=400)







# stripe.api_key = settings.STRIPE_SECRET_KEY

# def checkout_view(request):
#     if request.method == "POST":
#         try:
#             # Retrieve items from the session or request data
#             cart_items = request.session.get('cart', [])
            
#             if not cart_items:
#                 return JsonResponse({'error': 'Cart is empty'}, status=400)
            
#             # Format items for Stripe
#             line_items = [
#                 {
#                     "price_data": {
#                         "currency": "usd",
#                         "product_data": {
#                             "name": item['name'],  # Product name
#                         },
#                         "unit_amount": int(item['price'] * 100),  # Convert to cents
#                     },
#                     "quantity": item['quantity'],  # Bulk quantities
#                 }
#                 for item in cart_items
#             ]
            
#             # Create a Checkout Session
#             checkout_session = stripe.checkout.Session.create(
#                 payment_method_types=['card'],
#                 line_items=line_items,
#                 mode='payment',
#                 success_url=request.build_absolute_uri('/checkout/success/'),
#                 cancel_url=request.build_absolute_uri('/checkout/cancel/'),
#             )
            
#             return JsonResponse({'id': checkout_session.id})
        
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

#     return render(request, "checkout.html")

# stripe.api_key = settings.STRIPE_SECRET_KEY

# def checkout(request):
#     if request.method == "POST":
#         # Print POST data for debugging
#         print("POST data:", request.POST)

#         # Retrieve 'quantities' from POST and ensure correct data structure
#         quantities = {key.split('[')[1].split(']')[0]: value for key, value in request.POST.items() if 'quantities' in key}
#         print("Quantities: ", quantities)

#         # Prepare the selected products based on quantities
#         selected_products = {int(k): int(v) for k, v in quantities.items() if int(v) > 0}

#         print("Selected Products: ", selected_products)  # Debugging

#         line_items = []
#         for product_id, quantity in selected_products.items():
#             try:
#                 product = ProductModel.objects.get(id=product_id)
#                 line_items.append({
#                     'price_data': {
#                         'currency': 'gbp',
#                         'product_data': {
#                             'name': product.name,
#                             'images': [request.build_absolute_uri(product.image.url)] if product.image else None,
#                         },
#                         'unit_amount': int(product.price * 100),  # Stripe accepts amounts in pence
#                     },
#                     'quantity': quantity,
#                 })
#             except ProductModel.DoesNotExist:
#                 continue

#         # If no valid line items, redirect to the cancel page
#         if not line_items:
#             return redirect('checkout_cancel')

#         # Create Stripe Checkout session
#         session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=line_items,
#             mode='payment',
#             success_url=request.build_absolute_uri('/success/'),
#             cancel_url=request.build_absolute_uri('/cancel/'),
#         )

#         # Redirect to Stripe Checkout
#         return redirect(session.url, code=303)

#     return render(request, "cart.html")

# stripe.api_key = settings.STRIPE_SECRET_KEY

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



def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))
        product = get_object_or_404(ProductModel, id=product_id)
    
        # Initialize cart in session if not already present
        if 'cart' not in request.session:
            request.session['cart'] = []

        cart = request.session['cart']

        # Check if product is already in cart
        for item in cart:
            if item['id'] == product.id:
                item['quantity'] += quantity
                break
        else:
            # Add new product to cart
            cart.append({
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'quantity': quantity
            })

        # Save cart back to session
        request.session['cart'] = cart
        messages.success(request, f"{quantity} {product.name}(s) added to cart!")
        return redirect('product_list')



# def add_to_cart(request):
#     if request.method == 'POST':
#         product_id = request.POST.get('product_id')
#         quantity = int(request.POST.get('quantity', 1))

#         product = get_object_or_404(Product, id=product_id)

#         if quantity > product.stock:
#             messages.error(request, "Not enough stock available.")
#             return redirect('product_list')

#         cart, _ = Cart.objects.get_or_create(id=request.session.get('cart_id', None))
#         cart_item, created = CartItem.objects.get_or_create(product=product)

#         if not created:
#             cart_item.quantity += quantity
#         else:
#             cart_item.quantity = quantity

#         cart_item.save()
#         cart.items.add(cart_item)
#         request.session['cart_id'] = cart.id

#         messages.success(request, f"{product.name} added to cart.")
#         return redirect('product_list')

# def cart_view(request):
#     cart = Cart.objects.filter(id=request.session.get('cart_id')).first()
#     return render(request, 'cart.html', {'cart': cart})