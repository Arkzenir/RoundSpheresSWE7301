"""
URL configuration for roundsphere project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from app import views as app
from app import formview as appview
from app import server
# from app.views import create_checkout_session


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', app.home),
    # path('login/', app.login),
    path('register/', app.register),
    path('registration/', appview.registration),
    path('adminrecords/', app.adminrecords),
    path('adminproducts/', app.adminproducts),
    path('adminprofile/', app.adminprofile),
    path('adminproductprofile/', app.adminproductprofile),
    path('adminupdate/', app.adminupdate),
    path('updaterecord/', appview.updaterecord),
    path('adminimg/', app.adminimg),
    path('adminproductimg/', app.adminproductimg),
    path('uploadimg/', appview.uploadimg),
    path('uploadproductimg/', appview.uploadproductimg),
    path('delete/', app.delete),
    # path('login/', app.login),
    path('login/', appview.login_view,name='login'),
    path('logout/', app.logout_view, name='logout'),
    # path('checkout', server.loadCheckout, name='checkout'),
    path('cart/', app.cart, name='cart'),
    path('create-checkout-session/', appview.create_checkout_session, name='create_checkout_session'),
    path('success', server.success, name='success'),
    # path('loadCheckout', server.checkout, name='loadCheckout'),
    path('', app.product_list, name='product_list'),
    path('add-to-cart/', appview.add_to_cart, name='add_to_cart'),
    # path('cart/', appview.cart_view, name='cart'),
    # path('checkout/', appview.checkout, name='checkout'),
    path('checkout_success/', app.checkout_success, name='checkout_success'),
    path('cancel/', app.checkout_cancel, name='checkout_cancel'),
    path('verify-email/<str:token>/', appview.verify_email, name='verify_email'),


]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns() 