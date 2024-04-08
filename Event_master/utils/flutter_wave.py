import traceback

import requests
import json
import environ
env = environ.Env()



class CreatePayment(object):

    @staticmethod
    def make_payment(payment_object):
       try:
           headers = {
               "Authorization": f'Bearer {env("FLUTTERWAVE_SECRET_KEYS")}',
               'Content-Type': 'application/json',
           }

           payment_data = {
               # "public_key": "FLWPUBK_TEST-783b7271418cb678ae366af408ad8551-X",
               "encryption_key": env("FLUTTERWAVE_ENCRYPTION_KEYS"),
               "tx_ref": payment_object['reference_number'],  # required
               "amount": payment_object['amount'],  # required
               "currency": "RWF",
               "redirect_url": payment_object["redirect_url"],  # required
               "payment_options": "card",  # required
               "customer": {  # required
                   "email": payment_object["customer_email"],
                   "phonenumber": payment_object['customer_phone'],
                   "name": payment_object["customer_name"]
               },
               "customizations": {  # required
                   "title": "Pay accounting master",
                   "description": "Pay Suscription on Accounting master",
                   "logo":""
               }
           }

           pay_response = requests.post(
               url="https://api.flutterwave.com/v3/payments",
               #    url="https://api.flutterwave.com/v3/charges?type=mobile_money_rwanda",
               data=json.dumps(payment_data),
               headers=headers
           )
           response = pay_response.json()
           print(response)
           if response['status'] == "success":
               return response
           return None
       except Exception as e:
           print(traceback.format_exc())
           return None
