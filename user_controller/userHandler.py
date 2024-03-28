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
    GetUserDetailsRequest
)

from user_service_pb2_grpc import UserStub

user_service_host = os.getenv("USER_SERVICE_HOST", "localhost")
user_service_port = os.getenv("USER_SERVICE_PORT", "50051")
user_service_channel = grpc.insecure_channel(f"{user_service_host}:{user_service_port}")

client = UserStub(user_service_channel)

def addToCart(userId):

    if connexion.request.is_json:
        cartBody = UserIdCartBody.from_dict(connexion.request.get_json())

        request = AddItemCartRequest(user_id = userId, batch_id=cartBody.batch_id, volume=cartBody.volume)
        response = client.AddItemCart(request)

        if(response.response_code==0):
            return '',200
        elif(response.response_code==1):
            return '',404
        elif(response.response_code==2 or response.response_code==3):
            return '', 400
        else:
            return '', 500

    else:
        return '', 400

def getCart(userId):

    request = GetCartContentRequest(user_id=userId)
    response = client.GetCartContent(request)

    if(response.response_code == 0):
        cart_content = {'items' : list(response.content), 'totalCost' : float(response.total_price)}
        return cart_content, 200
    elif(response.response_code == 1):
        return '', 404
    else:
        return '', 500

def removeFromCart(userId, itemId=None):
    return 'TESTING'

def checkoutCart(userId):
    return 'TESTING'

def createUser():

    if connexion.request.is_json:
        user = User.from_dict(connexion.request.get_json())

        request = CreateUserRequest(username=user.username, password=user.password, address=user.address)
        response = client.CreateUser(request)

        if(response.response_code == 0):
            return f"{response.user_id}", 200
        elif(response.response_code == 1):
            return 'Teste', 403
        elif(response.response_code == 2):
            return '', 400
        else:
            return '', 500

    else:
        return 'Invalid request body', 400

def authenticateUser(username, password):
    return 'Testing'