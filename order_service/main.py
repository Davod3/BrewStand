from concurrent import futures

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from order_pb2 import (
    GetOrderResponse,
    GetOrderResponse,
    CreateOrderResponse,
    ValidateOrderResponse
)

import order_pb2_grpc

class OrderService(order_pb2_grpc.OrderServicer):

    def GetOrder(self, request, context):
        # TO DO
        order_id = request.order_id
        return GetOrderResponse(response_code=0)

    def GetOrders(self, request, context):
        # TO DO
        user_id = request.user_id
        return GetOrdersResponse(response_code=0)

    def CreateOrder(self, request, context):
        # TO DO
        user_id = request.user_id
        return CreateOrderResponse(response_code=0)

    def ValidateOrder(self, request, context):
        # TO DO
        order_id = request.order_id
        return ValidateOrderResponse(response_code=0, valid=True)

def serve():

    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )

    order_pb2_grpc.add_OrderServicer_to_server(
        OrderService(), server
    )

    server.add_insecure_port("[::]:50054")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()