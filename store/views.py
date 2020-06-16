from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as Login, logout as Logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import random
from django.core import serializers
from .task import order_status_confirm, order_status_cancel
# Create your views here.

def store(request):
	if request.user.is_authenticated:
		customer, completed = Customer.objects.get_or_create(name = request.user.username)
		customer.user = request.user
		customer.save()
		order, completed = Order.objects.get_or_create(customer=customer, completed	=False)
	products = Product.objects.all()
	context = {'products': products, 'order':order}
	return render(request, 'store/store.html', context)

def login(request):
	if request.method== 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			Login(request, user)
			return redirect('/')
		else:
			messages.error(request,"Invalid UserName and password")
	return render(request, 'store/login.html')

@login_required
def logout(request):
	Logout(request)
	return redirect('/')

def register(request):
	if request.method== 'POST':
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		confirm_password = request.POST['confirm_password']
		if password == confirm_password:
			if User.objects.filter(username=username).exists():
				messages.error(request, "UserName Already Taken!!!")
			elif User.objects.filter(email=email).exists():
					messages.error(request, "Email Already Taken!!!")
			user = User.objects.create_user(username=username, email=email, password=password)
			user.save()
			Login(request, user)
			return redirect('/')
	return render(request, 'store/register.html')

@login_required
def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, completed = Order.objects.get_or_create(customer=customer, completed	=False)
		items = order.orderitem_set.all()
	context = {'items':items, 'order':order}
	return render(request, 'store/cart.html', context)

@login_required
def add_to_cart(request):
	customer = request.user.customer
	productId = request.GET['productId']
	product = Product.objects.get(id=productId)
	order, completed = Order.objects.get_or_create(customer=customer, completed=False)
	
	if product.total_qty_available <= 0 and request.GET['action'] == 'add':
		product.total_qty_available = 0
		product.save()

	if request.GET['action'] == 'None':
		orderitem, completed = OrderItem.objects.get_or_create(order=order, product=product, quantity=1)
		product.total_qty_available -= 1
		product.save()
	
	elif request.GET['action'] == 'add':
		orderitem, completed = OrderItem.objects.get_or_create(order=order, product=product)
		orderitem.quantity += 1
		product.total_qty_available -= 1
		orderitem.save()
		product.save()
		
	elif request.GET['action'] == 'remove':
		orderitem, completed = OrderItem.objects.get_or_create(order=order, product=product)
		orderitem.quantity -= 1
		product.total_qty_available += 1
		product.save()
		orderitem.save()

		if orderitem.quantity <= 0:
			orderitem.delete()
			orderitems.save()
	return JsonResponse("this is working", safe=False)

def search(request):
	search_query = request.GET.get('search_input')
	product_name = Product.objects.filter(name__icontains=search_query)
	product_price = Product.objects.filter(price__icontains=search_query)
	products_filter = product_name.union(product_price)
	context = {'products_filter':products_filter}
	return render(request, 'store/store.html', context)

@login_required
def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, completed = Order.objects.get_or_create(customer=customer, completed	=False)
		items = order.orderitem_set.all()
	context = {'items':items, 'order': order}
	return render(request, 'store/checkout.html', context)

@login_required
def complete_order(request):
	transaction_id = f'{random.randrange(1, 10**10):03}'
	if request.user.is_authenticated:
		customer = request.user.customer
		order, completed = Order.objects.get_or_create(customer=customer, completed=False)
	
	order.transaction_id = transaction_id
	shipping_obj = ShippingAddress.objects.create(
		customer = customer,
		order = order,
		name = request.POST.get('fullname'),
		phone_no = request.POST.get('number'),
		address = request.POST.get('address'),
		city = request.POST.get('city'),
		state = request.POST.get('state'),
		zipcode = request.POST.get('zip'),
		)
	if shipping_obj is not None:
		messages.success(request, "Order is Placed Successfully!!!! Thank You For Shopping!")
		order.completed = True
		order.save()
		orderitems = order.orderitem_set.all()
		product = [products.product.total_qty_available for products in orderitems]
		available_products = [qty for qty in product if qty<=0 ]
		email = customer.user.email
		if len(available_products) > 0:
			order_status_cancel.delay(email)
		if len(available_products) <= 0:
			order_status_confirm.delay(email)
		return redirect('/')
	return JsonResponse('Order Completed', safe=False)



