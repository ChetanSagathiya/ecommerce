from django.urls import path
from . import views

urlpatterns = [
	path('', views.store, name='store'),
	path('checkout/', views.checkout, name="checkout"),
	path('cart/', views.cart, name="cart"),
	path('login/', views.login, name="login"),
	path('add_to_cart/', views.add_to_cart, name="tracking"),
	path('search/', views.search, name="search"),
	path('register/', views.register, name="register"),
	path('logout/', views.logout, name="logout"),
	path('complete_order/', views.complete_order, name="complete_order"),
]