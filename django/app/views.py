from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import membershipModel, ProductModel
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import membershipModel, ProductModel



def home(request):
    # Fetch all products from the database
    products = ProductModel.objects.all()
    
    # Fetch user information from the session
    first_name = request.session.get('first_name', None)
    last_name = request.session.get('last_name', None)
    is_admin = request.session.get('is_admin', None)
    
    # Render the template with the products and user information
    return render(request, "home.html", {
        "products": products,
        "first_name": first_name,
        "last_name": last_name,
        "is_admin": is_admin
    })

def login(request):
    return render(request, 'login.html')

def register(request):
    data = request.GET
    message = data.get('message', '') 
    return render(request, "register.html", { "message": message })

def adminrecords(request):
    data = request.GET
    message = data.get('message', '')

    records= membershipModel.objects.all()
    return render(request, "adminrecords.html", {"records": records, "message": message })

def adminproducts(request):
    data = request.GET
    message = data.get('message', '')

    records= ProductModel.objects.all()
    return render(request, "adminproducts.html", {"records": records, "message": message })

def adminprofile(request):
    try:
        data = request.GET
        id = data['id']
        record= membershipModel.objects.get(id=id)
        return render(request, "adminprofile.html", {"profile": record })
    
    except:
        message = "record no longer exist for the selected id"
        return redirect('/adminrecords/?message=' + message)
    
def adminproductprofile(request):
    try:
        data = request.GET
        id = data['id']
        record= ProductModel.objects.get(id=id)
        return render(request, "adminproductprofile.html", {"profile": record })
    
    except:
        message = "record no longer exist for the selected id"
        return redirect('/adminproducts/?message=' + message)    
    
def adminupdate(request):
    data = request.GET
    id = data['id']
    message = data.get('message', '')
    record= membershipModel.objects.get(id=id)
    return render(request, 'adminupdate.html', {"profile": record, "message": message })  

def adminimg(request):
    data = request.GET
    id = data['id']
    message = data.get('message', '')
    return render(request, "adminprofileIMG.html", {"id": id, "message": message } )  

def adminproductimg(request):
    data = request.GET
    id = data['id']
    message = data.get('message', '')
    return render(request, "adminproductIMG.html", {"id": id, "message": message } )  


def delete(request):

    try:
        data = request.GET
        id = data['id']
        message = "Record has been deleted successfully"
        record= membershipModel.objects.get(id=id)
        record.delete()
        return redirect('/adminrecords/?message=' + message)

    except:
        message = "Record can not be deleted presently, please try again"
        return redirect('/adminrecords/?message=' + message)


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('/')


def product_list(request):
    products = ProductModel.objects.all()
    return render(request, 'products.html', {'products': products})

# def cart(request):
#     data = request.GET
#     id = data.get('id')  # Use get to avoid the error if 'id' is missing
#     message = data.get('message', '')
#     if not id:
#         # Handle the case where id is missing
#         return render(request, "cart.html", {"message": "Missing id parameter"})
#     return render(request, "cart.html", {"id": id, "message": message})

# def cart(request):
#     # Simulate a cart for demonstration (replace with your actual cart logic)
#     cart_items = [
#         {"name": "Product 1", "quantity": 2, "price": 20.00},
#         {"name": "Product 2", "quantity": 1, "price": 15.50},
#         {"name": "Product 3", "quantity": 3, "price": 10.00},
#     ]
    
#     # Calculate total price for each item and total cart amount
#     for item in cart_items:
#         item["total_price"] = item["quantity"] * item["price"]

#     cart_total = sum(item["total_price"] for item in cart_items)

#     return render(request, "cart.html", {"cart": cart_items, "cart_total": f"{cart_total:.2f}"})

def cart(request):
    if request.method == "POST":
        # Retrieve product quantities from the form
        quantities = request.POST.dict()  # Get all submitted form data as a dictionary
        selected_items = []

        for product_id, quantity in quantities.items():
            if product_id.startswith("quantities["):  # Filter form fields for quantities
                product_id = product_id.replace("quantities[", "").replace("]", "")  # Extract product ID
                quantity = int(quantity)
                if quantity > 0:  # Only include products with quantities > 0
                    product = get_object_or_404(ProductModel, id=product_id)
                    total_price = product.price * quantity
                    selected_items.append({
                        'name': product.name,
                        'quantity': quantity,
                        'price': product.price,
                        'total_price': total_price,
                    })

        # Calculate cart total
        cart_total = sum(item['total_price'] for item in selected_items)

        return render(request, "cart.html", {"cart": selected_items, "cart_total": f"{cart_total:.2f}"})
    
    return render(request, "cart.html", {"cart": [], "cart_total": "0.00"})


def checkout(request):
    print("seyi")
    data = request.GET
    # id = data['id']
    message = data.get('message', '')
    return render(request, "checkout.html", {"id": id, "message": message } )  



# def checkout(request):
#     if request.method == 'POST':
#         quantities = request.POST.getlist('quantities[]')  # or similar, depending on your form
#         # Process the checkout data, e.g., calculate totals, create an order, etc.
        
#         # Dummy response: if checkout is successful, redirect to a payment URL
#         return JsonResponse({'url': '/checkout/'})

#     # GET request handling, if needed
#     return render(request, "checkout.html")


def checkout_success(request):
    # Clear the cart session
    request.session['cart'] = []
    return render(request, 'checkout_success.html', {"message": "Payment successful!"})

def checkout_cancel(request):
    return render(request, 'checkout_cancel.html', {"message": "Payment canceled."})



# def checkout_success(request):
#     return render(request, "success.html")

# def checkout_cancel(request):
#     return render(request, "cancel.html")




# Create your views here.
