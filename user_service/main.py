from concurrent import futures

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from user_service_pb2 import (
    CreateUserResponse,
    AuthenticateUserResponse,
    GetUserDetailsResponse,
    PayCartResponse,
    AddItemCartResponse,
    DeleteItemCartResponse,
    GetCartContentResponse

)

import user_service_pb2_grpc
import handlers.userHandler as UserHandler
import handlers.billingHandler as BillingHandler

class UserService(user_service_pb2_grpc.UserServicer):
    
    def CreateUser(self, request, context):

        result = UserHandler.registerUser(request.username, request.password, request.address)

        return CreateUserResponse(response_code = result)
    
    def AuthenticateUser(self, request, context):

        (response_code, received_id) = UserHandler.authenticateUser(request.username, request.password)

        return AuthenticateUserResponse(response_code = response_code, user_id = received_id)
    
    def GetUser(self, request, context):

        response = UserHandler.getUserByID(request.user_id)

        return GetUserDetailsResponse(response_code = response.response_code, username = response.username, address = response.address)
    
    def PayCart(self, request, context):
        return PayCartResponse(response_code = 0, invoice=None)
    
    def AddItemCart(self, request, context):

        response = UserHandler.addToCart(request.user_id, request.batch_id, request.volume)

        return AddItemCartResponse(response_code = response)
    
    def DeleteItemCart(self, request, context):

        result = UserHandler.deleteFromCart(user_id=request.user_id,batch_id=request.batch_id)

        return DeleteItemCartResponse(response_code = result)
    
    def GetCartContent(self, request, context):

        (response_code, cart_content, total_cost) = UserHandler.getCartContent(request.user_id)

        return GetCartContentResponse(response_code=response_code, content=cart_content, total_price=total_cost)
    
def serve():

    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )

    user_service_pb2_grpc.add_UserServicer_to_server(
        UserService(), server
    )

    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()