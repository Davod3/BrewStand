from concurrent import futures

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from user_repository_pb2 import (
    InsertUserResponse,
    UserCartAddResponse,
    UserCartDeleteResponse,
    UserCartGetResponse,
    Batch,
    GetUserResponse
)

import user_repository_pb2_grpc
from models.user import User
from mongoengine import *
import os
import cartHandler as CartHandler

class UserRepositoryService(user_repository_pb2_grpc.UserRepositoryServicer):
    
    def InsertUser(self, request, context):

        username = request.username
        password = request.password
        address = request.address

        user = User(username=username, password=password, address=address)

        try:
            user.save()
            #Success
            return InsertUserResponse(response_code = 0, user_id=str(user.pk))
        except NotUniqueError:
            #Repeated username
            return InsertUserResponse(response_code = 1)

    
    def UserCartAdd(self,request, context):

        result = CartHandler.addToCart(request.user_id, request.batch_id, request.volume)

        return UserCartAddResponse(response_code = result)
    
    def UserCartDelete(self, request, context):

        result = CartHandler.removeFromCart(request.user_id, request.batch_id)

        return UserCartDeleteResponse(response_code = result)
    
    def UserCartGet(self, request, context):

        user_cart = CartHandler.getCart(request.user_id)

        def convertToRPC(cart_item):
            return Batch(batch_id=cart_item.batch_id, volume=cart_item.volume)

        if(user_cart is None):
             return UserCartGetResponse(response_code = 1, content = None)
        else:
            converted_items = map(convertToRPC, user_cart)
            return UserCartGetResponse(response_code = 0,content = converted_items )
        
    def GetUser(self, request, context):

        try:
            user = User.objects.get(id=request.user_id)
            return GetUserResponse(response_code=0, username=user.username, address=user.address, user_id=str(user.pk))
        except DoesNotExist:
            return GetUserResponse(response_code=1) # User not found
    
    def GetUserByToken(self, request, context):

        # Kept things the same to not change too much code, but the password in the db
        # is the token. The user_id in the request is also supposed to be the token

        try:
            user = User.objects.get(password=request.token)
            return GetUserResponse(response_code=0, username=user.username, address=user.address, user_id=str(user.pk))
        except DoesNotExist:
            return GetUserResponse(response_code=1) # User with given token not found


    
def serve():

    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )

    user_repository_pb2_grpc.add_UserRepositoryServicer_to_server(
        UserRepositoryService(), server
    )

    server.add_insecure_port("[::]:50061")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":

    __USER = os.getenv('MONGO_USER')
    __PASSWORD =  os.getenv('MONGO_PASSWORD')
    url = f"mongodb+srv://{__USER}:{__PASSWORD}@cluster0.q350jt0.mongodb.net/db?retryWrites=true&w=majority&appName=Cluster0"
    connect(host=url)

    serve()