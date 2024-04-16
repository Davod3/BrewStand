import connexion
import six

from models.order import Order 
from models.order_items import OrderItems
from utils import util

import os
import grpc

from order_service_pb2 import (
    GetOrderServiceRequest,
    GetOrdersServiceRequest
)

from order_service_pb2_grpc import OrderStub

order_service_host = os.getenv("ORDER_SERVICE_HOST", "localhost")
order_service_port = os.getenv("ORDER_SERVICE_PORT", "50054")
order_service_channel = grpc.insecure_channel(f"{order_service_host}:{order_service_port}")

client = OrderStub(order_service_channel)

def __protoOrderToOrder(order):

    order_items = list()

    for item in order.items:

            item_schema = {
                 'itemID' : item.itemID,
                 'volume' : item.volume
            }

            order_items.append(item_schema)

    return Order.from_dict({
            'id' : order.order_id,
            'items' : order_items,
            'shipDate' : order.shipDate,
            'status' : order.status,
            'complete' : order.complete,
            'destinationAddress' : order.destinationAddress,
            'userId' : order.user_id
        })

def getOrder(orderId, token_info=None):

    if(token_info):
            userId = token_info['user_id']
    else:
        return 'Invalid user token', 403

    request = GetOrderServiceRequest(order_id = orderId)
    response = client.GetOrder(request)

    if(response.response_code == 0 and response.order.user_id == userId):

        return __protoOrderToOrder(response.order), 200

    else:
        #Not Found
        return 'Order not found', 404


def getOrders(token_info=None):

    if(token_info):
            userId = token_info['user_id']
    else:
        return 'Invalid user token', 403

    request = GetOrdersServiceRequest(user_id = userId)
    response = client.GetOrders(request)

    if(response.response_code == 0):
         
        orders = list()

        for order in response.orders:
              
            orders.append(__protoOrderToOrder(order))

        return orders, 200
         
    else:
    
         #User not found
         return 'User not found', 404
