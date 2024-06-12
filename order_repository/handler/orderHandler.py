from concurrent import futures
from datetime import datetime

import threading
import time

from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from order_repository_pb2 import (
    InsertOrderResponse,
    GetOrderResponse,
    GetOrdersResponse,
    OrderRepo,
    OrderRepoID,
    ItemRepo
)

from models.order import OrderRepoMongo, ItemRepoMongo
from mongoengine import *

#Não necessita de test
def run_updateOrderStatus(order_id):
    updateOrderStatus(order_id)

#Não necessita de test
def updateOrderStatus(order_id):
    time.sleep(100)

    try:
        order = OrderRepoMongo.objects.with_id(order_id)
        if order:
            order.status = "delivered"
            order.complete = True
            order.save()
    except DoesNotExist:
        pass
#---------------------------

def insertOrder(request, context):

    user_id = request.user_id
    items = request.items
    destinationAddress = request.destinationAddress
    shipDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    item_instances = []
    for item in items:
        item_instance = ItemRepoMongo(itemID=item.itemID, volume=item.volume)
        item_instances.append(item_instance)

    new_order = OrderRepoMongo(user_id=user_id, items=item_instances, shipDate=shipDate,
                        status="placed", complete=False, destinationAddress=destinationAddress)

    try:

        new_order.save()
        
        threading.Thread(target=lambda: run_updateOrderStatus(str(new_order.pk))).start()
        # Success
        return InsertOrderResponse(response_code=0, order_id=str(new_order.pk))
    except Exception as e:
        error_msg = str(e)
        return InsertOrderResponse(response_code=1, error_msg=error_msg)

def getOrder(request, context):
        order_id = request.order_id
        try:
            order = OrderRepoMongo.objects.with_id(request.order_id)

            # convert to ItemRepo
            items = []
            for item in order.items:
                item_instance = ItemRepo(itemID=item.itemID, volume=item.volume)
                items.append(item_instance)


            orderRepoID = OrderRepoID(
                order_id=str(order_id),
                user_id=order.user_id,
                items=items,
                shipDate=str(order.shipDate),
                status=order.status,
                complete=order.complete,
                destinationAddress=order.destinationAddress
            )

            return GetOrderResponse(response_code=0, order=orderRepoID)
        except DoesNotExist:
            return GetOrderResponse(response_code=1)
        except Exception as e:
            error_msg = str(e)
            return GetOrderResponse(response_code=2, error_msg=error_msg)

def getOrders(request, context):
        try:
            user_id = request.user_id
            orders = OrderRepoMongo.objects(user_id=user_id)

            if not orders:
                return GetOrdersResponse(response_code=1)

            converted_orders = []
            for order in orders:
                
                items = []
                for item in order.items:
                    item_instance = ItemRepo(itemID=item.itemID, volume=item.volume)
                    items.append(item_instance)

                converted_order = OrderRepoID(
                    order_id=str(order.id),
                    user_id=order.user_id,
                    items=items,
                    shipDate=str(order.shipDate),
                    status=order.status,
                    complete=order.complete,
                    destinationAddress=order.destinationAddress
                )
                converted_orders.append(converted_order)

            return GetOrdersResponse(response_code=0, orders=converted_orders)
        except Exception as e:
            error_msg = str(e)
            return GetOrdersResponse(response_code=2, error_msg=error_msg)
