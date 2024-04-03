import connexion
import six

from models.item import Item  # noqa: E501
from utils import util

import os
import grpc

from inventory_service_pb2 import (
    GetBatchServiceRequest,
    EmptyMessage
)

from inventory_service_pb2_grpc import InventoryServiceStub

inventory_service_host = os.getenv("INVENTORY_SERVICE_HOST", "localhost")
inventory_service_port = os.getenv("INVENTORY_SERVICE_PORT", "50052")
inventory_service_channel = grpc.insecure_channel(f"{inventory_service_host}:{inventory_service_port}")

client = InventoryServiceStub(inventory_service_channel) 

def __parseBatch(batch):

    parsed_batch = Item.from_dict({
                    "batchID" : batch.batch_id,
                    "brewLocation" : batch.location,
                    "beerStyle" : batch.beer_style,
                    "userScore" : batch.user_score,
                    "expertScore" : batch.quality_score,
                    "phLevel" : batch.ph_level,
                    "alchoolContent" : batch.alcohol_content,
                    "availableVolume" : batch.volume_produced,
                    "brewDate" : batch.brew_date,
                    "cost" : batch.cost
                })
    
    return parsed_batch


def getBatch(itemId):

    request = GetBatchServiceRequest(batch_id = itemId)
    response = client.getBatchService(request)

    if(response.response_code == 0):

        return __parseBatch(response.batch), 200
    else:

        #Not found
        return '', 404


def getBatches(item1=None, item2=None):

    if(item1 is not None and item2 is not None):

        request_batch1 = GetBatchServiceRequest(batch_id = item1)
        response_batch1 = client.getBatchService(request_batch1)

        request_batch2 = GetBatchServiceRequest(batch_id = item2)
        response_batch2 = client.getBatchService(request_batch2)

        if(response_batch1.response_code == 0 and response_batch2.response_code == 0):
            
            batch1 = __parseBatch(response_batch1.batch)
            batch2 = __parseBatch(response_batch2.batch)

            return [batch1, batch2]

        else:

            #Not found
            return [], 404
    else:

        batches = list()

        request = EmptyMessage()
        response = client.getBatchesService(request)

        if(response.response_code == 0):

            for batch in response.batches:

                batches.append(__parseBatch(batch))
            
            return batches, 200

        else:
            return '', 500
