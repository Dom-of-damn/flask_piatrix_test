from flask import Flask, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from piatrix_app.config import Config
from .service_layer import currency_router

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from piatrix_app.models import Payment


@app.route('/')
def base_form():
    return render_template('index.html')


@app.route('/payment', methods=['POST'])
def payment():
    """
    Use for implement payment methods and save payment data into database
    :return: render template or redirect, implement in currency logic
    """
    amount = request.form['value']
    currency = request.form['select']
    product_description = request.form['description']
    payment_record = Payment(currency, amount, product_description)
    db.session.add(payment_record)
    db.session.commit()
    return currency_router(
        currency=currency,
        amount=amount,
        desc=product_description
    )
