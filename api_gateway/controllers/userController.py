import connexion
from models.user_id_cart_body import UserIdCartBody
from models.user import User

import os

import grpc 
from user_pb2 import CreateUserRequest
from user_pb2_grpc import UserStub

user_host = os.getenv("USER_SERVICE_HOST", "localhost")
user_channel = grpc.insecure_channel(f"{user_host}:50051")

user_client = UserStub(user_channel)

print('THIS HAPPENSSSS')

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

    create_user_request = CreateUserRequest(username=user.username, password=user.password, address=user.address)

    create_user_response = user_client.CreateUser(create_user_request) 

    return create_user_response.response_code

def authenticateUser(username, password):
    return 'Testing'