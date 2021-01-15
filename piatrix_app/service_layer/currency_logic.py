import logging

from flask import redirect, render_template

from piatrix_app import app
from piatrix_app.service_layer.shop import Shop


def currency_router(currency, amount, desc):
    """
    Use for route functional vie currency
    :return: render template or redirect
    """
    try:
        currency_funcs = {
            'usd': usd_payment,
            'eur': eur_payment,
            'rub': rub_payment
        }
        return currency_funcs[str(currency)](currency, amount, desc)
    except ValueError:
        return f'Your amount: "{amount}" has incorrect value for this operation'


def eur_payment(currency, amount, desc):
    shop = Shop()
    sign = shop.get_sign(currency, str(amount))
    inputs_dict = {
        'amount': amount,
        'currency': shop.currency_values[currency],
        'shop_id': shop.shop_id,
        'sign': sign,
        'shop_order_id': shop.shop_order_id,
        'description': desc
    }
    return render_template(
        'payment_form.html',
        url='https://pay.piastrix.com/ru/pay',
        inputs_dict=inputs_dict,
        method='POST'
    )


def usd_payment(currency, amount, desc):
    shop = Shop()
    sign = shop.get_sign(currency, str(amount), type_of_payment='bill')
    response = shop.send_request(
        method='POST',
        url='https://core.piastrix.com/bill/create',
        data={
            'shop_id': shop.shop_id,
            'shop_amount': amount,
            'shop_currency': shop.currency_values[currency],
            'payer_currency': shop.currency_values[currency],
            'description': desc,
            'shop_order_id': shop.shop_order_id,
            'sign': sign
        }
    )
    url = response.json()['data']['url']
    return redirect(url)


def rub_payment(currency, amount, desc):
    if float(amount) < 10.0:
        logging.error('Not correct amount value for this operation!')
        raise ValueError
    shop = Shop()
    sign = shop.get_sign(currency, str(amount), type_of_payment='invoice')
    response = shop.send_request(
        method='POST',
        url='https://core.piastrix.com/invoice/create',
        data={
            'shop_id': shop.shop_id,
            'amount': amount,
            'currency': shop.currency_values[currency],
            'payway': shop.payway,
            'description': desc,
            'shop_order_id': shop.shop_order_id,
            'sign': sign
        }
    )
    response_data = response.json()['data']
    inputs_dict = {
        'ac_account_email': response_data['data']['ac_account_email'],
        'ac_sci_name': response_data['data']['ac_sci_name'],
        'ac_amount': response_data['data']['ac_amount'],
        'ac_currency': response_data['data']['ac_currency'],
        'ac_order_id': response_data['data']['ac_order_id'],
        'ac_sign': response_data['data']['ac_sign'],
        'ac_sub_merchant_url': response_data['data']['ac_sub_merchant_url'],

    }
    return render_template(
        'payment_form.html',
        inputs_dict=inputs_dict,
        method='POST',
        url=response_data['url']
    )
