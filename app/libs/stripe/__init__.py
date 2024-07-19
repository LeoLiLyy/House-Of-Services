import stripe

stripe.api_key = "sk_test_51PRUTB04RXCS71J7NFOaCej5GKIL2vlfJsOzsUgmsIUPrsfD2u1vCCr8IgJNzhVwd1OUuU7qO0TQkXk3Igp4hCCf00cwJSBXve"


def create_product(p_name):
    p_re = stripe.Product.create(name=p_name)
    return p_re


def create_price(p_id, p_p):
    pr_re = stripe.Price.create(
        product=str(p_id),
        unit_amount=int(p_p),
        currency="sek",
    )
    return pr_re


def create_sub_price(p_id, p_p, unit):
    pr_re = stripe.Price.create(
        product=str(p_id),
        unit_amount=int(p_p),
        currency="usd",
        recurring={"interval": str(unit)}
    )
    return pr_re


def create_subscription(c_id, p_id):
    subscription = stripe.Subscription.create(
        customer=str(c_id),
        items=[
            {"price": str(p_id)},
        ],
    )


def create_customer(c_email, c_name):
    c_re = stripe.Customer.create(
        email=c_email,
        name=c_name,
    )
    return c_re


def create_invoice(c_id):
    invoice = stripe.Invoice.create(customer=c_id)
    finalized_invoice = stripe.Invoice.finalize_invoice(invoice['id'])
    return finalized_invoice


def add_item_to_invoice(c_id, p_id):
    stripe.InvoiceItem.create(
        customer=c_id,
        price=str(p_id),
    )


def create_product_with_price(p_name, price):
    p_re = create_product(p_name)
    p_p_re = create_price(p_re['id'], price)
    return p_re, p_p_re


def create_and_send_invoice(c, p):
    finalized_invoice = create_customer(c['id'], p['name'])
    sent_invoice = stripe.Invoice.send_invoice(finalized_invoice['id'])
