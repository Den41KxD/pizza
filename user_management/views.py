from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import render, redirect

from sms_handler.views import send_user_code
from django.contrib.auth import authenticate, login
from user_management.models import User, UserLoginCode
import random


def get_random_code() -> str:
	random_number = random.randint(100000, 999999)
	return str(random_number)


def authentication(request):
	user = User.objects.get(phone=request.POST.get('phone_number'),
							user_code__login_code=request.POST.get('verification_code'))
	if user:
		login(request, user)
		return True
	else:
		return False


def get_and_send_code(request):
	phone_number = request.POST.get('phone_number')
	try:
		user = User.objects.get(phone=phone_number)
	except User.DoesNotExist:
		user = User.objects.create(phone=phone_number, username=phone_number)

	random_code = get_random_code()
	try:
		user_code = UserLoginCode.objects.get(user=user)
		user_code.login_code = random_code
		user_code.save()
	except UserLoginCode.DoesNotExist:
		user_code = UserLoginCode.objects.create(user=user, login_code=random_code)

	# send_user_code(text=f'Your code: {random_code}', user_phone=phone_number)

	return JsonResponse({'code': user_code.login_code, 'phone_number': phone_number}, status=200, safe=False)


def account_login(request: WSGIRequest):
	if authentication(request=request):
		return redirect('/')
	return JsonResponse({'error': '123'}, status=400, safe=False)
