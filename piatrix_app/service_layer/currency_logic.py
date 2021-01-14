from flask import redirect, render_template

from piatrix_app.service_layer.client import Client


def currency_router(currency, amount, desc):
    currency_funcs = {
        'usd': usd_payment,
        'eur': eur_payment,
        'rub': rub_payment
    }
    return currency_funcs[str(currency)](currency, amount, desc)


def eur_payment(currency, amount, desc):
    client = Client()
    sign = client.get_sign(currency, str(amount))
    inputs_dict = {
        'amount': amount,
        'currency': client.currency_values[currency],
        'shop_id': client.shop_id,
        'sign': sign,
        'shop_order_id': client.shop_order_id,
        'description': desc
    }
    return render_template(
        'payment_form.html',
        url='https://pay.piastrix.com/ru/pay',
        inputs_dict=inputs_dict,
        method='POST'
    )


def usd_payment(currency, amount, desc):
    client = Client()
    sign = client.get_sign(currency, str(amount), type_of_payment='bill')
    response = client.send_request(
        method='POST',
        url='https://core.piastrix.com/bill/create',
        data={
            'shop_id': client.shop_id,
            'shop_amount': amount,
            'shop_currency': client.currency_values[currency],
            'payer_currency': client.currency_values[currency],
            'description': desc,
            'shop_order_id': client.shop_order_id,
            'sign': sign
        }
    )
    url = response.json()['data']['url']
    return redirect(url)


def rub_payment(currency, amount, desc):
    client = Client()
    sign = client.get_sign(currency, str(amount), type_of_payment='invoice')
    response = client.send_request(
        method='POST',
        url='https://core.piastrix.com/invoice/create',
        data={
            'shop_id': client.shop_id,
            'amount': amount,
            'currency': client.currency_values[currency],
            'payway': client.payway,
            'description': desc,
            'shop_order_id': client.shop_order_id,
            'sign': sign
        }
    )
    print(response.json())
    url = response.json()['data']['url']
    return redirect(url)
