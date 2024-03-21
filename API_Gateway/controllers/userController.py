import connexion
from models.user_id_cart_body import UserIdCartBody
from models.user import User

def addToCart(user_id):

    if connexion.request.is_json:
        cartBody = UserIdCartBody.from_dict(connexion.request.get_json())

    return cartBody

def getCart(user_id):
    return 'TESTING'

def removeFromCart(user_id, item_id=None):
    return 'TESTING'

def checkoutCart(user_id):
    return 'TESTING'

def createUser():

    if connexion.request.is_json:
        user = User.from_dict(connexion.request.get_json())

    return user

def authenticateUser(username, password):
    return 'Testing'