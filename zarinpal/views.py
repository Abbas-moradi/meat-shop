from django.views import View
from meatshop import settings
import requests
import json



ZP_API_REQUEST = f"https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = f"https://www.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://www.zarinpal.com/pg/StartPay/"

amount = 100000  # Rial / Required
description = "فروشگاه گوشت دامیران"  # Required
phone = '09126818407'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8080/zarinpal/verify/'


class Zarinpal(View):
    def get(self, request):
        data = {
                "MerchantID": settings.MERCHANT,
                "Amount": int(amount),
                "CallbackURL": CallbackURL,
                "Description": description,                                    
                "metadata": {"mobile": phone,"email": "info.test@gmail.com"},
            }
        
        data_main = json.dumps(data)
        print('#'*10, data_main)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        try:
            response = requests.post(ZP_API_REQUEST, data=data_main ,headers=headers, timeout=10)

            if response.status_code == 200:
                response = response.json()
                print(response, '#*'*20)
                if response['Status'] == 100:
                    print('ok')
                    # return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']}
                else:
                    print('nok')
                    # return {'status': False, 'code': str(response['Status'])}
            return response
        
        except requests.exceptions.Timeout:
            return {'status': False, 'code': 'timeout'}
        except requests.exceptions.ConnectionError:
            return {'status': False, 'code': 'connection error'}


class CallbackUrl(View):
    def post(self, request, authority):
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": amount,
            "Authority": authority,
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return {'status': True, 'RefID': response['RefID']}
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response