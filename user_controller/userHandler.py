import connexion
from models.user_id_cart_body import UserIdCartBody
from models.user import User

import os
import grpc

from user_service_pb2 import (
    CreateUserRequest,
    PayCartRequest,
    AddItemCartRequest,
    DeleteItemCartRequest,
    GetCartContentRequest,
    GetUserRequest
)

from user_service_pb2_grpc import UserStub

user_service_host = os.getenv("USER_SERVICE_HOST", "localhost")
user_service_port = os.getenv("USER_SERVICE_PORT", "50051")
user_service_channel = grpc.insecure_channel(f"{user_service_host}:{user_service_port}")

client = UserStub(user_service_channel)

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

        request = CreateUserRequest(username=user.username, password=user.password, address=user.address)
        response = client.CreateUser(request)

        if(response.response_code == 0):
            return 'Success', 200
        elif(response.response_code == 1):
            return 'Username already exists', 403
        elif(response.response_code == 2):
            return 'Invalid user parameters', 400
        else:
            return 'Service unavailable. Try again later', 500

    else:
        return 'Invalid request body', 400

def authenticateUser(username, password):
    return 'Testing'