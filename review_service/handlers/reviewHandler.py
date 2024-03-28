import os
import grpc
import handlers.itemHandlerReview as itemHandlerReview

from review_service_pb2 import(
    ItemReviewRequest
    # A ideia é esta, mas tem de ser o Item Repository
)


def validScore(batch_id,score):

    # Aqui dentro tens de ver se o score dado é válido e depois contactar o Item Repository.

    if (0<=score<10):

        # O score é válido. Contacta o Item Repository
        # Do item repository tiras as cenas que precisas para fazer as contas
        # Quando tiveres o score novo, chamas uma função do ItemRepository para dar update (tens de coordenar com a Tânia)
        """ 
        oldScore = itemHandlerReview.getBatchScore()
        numero_pessoas= itemHandlerReview.getNvotos()
        newscore = (oldScore * numero_pessoas + score)/numero_pessoas + 1
        
        """

        ########################################
        # Estou confuso com o que meter aqui   #
        ########################################

        return 0 # Muda isto para ter em conta a resposta do item repository
    
    else:
        #O score é inválido. Retorna só o error code certo
        return 1
    
