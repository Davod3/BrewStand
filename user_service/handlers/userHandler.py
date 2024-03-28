import os
import grpc
import handlers.itemHandler as ItemHandler

from user_repository_pb2 import (
    InsertUserRequest,
    GetUserRequest,
    UserCartAddRequest,
    UserCartDeleteRequest,
    UserCartGetRequest,
    GetUserByIDRequest
)

from user_repository_pb2_grpc import UserRepositoryStub

from user_service_pb2 import CartContent

user_repository_host = os.getenv("USER_REPOSITORY_HOST", "localhost")
user_repository_port = os.getenv("USER_REPOSITORY_PORT", "50061")
user_repository_channel = grpc.insecure_channel(f"{user_repository_host}:{user_repository_port}")

client = UserRepositoryStub(user_repository_channel)


def __validateUsername(username):
    #TODO
    return True

def __validatePassword(password):
    #TODO
    return True

def __validateAddress(address):
    #TODO
    return True

def registerUser(username, password, address):

    if(__validateUsername(username) and __validatePassword(password) and __validateAddress(address)):

        #User has valid credentials
        request = InsertUserRequest(username=username, password=password, address=address)
        response = client.InsertUser(request)

        return response.response_code

    else:

        #Credentials don't have a valid format
        return 2
    
def authenticateUser(username, password):
    
    request = GetUserRequest(username = username, password = password)
    response = client.GetUser(request)

    if(response.response_code == 0):
        return (response.response_code, response.user_id)
    else:
        return(response.response_code, '')
    
def getUserByID(user_id):

    request = GetUserByIDRequest(user_id=user_id)
    response = client.GetUserByID(request)

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


        
