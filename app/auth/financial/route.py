from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
import logging
import stripe

auth_fin_bp = Blueprint('auth_fin', __name__)

logger = logging.getLogger('auth')

stripe.api_key = 'sk_test_51PRUTB04RXCS71J7NFOaCej5GKIL2vlfJsOzsUgmsIUPrsfD2u1vCCr8IgJNzhVwd1OUuU7qO0TQkXk3Igp4hCCf00cwJSBXve'

YOUR_DOMAIN = "http://127.0.0.1:5000"

# Enable Stripe logging
stripe.log = 'debug'


@auth_fin_bp.route('/checkout')
def checkout():
    cart = session.get('cart', [])
    return render_template('html/auth/financial/checkout.html', products=cart)


@auth_fin_bp.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    items = []
    cart = session.get('cart', [])
    for item in cart:
        print(item['price_id'])
        items.append({
            'price': item['price_id'],
            'quantity': 1,
        })
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=items,
            mode='payment',
            success_url=YOUR_DOMAIN + url_for('auth_fin.checkout_success'),
            cancel_url=YOUR_DOMAIN + url_for('auth_fin.checkout_cancel')
        )
        print(f"Checkout session created: {checkout_session.id}")
    except Exception as e:
        print(f"Error creating checkout session: {str(e)}")
        return jsonify(error=str(e)), 400

    return jsonify(sessionId=checkout_session.id)


@auth_fin_bp.route('/checkout/success')
def checkout_success():
    return render_template('html/auth/financial/checkout/success.html')


@auth_fin_bp.route('/checkout/cancel')
def checkout_cancel():
    return render_template('html/auth/financial/checkout/cancel.html')


@auth_fin_bp.route('/test-stripe', methods=['GET'])
def test_stripe():
    try:
        balance = stripe.Balance.retrieve()
        return jsonify(balance)
    except Exception as e:
        print(f"Error retrieving balance: {str(e)}")
        return str(e), 400
