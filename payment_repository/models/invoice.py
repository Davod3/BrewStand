from mongoengine import *

class Invoice(Document):
    invoice_id = StringField()  # Unique identifier for the invoice
    price = FloatField(required=True)  # Total price of the invoice
    order_id = StringField(required=True)  # Associated order ID
    costumer_id = StringField(required=True)  # ID of the user who made the payment
    fiscal_address = StringField(required=True)  # Billing address
    details = StringField(required=True)  # Last four digits of the card used
