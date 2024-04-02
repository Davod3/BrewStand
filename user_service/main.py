from concurrent import futures

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from user_service_pb2 import (
    CreateUserResponse,
    GetUserDetailsResponse,
    PayCartResponse,
    AddItemCartResponse,
    DeleteItemCartResponse,
    GetCartContentResponse,
    Invoice

)

import user_service_pb2_grpc
import handlers.userHandler as UserHandler
import handlers.billingHandler as BillingHandler

class UserService(user_service_pb2_grpc.UserServicer):
    
    def CreateUser(self, request, context):

        (response_code, user_id) = UserHandler.registerUser(request.username, request.password, request.address)

        return CreateUserResponse(response_code = response_code, user_id = user_id)
    
    def GetUser(self, request, context):

        response = UserHandler.getUserByID(request.user_id)

        return GetUserDetailsResponse(response_code = response.response_code, username = response.username, address = response.address)
    
    def PayCart(self, request, context):

        (response_code,invoice_id, price,order_id,customer_id,fiscal_address,details) = BillingHandler.initiatePayment(request.user_id, request.card_number, request.card_expiry, request.card_cvc)

        return PayCartResponse(response_code = response_code, invoice=Invoice(invoice_id=invoice_id, price=price, order_id=order_id, customer_id=customer_id, fiscal_address=fiscal_address, details=details))
    
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