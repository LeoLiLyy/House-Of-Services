import json
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_required, current_user
from datetime import datetime

service_bp = Blueprint('service', __name__)

# Use the correct path for your data.json file
DATA_FILE = os.path.join(os.path.dirname(__file__), '../../data.json')


def read_data():
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {'services': []}


def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)


@service_bp.route('/add_new_service', methods=['GET', 'POST'])
def add_new_service():
    services = read_data().get('services', [])
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        kind = request.form.get('type')
        service_category = request.form.get('service_category')
        location = request.form.get('location') if service_category == 'physical' else None
        price = request.form.get('price')
        subscription_price = request.form.get('subscription_price')
        repeat_cycle = request.form.get('repeat_cycle')
        email = request.form.get('email')
        provider = request.form.get('provider')
        image_url = request.form.get('image_url')

        new_service = {
            'id': len(services) + 1,
            'name': name,
            'description': description,
            'kind': kind,
            'service_category': service_category,
            'location': location,
            'price': price,
            'subscription_price': subscription_price,
            'repeat_cycle': repeat_cycle,
            'email': email,
            'provider': provider,
            'image_url': image_url,
            'date': datetime.now().strftime("%Y-%m-%d")
        }
        services.append(new_service)
        write_data({'services': services})
        flash('Service created successfully!', 'success')
        return redirect(url_for('service.find'))

    return render_template('html/service/add_new_service.html')


@service_bp.route('/services/<int:service_id>')
def view(service_id):
    services = read_data().get('services', [])
    service = next((s for s in services if s['id'] == service_id), None)
    return render_template('html/service/view.html', service=service)


@service_bp.route('/contact/<int:provider_id>')
def contact(provider_id):
    services = read_data().get('services', [])
    provider = next((s['provider'] for s in services if s['provider_id'] == provider_id), None)
    return render_template('html/service/contact.html', provider=provider)


@service_bp.route('/add_to_cart/<int:service_id>', methods=['POST'])
def add_to_cart(service_id):
    services = read_data().get('services', [])
    if 'cart' not in session:
        session['cart'] = []

    service = next((s for s in services if s['id'] == service_id), None)
    if service:
        session['cart'].append(service)
        session.modified = True
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Service not found'}), 404


@service_bp.route('/remove_from_cart/<int:service_id>', methods=['POST'])
def remove_from_cart(service_id):
    if 'cart' not in session:
        return jsonify({'error': 'Cart is empty'}), 400

    services = read_data().get('services', [])
    service = next((s for s in services if s['id'] == service_id), None)
    if service and service in session['cart']:
        session['cart'].remove(service)
        session.modified = True
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Service not found in cart'}), 404


@service_bp.route('/cart')
def view_cart():
    cart = session.get('cart', [])
    return render_template('html/service/cart.html', cart=cart)


@service_bp.route('/find')
def find():
    services = read_data().get('services', [])
    return render_template('html/service/find.html', services=services)


@service_bp.route('/host')
def host():
    return render_template('html/service/host.html')


# Initialize services data on module load
services = read_data().get('services', [])
