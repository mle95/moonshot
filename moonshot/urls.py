"""moonshot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from customer.views import Index, About, Menu_Display, Customer_Info, Order, OrderConfirmation, OrderPayConfirmation
from customer.views import Orders_Biddings, Orders_Biddings_All

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('customer/', include('customer.urls')),
    path('restaurant/', include('restaurant.urls')),
    path('', Index.as_view(), name='index'),
    path('about/', About.as_view(), name='about'),
    path('menu_display/', Menu_Display.as_view(), name='menu_display'),
    path('customer_info/', Customer_Info.as_view(), name='customer_info'),
    path('orders_biddings/', Orders_Biddings.as_view(), name='orders_biddings'),
    path('orders_biddings_all/', Orders_Biddings_All.as_view(), name='orders_biddings_all'),
    path('order/', Order.as_view(), name='order'),
    path('order-confirmation/<int:pk>', OrderConfirmation.as_view(), name='order-confirmation'),
    path('payment-confirmation/', OrderPayConfirmation.as_view(),  name='payment-confirmation'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
