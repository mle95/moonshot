# /customer/views.py

import json
from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail
from .models import MenuItem, Category, OrderModel, CustomerModel, DriverModel

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.timezone import datetime
from decimal import Decimal


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')


class About(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
           this_customer = CustomerModel.objects.get(email__exact=request.user.email)

           orders = OrderModel.objects.filter(email__exact=this_customer.email)

           total_spending = 0
           # loop through the orders to calculate cumulative total amount
           for order in orders:
               total_spending += order.price

           context = {
              'pk': this_customer.pk,
              'orders': orders,
              'email': this_customer.email,
              'phone': this_customer.phone,
              'street': this_customer.street,
              'city': this_customer.city,
              'state': this_customer.state,
              'zip_code': this_customer.zip_code,
              'balance': this_customer.balance,
              'warnings': this_customer.warnings,
              'total_spending': total_spending,
              'VIP_status': this_customer.VIP_status
           }

        return render(request, 'customer/about.html', context)


    def post(self, request, *args, **kwargs):
        funding = request.POST.get('funding')

        if request.user.is_authenticated:
           this_customer = CustomerModel.objects.get(email__exact=request.user.email)
           #update new funding (add more money)
           this_customer.balance += Decimal(funding)
           this_customer.save()

        return redirect('about')

    def test_func(self):
        return self



class Menu_Display(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/menu_display.html')

#new customer sign-up
class Customer_Info(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/customer_info.html')

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        #initial funding to account sign-up
        balance = request.POST.get('balance')

        customer = CustomerModel.objects.create(
            name=name,
            email=email,
            phone=phone,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code,
            balance=balance,
            orders_count=0
        )

        context = {
            'email': email,
            'balance': balance
        }

        return redirect('order')

# Delivery guy sign-up
class Driver_Info(View):
    def get(self, request, *args, **kwargs):
        orders = OrderModel.objects.all()

        # pass this info to template 
        # total number of orders 
        context = {
            'orders': orders,
            'total_orders': len(orders)
        }

        return render(request, 'customer/orders_biddings.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')

        customer = DriverModel.objects.create(
            name=name,
            email=email,
            phone=phone,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code,
            orders_count=0
        )

        context = {
            'email': email,
        }

        return redirect('orders_biddings')



class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        appetizers = MenuItem.objects.filter(category__name__contains='Appetizer')
        entres = MenuItem.objects.filter(category__name__contains='Entre')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')

        #customers = CustomerModel.objects.all()
        if request.user.is_authenticated:
           this_customer = CustomerModel.objects.get(email__exact=request.user.email)

        # pass into context
        if request.user.is_authenticated:
           context = {
            'appetizers': appetizers,
            'entres': entres,
            'desserts': desserts,
            'drinks': drinks,
            'this_customer': this_customer
           }
        else:
           context = {
            'appetizers': appetizers,
            'entres': entres,
            'desserts': desserts,
            'drinks': drinks,
           }

        # render the template
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        home_delivery = request.POST.get('home_delivery')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price,
                'ratings': menu_item.ratings
            }

            order_items['items'].append(item_data)

        price = 0
        item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            phone=phone,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code,
            home_delivery=home_delivery,
        )
        order.items.add(*item_ids)

        # After everything is done, send confirmation email to the user
        body = ('Thank you for your order! Your food is being made and will be delivered soon!\n'
                f'Your total: {price}\n'
                'Thank you again for your order!')

        send_mail(
            'Thank You For Your Order!',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )

        context = {
            'items': order_items['items'],
            'price': price,
            'home_delivery': home_delivery
        }

        if price > 0:
           return redirect('order-confirmation', pk=order.pk)
        else:
           return redirect('order')


class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):

        order = OrderModel.objects.get(pk=pk)

        this_customer = CustomerModel.objects.get(email__exact=order.email)
        #cur_balance = this_customer.balance - order.price
        this_customer.balance -= order.price
        this_customer.orders_count += 1

        # generate warnings here if orders cost exceed current balance


        if this_customer.orders_count % 3 == 0:
           this_customer.delivery_fee = 0
        this_customer.save()

        delivery_fee = 5
        if this_customer.VIP_status:
           delivery_fee = 0

        if this_customer.delivery_fee == 0:
           delivery_fee = 0

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
            'name': order.name,
            'email': order.email,
            'phone': order.phone,
            'street': order.street,
            'city': order.city,
            'state': order.state,
            'zip_code': order.zip_code,
            'delivery_fee':delivery_fee,
            'cur_balance': this_customer.balance
        }

        return render(request, 'customer/order_confirmation.html', context)

    def post(self, request, pk, *args, **kwargs):
        data = json.loads(request.body)

        if data['isPaid']:
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()

        return redirect('payment-confirmation')


class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')


class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        # get the current date
        today = datetime.today()
        orders = OrderModel.objects.all()

        # loop through the orders and add the price value
        total_revenue = 0
        for order in orders:
            total_revenue += order.price

        # pass total number of orders and total revenue into template
        context = {
            'orders': orders,
            'total_revenue': total_revenue,
            'total_orders': len(orders)
        }

        return render(request, 'customer/dashboard.html', context)

    def test_func(self):
        return self
