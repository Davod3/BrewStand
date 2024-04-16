import connexion
from models.user_id_cart_body import UserIdCartBody
from models.user import User
from models.cart_payment_body import CartPaymentBody
from models.invoice import Invoice

import os
import grpc

from user_service_pb2 import (
    CreateUserRequest,
    PayCartRequest,
    AddItemCartRequest,
    DeleteItemCartRequest,
    GetCartContentRequest,
    TradeTokenRequest
)

from user_service_pb2_grpc import UserStub

user_service_host = os.getenv("USER_SERVICE_HOST", "localhost")
user_service_port = os.getenv("USER_SERVICE_PORT", "50051")
user_service_channel = grpc.insecure_channel(f"{user_service_host}:{user_service_port}")

client = UserStub(user_service_channel)

def addToCart(token_info=None):

    if connexion.request.is_json:

        if(token_info):
            userId = token_info['user_id']
        else:
            return 'Invalid user token', 403

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
        return 'Invalid request body', 400

def getCart(token_info=None):

    if(token_info):
        userId = token_info['user_id']
    else:
        return 'Invalid user token', 403

    request = GetCartContentRequest(user_id=userId)
    response = client.GetCartContent(request)

    if(response.response_code == 0):

        cart_content = __getCartContent(response.content)

        cart_content = {'items' : cart_content, 'totalCost' : float(response.total_price)}
        return cart_content, 200
    elif(response.response_code == 1):
        return '', 404
    else:
        return '', 500

def removeFromCart(itemId=0, token_info=None):

    if(token_info):
        userId = token_info['user_id']
    else:
        return 'Invalid user token', 403

    request = DeleteItemCartRequest(user_id = userId, batch_id = itemId)
    response = client.DeleteItemCart(request)

    if(response.response_code == 0 or response.response_code == 2):
        return '', 200
    elif(response.response_code == 1):
        return '', 404
    else:
        return '', 500

def checkoutCart(token_info=None):

    if connexion.request.is_json:

        if(token_info):
            userId = token_info['user_id']
        else:
            return 'Invalid user token', 403

        card_details = CartPaymentBody.from_dict(connexion.request.get_json())  # noqa: E501

        request = PayCartRequest(user_id = userId,
                                 card_number = card_details.card_number,
                                 card_expiry = card_details.card_expiry,
                                 card_cvc = card_details.card_cvc)
        
        response = client.PayCart(request)

        if(response.response_code == 0):

            return Invoice.from_dict({
                'invoiceID' : response.invoice.invoice_id,
                'price' : response.invoice.price,
                'orderID' : response.invoice.order_id,
                'customerID' : response.invoice.customer_id,
                'fiscalAddress' : response.invoice.fiscal_address,
                'details' : response.invoice.details
            })


        elif(response.response_code == 1):
            return 'User not found', 404
        elif(response.response_code == 2):
            return 'Cart is empty', 500
        elif(response.response_code == 3):
            return 'Invalid Order', 500
        else:
            return 'Service Unavailable', 500


def createUser():

    if connexion.request.is_json:
        user = User.from_dict(connexion.request.get_json())

        request = CreateUserRequest(username=user.username, address=user.address)
        response = client.CreateUser(request)

        if(response.response_code == 0):
            return {'token' : response.user_id}, 200
        elif(response.response_code == 1):
            return '', 403
        elif(response.response_code == 2):
            return '', 400
        else:
            return '', 500

    else:
        return 'Invalid request body', 400


def tradeToken(token):

    request = TradeTokenRequest(token = token)
    response = client.TradeToken(request)


    if(response.response_code == 0):
        return {'user_id' : response.user_id}
    else:
        return None


def __getCartContent(item_list):

    cart_content = list()

    for item in item_list:
        cart_content.append({'itemID' : item.batch_id, 'volume' : item.volume})

    return cart_content
