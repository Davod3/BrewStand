import os
import grpc

from inventory_service_pb2 import (
    GetBatchCostServiceRequest,
    ValidateItemServiceRequest 
)

from inventory_service_pb2_grpc import InventoryServiceStub

inventory_service_host = os.getenv("INVENTORY_SERVICE_HOST", "localhost")
inventory_service_port = os.getenv("INVENTORY_SERVICE_PORT", "50062")
inventory_service_channel = grpc.insecure_channel(f"{inventory_service_host}:{inventory_service_port}")

client = InventoryServiceStub(inventory_service_channel)


def validateItem(batch_id):
    
    request = ValidateItemServiceRequest(batch_id = batch_id)
    response = client.validateItemService(request)

    return response.response_code

def getBatchCost(batch_id):
    
    request = GetBatchCostServiceRequest(batch_id = batch_id)
    response = client.getBatchCostService(request)

    return response.cost