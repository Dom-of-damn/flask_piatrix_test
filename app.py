from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def base_form():
    return render_template('index.html')


@app.route('/payment', methods=['POST'])
def payment():
    price = request.form['value']
    currency = request.form['select']
    product_description = request.form['description']
    return currency_router(
        currency=currency,
        price=price,
        desc=product_description
    )


def currency_router(currency, price, desc):
    currency_funcs = {
        'usd': usd_payment,
        'eur': eur_payment,
        'rub': rub_payment

    }
    return currency_funcs[str(currency)](currency, price, desc)


def eur_payment():
    pass


def usd_payment():
    pass


def rub_payment():
    pass


if __name__ == '__main__':
    app.run(debug=True)
