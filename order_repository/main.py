from concurrent import futures

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from order_repository_pb2 import (
    InsertOrderResponse,
    GetOrderResponse,
    GetOrdersResponse,
    AddItemToOrderResponse,
    RemoveItemFromOrderResponse,
    SetAddressForOrderResponse,
    MarkOrderAsCompleteResponse
)

import order_repository_pb2_grpc
from mongoengine import *
import os

class  OrderRepository(order_repository_pb2_grpc.OrderRepositoryServicer):

    def InsertOrder(self, request, context):
        # TO DO
        response = order_repository_pb2.InsertOrderResponse(response_code=0, order_id=12345)
        return response

    def GetOrder(self, request, context):
        # TO DO
        order = order_repository_pb2.OrderRepo(
            id=123,
            user_id='12',
            ship_date='2024-04-01',
            status='pending',
            complete=False,
            address='Amadora'
        )
        response = order_repository_pb2.GetOrderResponse(response_code=0, order=order)
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

    def AddItemToOrder(self, request, context):
        # TO DO
        response = order_repository_pb2.AddItemToOrderResponse(response_code=0)
        return response

    def RemoveItemFromOrder(self, request, context):
        # TO DO
        response = order_repository_pb2.RemoveItemFromOrderResponse(response_code=0)
        return response

    def SetAddressForOrder(self, request, context):
        # TO DO
        response = order_repository_pb2.SetAddressForOrderResponse(response_code=0)
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
    url = f"mongodb+srv://{__USER}:{__PASSWORD}@brewstandorder0.c4ozpqd.mongodb.net/db?retryWrites=true&w=majority&appName=BrewStand0"
    connect(host=url)

    serve()