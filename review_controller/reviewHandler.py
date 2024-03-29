import connexion
from models.item_id_review_body import ItemIdReviewBody

import os
import grpc

from review_service_pb2 import (
    ItemReviewRequest
)

from review_service_pb2_grpc import ReviewStub

review_service_host = os.getenv("REVIEW_SERVICE_HOST", "localhost")
review_service_port = os.getenv("REVIEW_SERVICE_PORT", "50053")
review_service_channel = grpc.insecure_channel(f"{review_service_host}:{review_service_port}")

client = ReviewStub(review_service_channel)

def updateReview(itemId, body=None):  # noqa: E501
  
    if connexion.request.is_json:
        
        body = ItemIdReviewBody.from_dict(connexion.request.get_json())  # noqa: E501

        request = ItemReviewRequest(item_id = itemId, score = body.score)
        response = client.ReviewItem(request)

        if(response.response_code == 0):
            return '', 200
        elif(response.response_code == 1):
            return '', 400
        elif(response.response_code == 2):
            return '', 404
        else:
            return '', 500

    else:
        return 'Invalid request body', 400