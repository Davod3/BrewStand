from concurrent import futures
from datetime import datetime

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

import order_repository_pb2_grpc
from mongoengine import *
import os

import handler.orderHandler as orderHandlers

class  OrderRepository(order_repository_pb2_grpc.OrderRepositoryServicer):

    def InsertOrder(self, request, context):

        return orderHandlers.insertOrder(request, context)
    
    def GetOrder(self, request, context):

        return orderHandlers.getOrder(request, context)

    def GetOrders(self, request, context):

        return orderHandlers.getOrders(request, context)
    
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
    __DB = os.getenv('MONGO_DB')
    url = f"mongodb+srv://{__USER}:{__PASSWORD}@orders.rfyzofq.mongodb.net/{__DB}?retryWrites=true&w=majority&appName=Orders"
    connect(host=url)

    serve()