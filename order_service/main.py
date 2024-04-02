from concurrent import futures

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from order_service_pb2 import (
    GetOrderServiceRequest,
    GetOrderServiceResponse,
    GetOrdersServiceRequest,
    GetOrdersServiceResponse,
    CreateOrderServiceRequest,
    CreateOrderServiceResponse,
    OrderDetails,
    ItemDetails
)

import order_service_pb2
import order_service_pb2_grpc

import os
import order_repository_pb2
from order_repository_pb2_grpc import OrderRepositoryStub

class OrderService(order_service_pb2_grpc.OrderServicer):

    def __init__(self):
        self.order_repository_host = os.getenv("ORDER_REPOSITORY_HOST", "localhost")
        self.order_repository_port = os.getenv("ORDER_REPOSITORY_PORT", "50064")
        self.order_repo_stub = OrderRepositoryStub(grpc.insecure_channel(f"{self.order_repository_host}:{self.order_repository_port}"))

    def convertOrderToDetails(self, order):
        items = []
        for item in order.items:
            items.append(ItemDetails(itemID=item.itemID, volume=item.volume))
        
        return OrderDetails(
            order_id=order.order_id,
            user_id=order.user_id,
            items=items,
            shipDate=order.shipDate,
            status=order.status,
            complete=order.complete,
            destinationAddress=order.destinationAddress
        )

    def GetOrder(self, request, context):
        try:
            order_id = request.order_id
            
            response = self.order_repo_stub.GetOrder(order_repository_pb2.GetOrderRequest(order_id=order_id))
            convertedOrder = self.convertOrderToDetails(response.order)
            return GetOrderServiceResponse(response_code=response.response_code, order=convertedOrder)
        except grpc.RpcError as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to get order: {e}")
            return GetOrderServiceResponse(response_code=1)


    def GetOrders(self, request, context):
        try:
            user_id = request.user_id
            
            response = self.order_repo_stub.GetOrders(order_repository_pb2.GetOrdersRequest(user_id=user_id))
            order_details_list = [self.convertOrderToDetails(order) for order in response.orders]
            return GetOrdersServiceResponse(response_code=response.response_code, orders=order_details_list)
        except grpc.RpcError as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to get orders: {e}")
            return GetOrdersServiceResponse(response_code=1)

    def CreateOrder(self, request, context):
        # TO DO
        user_id = request.user_id
        return CreateOrderServiceResponse(response_code=0)

def serve():

    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )

    order_service_pb2_grpc.add_OrderServicer_to_server(
        OrderService(), server
    )

    server.add_insecure_port("[::]:50054")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()