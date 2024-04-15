import os
import grpc
import handlers.itemHandler as ItemHandler
import re
import http.client
import json

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

def registerUser(username, address):

    if(__validateUsername(username)):

        #User has valid credentials

        #Get token from Auth0
        token = __getToken()

        if(token):

            #Save User
            request = InsertUserRequest(username=username, password=token, address=address)
            response = client.InsertUser(request)

            return (response.response_code, token)
    
        else:
            return (3, '')
    else:

        #Credentials don't have a valid format
        return (2, '')
    
def getUserByID(user_id):

    request = GetUserRequest(user_id=user_id)
    response = client.GetUser(request)

    return response

def tradeToken(token):

    #TODO

    return None


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

def __getToken():

    #Code taken and adapted from Auth0 test example

    conn = http.client.HTTPSConnection("dev-gcr7j33oe3lkm2f4.us.auth0.com")
    payload = "{\"client_id\":\"Bxyu0zRaHLs5XMFt6xuSVXRZ1br5S9Hv\",\"client_secret\":\"YfOytuaiv8iYVThvmgDTflaSx7E-ze_WrSrJxbW6-cJLN7sYbjWK38UFqaD8aGL0\",\"audience\":\"http://brewstand-api/\",\"grant_type\":\"client_credentials\"}"
    headers = { 'content-type': "application/json" }

    conn.request("POST", "/oauth/token", payload, headers)

    res = conn.getresponse()
    
    if(res.status == 200):
        jsonString = res.read()
        data = json.loads(jsonString)
        return data['access_token']
    else:
        return None



        
