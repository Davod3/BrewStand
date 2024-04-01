from concurrent import futures
from datetime import datetime

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from order_repository_pb2 import (
    InsertOrderResponse,
    GetOrderResponse,
    GetOrdersResponse,
    MarkOrderAsCompleteResponse
)

from models.order import OrderRepo, ItemRepo
import order_repository_pb2_grpc
from mongoengine import *
import os

class  OrderRepository(order_repository_pb2_grpc.OrderRepositoryServicer):

    def InsertOrder(self, request, context):

        user_id = request.user_id
        items = request.items
        destinationAddress = request.destinationAddress
        shipDate = datetime.now()

        item_instances = []
        for item in items:
            item_instance = ItemRepo(itemID=item.itemID, volume=item.volume)
            item_instances.append(item_instance)

        new_order = OrderRepo(user_id=user_id, items=item_instances, shipDate=shipDate,
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
            order = OrderRepo.objects.get(id=order_id)
            orderRepo = order_repository_pb2.OrderRepo(
                id=str(order.id),
                user_id=order.user_id,
                ship_date=str(order.shipDate),
                status=order.status,
                complete=order.complete,
                address=order.destinationAddress
            )
            response = GetOrderResponse(response_code=0, order=orderRepo)
        except DoesNotExist:
            response = GetOrderResponse(response_code=1)
        except Exception as e:
            response = GetOrderResponse(response_code=1, error_msg=str(e))
        return response

    def GetOrders(self, request, context):
        # TO DO
        orders = [
            order_repository_pb2.OrderRepo(
                id=123,
                user_id='23',
                ship_date='2024-04-01',
                status='pending',
                complete=False,
                address='Amadora'
            ),
            order_repository_pb2.OrderRepo(
                id=456,
                user_id='user123',
                ship_date='2024-04-02',
                status='shipped',
                complete=True,
                address='Alges'
            )
        ]
        response = order_repository_pb2.GetOrdersResponse(response_code=0, orders=orders)
        return response

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