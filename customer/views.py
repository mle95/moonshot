# /customer/views.py

import json
from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail
from .models import MenuItem, Category, OrderModel, CustomerModel, DriverModel, BiddingsModel

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.timezone import datetime
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')


class About(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):

        if request.user.username == 'admin':
           return render(request, 'customer/index.html')

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
              'VIP_status': this_customer.VIP_status,
              'orders_count': this_customer.orders_count
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
        VIP_status = 0
        orders_count = 0
        #initial funding to account sign-up
        balance = request.POST.get('balance')

        # create new entry in database table
        customer = CustomerModel.objects.create(
            name=name,
            email=email,
            phone=phone,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code,
            balance=balance,
            VIP_status = VIP_status,
            orders_count = orders_count
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


# Delivery guy bidding on orders
class Orders_Biddings(View):
    def get(self, request, *args, **kwargs):
        orders = OrderModel.objects.all()
        orders_biddings = BiddingsModel.objects.all()

        # pass this info to template 
        # total number of orders 
        context = {
            'orders': orders,
            'orders_biddings' : orders_biddings,
            'total_orders': len(orders)
        }

        return render(request, 'customer/orders_biddings.html', context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')

        orders = request.POST.getlist('orders[]')
        biddings = request.POST.getlist('biddings[]')
        customer_name = request.POST.getlist('customer_name[]')
        customer_email = request.POST.getlist('customer_email[]')
        customer_receipt = request.POST.getlist('customer_receipt[]')
        customer_street = request.POST.getlist('customer_street[]')
        customer_city = request.POST.getlist('customer_city[]')
        customer_state = request.POST.getlist('customer_state[]')
        customer_zip_code = request.POST.getlist('customer_zip_code[]')

        #debug info
        #if orders:
        #   print("there are orders")
        #if biddings:
        #   print("there are bids ")

        # biddings counting variable
        k = 0
        for bid in biddings:
          if k >= len(orders):
             break;   # no more biddings, terminate this for-loop
          try: 
             this_bid = BiddingsModel.objects.get(driver_email__exact=request.user.email, order_id__exact=orders[k])
             print("post() update entry _____________")
             length = len(bid)
             if length > 0:
                this_bid.delivery_price = int(bid)
                this_bid.customer_receipt = customer_receipt[k]
                this_bid.customer_email = customer_email[k]
                this_bid.customer_name = customer_name[k]
                this_bid.customer_street = customer_street[k]
                this_bid.customer_city = customer_city[k]
                this_bid.customer_state = customer_state[k]
                this_bid.customer_zip_code = customer_zip_code[k]
                this_bid.save()
                print ("save() update biddings")
                k += 1

          except ObjectDoesNotExist: 
             print("post() new entry____")
             length = len(bid)
             if length > 0:
                this_bid = BiddingsModel.objects.create(
                            order_id=orders[k],
                            driver_email=request.user.email,
                            delivery_price=int(bid),
                            customer_receipt=customer_receipt[k],
                            customer_email=customer_email[k],
                            customer_name=customer_name[k],
                            customer_street=customer_street[k],
                            customer_city=customer_city[k],
                            customer_state=customer_state[k],
                            customer_zip_code=customer_zip_code[k],

                )
                k += 1   # biddings counting variable

        return redirect('orders_biddings')

# all biddings (manager view)
class Orders_Biddings_All(View):
    def get(self, request, *args, **kwargs):
        #orders = OrderModel.objects.all()
        orders_biddings = BiddingsModel.objects.all().order_by('order_id')

        # pass this info to template 
        # total number of orders 
        context = {
            'orders_biddings' : orders_biddings,
        }

        return render(request, 'customer/orders_biddings_all.html', context)

    def post(self, request, *args, **kwargs):
        orders = request.POST.getlist('orders[]')
        biddings = request.POST.getlist('biddings[]')
        driver_email = request.POST.getlist('driver_email[]')
        driver_assigned = request.POST.getlist('assigned[]')
        customer_name = request.POST.getlist('customer_name[]')
        customer_receipt = request.POST.getlist('customer_receipt[]')
        customer_street = request.POST.getlist('customer_street[]')
        customer_city = request.POST.getlist('customer_city[]')
        customer_state = request.POST.getlist('customer_state[]')
        customer_zip_code = request.POST.getlist('customer_zip_code[]')

        # debug info  ##
        if orders:
           print("there are orders")
        if biddings:
           print("there are bids ")
        if driver_assigned:
           print("there are drivers assigned")
        # debug   ######

        driver_is_assigned = False

        # biddings counting variable
        k = 0
        for bid in biddings:
          if k >= len(orders):
             break;   # no more biddings, terminate this for-loop
          try: 
             #this_bid = BiddingsModel.objects.get(driver_email__exact=driver_email[k], order_id__exact=orders[k])
             this_bid = BiddingsModel.objects.get(order_id__exact=orders[k])
             print("post for-loop ")
             print("Driver assigned value")
             print(driver_assigned)
             if driver_assigned:
                if driver_assigned[k] == 'on':
                   driver_is_assigned = True

             length = len(bid)
             print ("==================================")
             print (driver_is_assigned)
             if length > 0:
                this_bid.delivery_price = int(bid)
                this_bid.customer_receipt = customer_receipt[k]
                #this_bid.driver_email = driver_email[k]
                this_bid.assigned=driver_is_assigned
                this_bid.customer_name = customer_name[k]
                this_bid.customer_street = customer_street[k]
                this_bid.customer_city = customer_city[k]
                this_bid.customer_state = customer_state[k]
                this_bid.customer_zip_code = customer_zip_code[k]
                this_bid.save()
                print ("save() update biddings")
                k += 1

          except ObjectDoesNotExist: 
             print("driver assigned value")
             print(driver_assigned)
             if driver_assigned[k] == 'on':
                driver_is_assigned = True

             length = len(bid)
             if length > 0:
                this_bid = BiddingsModel.objects.create(
                            order_id=orders[k],
                            delivery_price=int(bid),
                            #driver_email=driver_email[k],
                            assigned=driver_is_assigned,
                            customer_receipt=customer_receipt[k],
                            customer_name=customer_name[k],
                            customer_street=customer_street[k],
                            customer_city=customer_city[k],
                            customer_state=customer_state[k],
                            customer_zip_code=customer_zip_code[k],

                )
                k += 1   # biddings counting variable

        return redirect('orders_biddings_all')

delivery_fee = 5

class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        appetizers = MenuItem.objects.filter(category__name__contains='Appetizer')
        entres = MenuItem.objects.filter(category__name__contains='Entre')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')

        if request.user.username == 'admin':
           return render(request, 'customer/menu_display.html')

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

        price = price + delivery_fee

        this_customer = CustomerModel.objects.get(email__exact=request.user.email)
        context = {
            'items': order_items['items'],
            'price': price,
            'cur_balance': this_customer.balance,
            'warnings': this_customer.warnings,
            'email': this_customer.email,
            'home_delivery': home_delivery
        }

        this_customer.orders_count = this_customer.orders_count + 1


        if this_customer.orders_count >= 5:
            this_customer.VIP_status = 5
            this_customer.save()


        if this_customer.VIP_status > 0:
            price = price - (int(float(price) * 0.05)) - delivery_fee
        

        # if new order cost is more than account balance, reject this order now
        if price > this_customer.balance:
           this_customer.warnings += 1     #add one warning
           if this_customer.warnings >= 2:
              this_customer.VIP_status = 0    # downgrade account status to regular

           if this_customer.warnings >= 2 and this_customer.VIP_status == 0:
              this_customer.blacklist = True  # flag this account to blacklist

           #update customer profile in the database MySQL
           this_customer.save()
           return render(request, 'customer/order-reject.html', context)

        # create new food order entry in database table
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

        if price > 0:
           return redirect('order-confirmation', pk=order.pk)
        else:
           return redirect('order')


#receipt for food order
class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):

        order = OrderModel.objects.get(pk=pk)

        this_customer = CustomerModel.objects.get(email__exact=order.email)
        this_customer.balance -= order.price
        this_customer.orders_count += 1

        # generate warnings here if orders cost exceed current balance


        if this_customer.orders_count % 3 == 0:
           this_customer.delivery_fee = 0
        this_customer.save()


        # if this_customer.delivery_fee == 0:
        #    delivery_fee = 0

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
            'home_delivery': order.home_delivery,
            'delivery_fee':delivery_fee,
            'VIP_status':this_customer.VIP_status,
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
