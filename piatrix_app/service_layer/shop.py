import json
import random
from hashlib import sha256

import requests


class Shop:
    shop_id = '5'
    secretKey = 'SecretKey01'
    payway = 'advcash_rub'
    shop_order_id = str(random.randint(1000, 1000000))
    currency_values = {
        'usd': '840',
        'rub': '643',
        'eur': '978'
    }

    @staticmethod
    def send_request(method, url, data):
        response = requests.request(
            method=method,
            url=url,
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
        return response

    def get_sign(self, currency, amount, type_of_payment=None):
        values = [amount, self.currency_values[currency], self.shop_id, self.shop_order_id]
        if type_of_payment == 'invoice':
            values.insert(2, self.payway)
        if type_of_payment == 'bill':
            values.insert(0, str(self.currency_values[currency]))
        data = ':'.join(values) + self.secretKey
        result = sha256(data.encode()).hexdigest()
        return result
