import json

import requests

SMS_SENDER_URL = 'https://im.smsclub.mobi/sms/send'
BEARER_PASSWORD = 'c_ULyiOKz8HhCjp'

def qwer2():


	data = {
		'phone': ['380668388587'],
		'message': 'My test message',
		'src_addr': 'BigSales'
	}

	headers = {
		'Authorization': 'Bearer ' + 'c_ULyiOKz8HhCjp',
		'Content-Type': 'application/json'
	}

	response = requests.post(SMS_SENDER_URL, data=json.dumps(data), headers=headers)

	if response.status_code == 200:
		print("SMS sent successfully!")
		print(response.text)
	else:
		print(f"Failed to send SMS. Status Code: {response.status_code}")
		print(response.text)


def send_user_code(text: str, user_phone: str):
	data = {'phone': [user_phone, ], 'message': text, 'src_addr': 'BigSales'}
	headers = {
		'Authorization': 'Bearer ' + BEARER_PASSWORD,
		'Content-Type': 'application/json'
	}

	response = requests.post(SMS_SENDER_URL, data=json.dumps(data), headers=headers)
	if response.status_code == 200:
		print("SMS sent successfully!")
		print(response.text)
	else:
		print(f"Failed to send SMS. Status Code: {response.status_code}")
		print(response.text)