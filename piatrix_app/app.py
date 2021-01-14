from flask import Flask, render_template, request

from .service_layer import currency_router

app = Flask(__name__)


@app.route('/')
def base_form():
    return render_template('index.html')


@app.route('/payment', methods=['POST'])
def payment():
    amount = request.form['value']
    currency = request.form['select']
    product_description = request.form['description']
    return currency_router(
        currency=currency,
        amount=amount,
        desc=product_description
    )


if __name__ == '__main__':
    app.run(debug=True)
