from mongoengine import *

class CartItem(EmbeddedDocument):
    batch_id = StringField(required=True)
    volume = FloatField(required=True)


class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    address = StringField(required=True)
    cart = EmbeddedDocumentListField(CartItem)