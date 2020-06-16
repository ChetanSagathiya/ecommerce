from celery import shared_task
from django.core.mail import send_mail
import json
from django.core import serializers

@shared_task
def order_status_confirm(email):
	send_mail(
		'Karma Order Status',
		'''your order has been successfully Accepted!!

Thank You.
Team Karma
		''',
		'chetuu.018@gmail.com',
		[email],
		)
	return None

@shared_task
def order_status_cancel(email):
	send_mail(
		'Karma Order Status',
		'''your order has been Declined Due to Insufficient Stock!!!
Please Reorder After Some Time.
		
Thank You.
Team Karma
		''',
		'chetuu.018@gmail.com',
		[email],
		)
	return None