import random
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from twilio.rest import Client
import random
from django.conf import settings

TWILIO_ACCOUNT_SID = 'AC8c69c0642fa4636f0dc340aba1d86e76'
TWILIO_AUTH_TOKEN = '633fb2d55f6db99d03aac9d735be708f'
TWILIO_PHONE_NUMBER = '+13158963891'



def send_verification_code():

    phone_number = '+380990504281'

    verification_code = ''.join(str(random.randint(0, 9)) for _ in range(6))
    # VerificationCode.objects.create(user=user, code=verification_code)

    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = twilio_client.messages.create(
        body=f'Ваш код подтверждения: {verification_code}',
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    print(message)
    return 'qwer'