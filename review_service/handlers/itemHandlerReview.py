import os
import grpc

from inventory_service_pb2 import (
    
    ValidateItemServiceRequest,
    GetBatchScoreServiceRequest,
    GetBatchUsersReviewServiceRequest,
    UpdateScoreServiceRequest

)

from inventory_service_pb2_grpc import InventoryServiceStub


inventory_service_host = os.getenv("INVENTORY_SERVICE_HOST", "localhost")
inventory_service_port = os.getenv("INVENTORY_SERVICE_PORT", "50052")
inventory_service_channel = grpc.insecure_channel(f"{inventory_service_host}:{inventory_service_port}")

client = InventoryServiceStub(inventory_service_channel)


def validateBatch(batch_id):
    
    request = ValidateItemServiceRequest(batch_id = batch_id)
    response = client.validateItemService(request)

    if(response.response_code == 0):
        return True
    else:
        return False

def getBatchScore(batch_id):
    
    request = GetBatchScoreServiceRequest(batch_id = batch_id)
    response = client.getBatchScoreService(request)

    return response.score

def getNvotos(batch_id):
    
    request = GetBatchUsersReviewServiceRequest(batch_id = batch_id)
    response = client.getBatchUsersReviewService(request)

    return response.n_users_review

def updateScore(batch_id, score):
    
    request = UpdateScoreServiceRequest(batch_id = batch_id, new_score = score)
    response = client.updateScoreService(request)

    return response.response_code
