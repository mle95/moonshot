# /customer/views.py

import json
from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail
from .models import MenuItem, Category, OrderModel, CustomerModel

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.timezone import datetime


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')

class Info(View):
    def get(self, request, *args, **kwargs):
        customers = OrderModel.objects.all()

        context = {
            'customers': customers,
        }

        return render(request, 'customer/info.html', context)

class About(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk, *args, **kwargs):

        today = datetime.today()
        new_customer = CustomerModel.objects.get(pk=pk)

        orders = OrderModel.objects.filter(email__exact=new_customer.email)

        total_spending = 0

        # loop through the orders and find this customer info
        for order in orders:
            total_spending += order.price

        cur_balance  = new_customer.balance - total_spending
        #update database current balance
        #new_customer.balance = cur_balance
        #new_customer.save()

        context = {
            'pk': new_customer.pk,
            'orders': orders,
            'email': new_customer.email,
            'phone': new_customer.phone,
            'street': new_customer.street,
            'city': new_customer.city,
            'state': new_customer.state,
            'zip_code': new_customer.zip_code,
            'customer_balance': new_customer.balance,
            'balance': cur_balance,
            'total_spending': total_spending
        }


        return render(request, 'customer/about.html', context)


    def post(self, request, pk, *args, **kwargs):
        data = json.loads(request.body)

        return render(request, 'customer/menu_display.html')


    def test_func(self):
        return self



class Menu_Display(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/menu_display.html')


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
        balance = request.POST.get('balance')

        customer = CustomerModel.objects.create(
            name=name,
            email=email,
            phone=phone,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code,
            balance=balance
        )

        context = {
            'email': email,
            'balance': balance
        }

        return redirect('about', pk=customer.pk)




class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        appetizers = MenuItem.objects.filter(category__name__contains='Appetizer')
        entres = MenuItem.objects.filter(category__name__contains='Entre')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')

        customers = CustomerModel.objects.all()

        # pass into context
        context = {
            'appetizers': appetizers,
            'entres': entres,
            'desserts': desserts,
            'drinks': drinks,
            'customers': customers
        }

        # render the template
        return render(request, 'customer/order.html', context)

    #def post(self, request, pk, *args, **kwargs):
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        bidding = request.POST.get('bidding')

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
            name=name,
            email=email,
            phone=phone,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code,
            price=price,
            bidding=bidding

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
            'price': price
        }

        return redirect('order-confirmation', pk=order.pk)


class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        this_customer = CustomerModel.objects.get(email__exact=order.email)
        cur_balance = this_customer.balance - order.price
        this_customer.balance = cur_balance
        this_customer.save()

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
            'cur_balance': cur_balance
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
