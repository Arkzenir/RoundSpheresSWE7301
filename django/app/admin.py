from django.contrib import admin
from .models import ProductModel

@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    search_fields = ('name',)

# Register your models here.
