from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
	name = models.CharField(max_length=50, null=True)

class Product(models.Model):
	name = models.CharField(max_length=250, null=True)
	price = models.FloatField()
	total_qty_available = models.IntegerField(default=0)
	image = models.ImageField(null=True, blank=True, upload_to='')

	def __str__(self):
		return self.name


class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)	
	date_ordered = models.DateTimeField(auto_now_add=True)
	completed = models.BooleanField(default=False, null=True, blank=True)
	transaction_id = models.CharField(max_length=20, null=True)

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([items.get_item_total for items in orderitems])
		return total

	@property
	def get_cart_quantity(self):
		orderitems = self.orderitem_set.all()
		quantity = sum([items.quantity for items in orderitems])
		return quantity
	
	@property
	def get_cart_total_gst(self):
		orderitems = self.orderitem_set.all()
		total = sum([items.get_item_total for items in orderitems])
		return total + (total/100)*18

	def __str__(self):
		return str(self.id)


class OrderItem(models.Model): 
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)	
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.product)
	@property
	def get_item_total(self):
		total = self.quantity * self.product.price
		return total

class Coupon(models.Model):
	name = models.CharField(max_length=10)
	value = models.IntegerField()

	def __str__(self):
		return self.name

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
	name = models.CharField(max_length=200, null=True, blank=True)
	phone_no = models.IntegerField(null=True, blank=True)
	address =  models.CharField(max_length=250, null=True, blank=True)
	city = models.CharField(max_length=50, null=True, blank=True)
	state = models.CharField(max_length=50, null=True, blank=True)
	zipcode = models.IntegerField(null=True, blank=True)