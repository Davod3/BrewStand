from concurrent import futures

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

import handler.orderHandler as orderHandler
import order_service_pb2_grpc

class OrderService(order_service_pb2_grpc.OrderServicer):

    def GetOrder(self, request, context):
        
        return orderHandler.getOrder(request, context)

    def GetOrders(self, request, context):

        return orderHandler.getOrders(request, context)

    def CreateOrder(self, request, context):

        return orderHandler.createOrder(request, context)

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