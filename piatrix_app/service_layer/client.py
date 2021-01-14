import json
import random
from hashlib import sha256

import requests


class Client:
    shop_id = '5'
    secretKey = 'SecretKey01'
    payway = 'payeer_rub'
    shop_order_id = random.randint(1000, 1000000)
    currency_values = {
        'usd': 840,
        'rub': 643,
        'eur': 978
    }

    @staticmethod
    def send_request(method, url, data):
        print(data)
        response = requests.request(
            method=method,
            url=url,
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
        return response

    def get_sign(self, currency, amount, type_of_payment=None):
        values = [amount, str(self.currency_values[currency]), self.shop_id, str(self.shop_order_id)]
        print(values)
        if type_of_payment == 'invoice':
            values.insert(2, self.payway)
        if type_of_payment == 'bill':
            values.insert(0, str(self.currency_values[currency]))
        data = ':'.join(values) + self.secretKey
        print(data)
        result = sha256(data.encode()).hexdigest()
        return result
