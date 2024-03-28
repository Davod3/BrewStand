import os
import grpc
import handlers.reviewHandler as ReviewHandler

"""
from inventory_service_pb2 import (
    GetBatchIdRequest,
    GetBatchScoreRequest,
    GetBatchNvotosRequest,
    UpdateScoreRequest,  
)

from inventorry_service_pb2_grpc import InventoryserviceStub

inventory_service_host = os.getenv("INVENTORY_SERVICE_HOST", "localhost")
inventory_service_port = os.getenv("INVENTORY_SERVICE_PORT", "5006*")
inventory_service_channel = grpc.insecure_channel(f"{inventory_service_host}:{inventory_service_port}")

client = InventoryserviceStub(inventory_service_channel)


def validateBatch(batch_id):
    #TODO - vai falar com o inventory_service para ver se o batchID existe

    request = GetBatchIdRequest(batch_id=batch_id)
    
    return True

def getBatchScore(batch_id):
    #TODO - vai falar com o inventory_service para ver o score do batch

    request = GetBatchScoreRequest(batch_id=batch_id)
    response = client.GetBatchScore(request)

    return 1

def getNvotos(batch_id):
    #TODO - vai falar com o inventory_service para ver o numero de votos do batch

    request = GetBatchNvotosRequest(batch_id=batch_id)
    response = client.GetBatchNvotos(request)

    return 1

def updateScore(score):
    newscore = ReviewHandler.validScore()
    request = UpdateScoreRequest(score = newscore)
    response = client.UpdateScore(request)
    return 0

"""