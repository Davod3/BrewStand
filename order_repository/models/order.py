from mongoengine import *

class ItemRepo(EmbeddedDocument):
    item_id = IntField(required=True)
    volume = FloatField(required=True)

class Order(Document):
    id = IntField(primary_key=True)
    items = ListField(EmbeddedDocumentField(ItemRepo))
    user_id = StringField(required=True)
    ship_date = StringField(required=True)
    status = StringField(required=True)
    complete = BooleanField(required=True)
    address = StringField(required=True)