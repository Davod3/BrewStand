from mongoengine import *

class ItemRepo(EmbeddedDocument):
    itemID = IntField(required=True)
    volume = FloatField(required=True)

class OrderRepo(Document):
    user_id = StringField(required=True)
    items = ListField(EmbeddedDocumentField(ItemRepo))
    shipDate = DateTimeField(required=True)
    status = StringField(required=True)
    complete = BooleanField(required=True)
    destinationAddress = StringField(required=True)

class OrderRepoID(Document):
    order_id = StringField(required=True)
    user_id = StringField(required=True)
    items = ListField(EmbeddedDocumentField(ItemRepo))
    shipDate = DateTimeField(required=True)
    status = StringField(required=True)
    complete = BooleanField(required=True)
    destinationAddress = StringField(required=True)