from django.http import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from django.contrib import messages
from django.conf import settings
import razorpay

from app.forms import CustomerProfile, CustomerRegistrationForm
from .models import Cart, OrderPlaced, Payment, Product, Customer, Wishlist
from django.db.models import Count, Q

# Create your views here.
def home(request):
    total_item = 0
    user = request.user
    if user.is_authenticated:
        total_item = len(Cart.objects.filter(user = user))
    return render(request, 'app/home.html', locals())

def about(request):
    total_item = 0
    user = request.user
    if user.is_authenticated:
        total_item = len(Cart.objects.filter(user = user))
    return render(request, 'app/about.html', locals())

def contact(request):
    total_item = 0
    user = request.user
    if user.is_authenticated:
        total_item = len(Cart.objects.filter(user = user))
    return render(request, 'app/contact.html', locals())

def search(request):
    total_item = 0
    user = request.user
    if user.is_authenticated:
        total_item = len(Cart.objects.filter(user = user))
    query = request.GET["search"]
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request, 'app/search.html', locals())

class CategoryView(View):
    def get(self, request, val):
        total_item = 0
        user = request.user
        if user.is_authenticated:
            total_item = len(Cart.objects.filter(user = user))
        product = Product.objects.filter(category = val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, 'app/category.html', locals())
    
class CategoryTitle(View):
    def get(self, request, val):
        total_item = 0
        user = request.user
        if user.is_authenticated:
            total_item = len(Cart.objects.filter(user = user))
        product = Product.objects.filter(title = val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, 'app/category.html', locals())
    
class ProductDetail(View):
    def get(self, request, pk):
        total_item = 0
        product = Product.objects.get(pk = pk)
        user = request.user
        if user.is_authenticated:
            total_item = len(Cart.objects.filter(user = user))
        wishlist = Wishlist.objects.filter(product = product, user = user)
        return render(request, 'app/productdetail.html', locals())
    
class CustomerRegistrationView(View):
    def get(self, request):
        total_item = 0
        user = request.user
        if user.is_authenticated:
            total_item = len(Cart.objects.filter(user = user))
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', locals())
    
    def post(self, request):
        total_item = 0
        user = request.user
        if user.is_authenticated:
            total_item = len(Cart.objects.filter(user = user))
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations! User register successfuly!')
        else:
            messages.error(request, "Invalid input data")
        return render(request, 'app/customerregistration.html', locals())
    
class ProfileView(View):
    def get(self, request):
        total_item = 0
        user = request.user
        if user.is_authenticated:
            total_item = len(Cart.objects.filter(user = user))
        #customer = Customer.objects.filter(user = request.user)
        # if customer:
        #     return redirect('home')
        form = CustomerProfile()
        return render(request, 'app/profile.html', locals())

    def post(self, request):
        #print(request.POST)

        form = CustomerProfile(request.POST)
        if form.is_valid:
            #print(form)
            total_item = 0
            user = request.user
            if user.is_authenticated:
                total_item = len(Cart.objects.filter(user = user))
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user = user, name = name, locality = locality, city = city, mobile = mobile,
                           state = state, zipcode = zipcode)
            reg.save()
            messages.success(request, 'Congratulations! Profile save successfully')
        else:
            messages.error(request, "Invalid Input data")
        return render(request, 'app/profile.html', locals())

def address(request):
    total_item = 0
    user = request.user
    if user.is_authenticated:
        total_item = len(Cart.objects.filter(user = user))
    add = Customer.objects.filter(user = request.user)
    return render(request, 'app/address.html', locals())

class UpdateAddressView(View):
    def get(self, request, pk):
        total_item = 0
        user = request.user
        if user.is_authenticated:
            total_item = len(Cart.objects.filter(user = user))
        add = Customer.objects.get(pk = pk)
        form = CustomerProfile(instance=add)
        return render(request, 'app/updateAddress.html', locals())

    def post(self, request, pk):
        total_item = 0
        user = request.user
        if user.is_authenticated:
            total_item = len(Cart.objects.filter(user = user))
        form = CustomerProfile(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk = pk)
            add.user = request.user
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, 'Congratulations! Profile updated successfully')
        else:
            messages.error(request, "Invalid Input data")
        return redirect("address")

def add_to_cart(request):
    if request.user.is_authenticated:
        user = request.user
        product_id = request.GET.get('prod_id')
        product = Product.objects.get(id=product_id)
        cart = Cart.objects.filter(user = user, product = product)
        if cart:
            cart[0].quantity += 1
            cart[0].save()
        else:
            cart = Cart(user = user, product = product)
            cart.save()
        return redirect('show_cart')
    return redirect('login')

def show_cart(request):
    if request.user.is_authenticated:
        total_item = 0
        user = request.user
        total_item = len(Cart.objects.filter(user = user))
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        return render(request, 'app/add_to_cart.html', locals())
    return redirect('login')

class Checkout(View):
    def get(self, request):
        user = request.user
        total_item = len(Cart.objects.filter(user = user))
        add = Customer.objects.filter(user = user)
        cart_items = Cart.objects.filter(user = user)
        amount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            amount += value
        totalamount = amount + 40
        razoramount = int(totalamount) + 300
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount":razoramount, "currency": "INR", "receipt":"order_receipt_11"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == "created":
            payment = Payment(
                user = user,
                amount = totalamount,
                razorpay_order_id = order_id,
                razorpay_payement_status = order_status
            )
            payment.save()
        return render(request, 'app/checkout.html', locals())

def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    user = request.user
    total_item = len(Cart.objects.filter(user = user))
    customer = Customer.objects.get(id = cust_id)
    payment = Payment.objects.get(razorpay_order_id = order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    cart = Cart.objects.filter(user = user)
    for c in cart:
        OrderPlaced(user = user, customer = customer, product = c.product, quantity = c.quantity, payment = payment).save()
        c.delete()

    return redirect('orders')

def orders(request):
    order_placed = OrderPlaced.objects.filter(user = request.user)
    user = request.user
    total_item = len(Cart.objects.filter(user = user))
    return render(request, 'app/orders.html', locals())


def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET.get("prod_id")
        user = request.user
        total_item = len(Cart.objects.filter(user = user))
        product = Product.objects.get(id = prod_id)
        c = Cart.objects.get(user = user, product = product)
        c.quantity += 1
        c.save()
        cart = Cart.objects.filter(user = user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount += value
        totalamount = amount + 40
        #print(prod_id)
        data = {
            'quantity' : c.quantity,
            'amount' : amount,
            'totalamount' : totalamount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET.get("prod_id")
        user = request.user
        product = Product.objects.get(id = prod_id)
        c = Cart.objects.get(user = user, product = product)
        c.quantity -= 1
        c.save()
        cart = Cart.objects.filter(user = user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount += value
        totalamount = amount + 40
        #print(prod_id)
        data = {
            'quantity' : c.quantity,
            'amount' : amount,
            'totalamount' : totalamount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET.get("prod_id")
        user = request.user
        product = Product.objects.get(id = prod_id)
        c = Cart.objects.get(user = user, product = product)
        c.delete()
        cart = Cart.objects.filter(user = user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount += value
        totalamount = amount + 40
        #print(prod_id)
        data = {
            'amount' : amount,
            'totalamount' : totalamount
        }
        return JsonResponse(data)
    
