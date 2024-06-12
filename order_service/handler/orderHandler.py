import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from inventory_service_pb2 import (
    UpdateVolumeServiceRequest,
    ValidateOrderServiceRequest
)

from order_service_pb2 import (
    GetOrderServiceResponse,
    GetOrdersServiceResponse,
    CreateOrderServiceResponse,
    OrderDetails,
    ItemDetails
)

import os
import order_repository_pb2
from order_repository_pb2_grpc import OrderRepositoryStub
from inventory_service_pb2_grpc import InventoryServiceStub

order_repository_host = os.getenv("ORDER_REPOSITORY_HOST", "localhost")
order_repository_port = os.getenv("ORDER_REPOSITORY_PORT", "50064")
order_repo_stub = OrderRepositoryStub(grpc.insecure_channel(f"{order_repository_host}:{order_repository_port}"))
inventory_host = os.getenv("INVENTORY_SERVICE_HOST", "localhost")
inventory_port = os.getenv("INVENTORY_SERVICE_PORT", "50052")
inventory_channel = grpc.insecure_channel(f"{inventory_host}:{inventory_port}")
inventory_client = InventoryServiceStub(inventory_channel)

#Não necessita de test
def convertOrderToDetails(order):
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

#--------------------------

def getOrder(request, context):
        try:
            order_id = request.order_id
            
            response = order_repo_stub.GetOrder(order_repository_pb2.GetOrderRequest(order_id=order_id))
            convertedOrder = convertOrderToDetails(response.order)
            return GetOrderServiceResponse(response_code=response.response_code, order=convertedOrder)
        except grpc.RpcError as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to get order: {e}")
            return GetOrderServiceResponse(response_code=1)
        
def getOrders(request, context):
        try:
            user_id = request.user_id
            
            response = order_repo_stub.GetOrders(order_repository_pb2.GetOrdersRequest(user_id=user_id))
            order_details_list = [convertOrderToDetails(order) for order in response.orders]
            return GetOrdersServiceResponse(response_code=response.response_code, orders=order_details_list)
        except grpc.RpcError as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to get orders: {e}")
            return GetOrdersServiceResponse(response_code=1)
        
#Não necessita de test       
def updateVolumeForItems(items):
        for item in items:
            update_volume_request = UpdateVolumeServiceRequest(batch_id=item.itemID, volume=item.volume)
            update_volume_response = inventory_client.updateVolumeService(update_volume_request)
            if update_volume_response.response_code != 0:
                return False
        return True

#Não necessita de test
def validateOrderItems(items):
        for item in items:
            validate_request = ValidateOrderServiceRequest(batch_id=item.itemID, volume_order=item.volume)
            validate_response = inventory_client.validateOrderService(validate_request)
            if validate_response.response_code != 0:
                return False
        return True     

def createOrder(request, context):
        try:

            user_id = request.user_id
            items = request.items
            destination_address = request.destinationAddress
            
            # Validate Order
            if not validateOrderItems(items):
                return CreateOrderServiceResponse(response_code=1)

            # Update Items for Order
            if not updateVolumeForItems(items):
                return CreateOrderServiceResponse(response_code=1)

            item_repo_list = []
            for item in items:
                item_repo = order_repository_pb2.ItemRepo(itemID=item.itemID, volume=item.volume)
                item_repo_list.append(item_repo)

            order_repo_response = order_repo_stub.InsertOrder(order_repository_pb2.InsertOrderRequest(
                user_id=user_id,
                items=item_repo_list,
                destinationAddress=destination_address
            ))
            
            if order_repo_response.response_code == 0:
                return CreateOrderServiceResponse(response_code=0, order_id=order_repo_response.order_id)
            else:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Falha ao criar pedido")
                return CreateOrderServiceResponse(response_code=1)
        except grpc.RpcError as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Falha ao criar pedido: {e}")
            return CreateOrderServiceResponse(response_code=1)     