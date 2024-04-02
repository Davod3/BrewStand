from concurrent import futures
from datetime import datetime

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from order_repository_pb2 import (
    InsertOrderResponse,
    GetOrderResponse,
    GetOrdersResponse,
    MarkOrderAsCompleteResponse,
    OrderRepo,
    OrderRepoID,
    ItemRepo
)

from models.order import OrderRepoMongo, ItemRepoMongo

import order_repository_pb2_grpc
from mongoengine import *
import os

class  OrderRepository(order_repository_pb2_grpc.OrderRepositoryServicer):

    def InsertOrder(self, request, context):

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

            # Success
            return InsertOrderResponse(response_code=0, order_id=str(new_order.pk))
        except Exception as e:
            return InsertOrderResponse(response_code=1)

    def GetOrder(self, request, context):
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

    def GetOrders(self, request, context):
        try:
            user_id = request.user_id
            orders = OrderRepoMongo.objects(user_id=user_id)

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
        except DoesNotExist:
            return GetOrdersResponse(response_code=1)
        except Exception as e:
            error_msg = str(e)
            return GetOrdersResponse(response_code=2, error_msg=error_msg)

    def MarkOrderAsComplete(self, request, context):
        # TO DO
        response = order_repository_pb2.MarkOrderAsCompleteResponse(response_code=0)
        return response

def serve():

    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )

    order_repository_pb2_grpc.add_OrderRepositoryServicer_to_server(
        OrderRepository(), server
    )

    server.add_insecure_port("[::]:50064")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":

    __USER = os.getenv('MONGO_USER')
    __PASSWORD =  os.getenv('MONGO_PASSWORD')
    url = f"mongodb+srv://{__USER}:{__PASSWORD}@orders.rfyzofq.mongodb.net/?retryWrites=true&w=majority&appName=Orders"
    connect(host=url)

    serve()