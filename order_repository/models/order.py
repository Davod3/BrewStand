from mongoengine import *

class ItemRepoMongo(EmbeddedDocument):
    itemID = IntField(required=True)
    volume = FloatField(required=True)

class OrderRepoMongo(Document):
    user_id = StringField(required=True)
    items = ListField(EmbeddedDocumentField(ItemRepoMongo))
    shipDate = StringField(required=True)
    status = StringField(required=True)
    complete = BooleanField(required=True)
    destinationAddress = StringField(required=True)
    