from mongoengine import *

class Invoice(Document):
    invoiceId = StringField()  # Unique identifier for the invoice
    price = FloatField(required=True)  # Total price of the invoice
    orderID = StringField(required=True)  # Associated order ID
    userId = StringField(required=True)  # ID of the user who made the payment
    fiscalAddress = StringField(required=True)  # Billing address
    cardLastFour = StringField(required=True)  # Last four digits of the card used
