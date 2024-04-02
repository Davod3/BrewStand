import os
import grpc
import handlers.itemHandler as ItemHandler
import re

from user_repository_pb2 import (
    InsertUserRequest,
    GetUserRequest,
    UserCartAddRequest,
    UserCartDeleteRequest,
    UserCartGetRequest
)

from user_repository_pb2_grpc import UserRepositoryStub

from user_service_pb2 import CartContent

user_repository_host = os.getenv("USER_REPOSITORY_HOST", "localhost")
user_repository_port = os.getenv("USER_REPOSITORY_PORT", "50061")
user_repository_channel = grpc.insecure_channel(f"{user_repository_host}:{user_repository_port}")

client = UserRepositoryStub(user_repository_channel)


def __validateUsername(username):
    
    pattern = re.compile("^[a-zA-Z0-9_]*$")

    return len(username) > 3 and pattern.match(username) is not None

def __validatePassword(password):

    return len(password) > 3

def registerUser(username, password, address):

    if(__validateUsername(username) and __validatePassword(password)):

        #User has valid credentials
        request = InsertUserRequest(username=username, password=password, address=address)
        response = client.InsertUser(request)

        return (response.response_code, response.user_id)

    else:

        #Credentials don't have a valid format
        return (2, '')
    
def getUserByID(user_id):

    request = GetUserRequest(user_id=user_id)
    response = client.GetUser(request)

    return response

def addToCart(user_id, batch_id, volume):

    if(volume <= 0):
        #Volume is invalid
        return 3

    item_response_code = ItemHandler.validateItem(batch_id)

    if(item_response_code == 0):
        
        #Item is valid, add to cart
        request = UserCartAddRequest(user_id=user_id, batch_id=batch_id, volume=volume)
        response = client.UserCartAdd(request)

        return response.response_code
    
    else:

        #Item is not valid. Return correct response code
        return item_response_code
    
def getCartContent(user_id):

    request = UserCartGetRequest(user_id=user_id)
    response = client.UserCartGet(request)

    if(response.response_code == 0):

        #Query went ok, extract items
        items = response.content
        total_cost = 0
        cart_contents = list()

        for item in items:
            cart_contents.append(CartContent(batch_id=item.batch_id, volume=item.volume))
            total_cost += ItemHandler.getBatchCost(item.batch_id) * item.volume


        return (0, cart_contents, total_cost)
    
    else:

        #User was not found
        return (response.response_code, [], 0)
    
def deleteFromCart(user_id, batch_id=0):

    request = UserCartDeleteRequest(user_id=user_id, batch_id=batch_id)
    response = client.UserCartDelete(request)

    return response.response_code


        
