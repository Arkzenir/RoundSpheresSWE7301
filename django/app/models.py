from django.db import models 
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User

class membershipModel(models.Model):
    id = models.AutoField(primary_key=True)
    First_name = models.CharField(max_length=255)
    Last_name = models.CharField(max_length=255)
    User_name = models.CharField(max_length=255, unique=True)
    Email_address = models.EmailField(max_length=255, unique=True)
    Password = models.CharField(max_length=512)
    Date_added = models.DateTimeField(auto_now_add=True)
    image_url = models.ImageField(upload_to='images/', blank=True, null=True)
    is_admin = models.BooleanField(default=False)  # True for admins, False for customers
    is_active = models.BooleanField(default=False)  # Indicates if the user has verified their email
    verification_token = models.CharField(max_length=64, null=True, blank=True)  # Store the unique token

    class Meta:
        db_table = "Membership_tbl"

    def __str__(self):
        return f"{self.First_name} {self.Last_name} ({'Admin' if self.is_admin else 'Customer'})"



# class membershipModel(models.Model):
#     First_name = models.CharField(max_length=100)
#     Last_name = models.CharField(max_length=100)
#     User_name = models.CharField(max_length=100, unique=True)
#     Email_address = models.EmailField(unique=True)
#     Password = models.CharField(max_length=128)
#     is_active = models.BooleanField(default=False)  # Indicates if the user has verified their email
#     verification_token = models.CharField(max_length=64, null=True, blank=True)  # Store the unique token



class ProductModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.IntegerField(default=0)

    class Meta:
        db_table = "product_tbl"

    def __str__(self):
        return f"{self.First_name} {self.Last_name} ({'Admin' if self.is_admin else 'Customer'})"

class CartItem(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = "cart_item_tbl"


# class CartItem(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)

# class Cart(models.Model):
#     items = models.ManyToManyField(CartItem)
#     created_at = models.DateTimeField(auto_now_add=True)

#     @property
#     def total(self):
#         return sum(item.quantity * item.product.price for item in self.items.all())