import os
import grpc

from review_service_pb2 import(
    ItemReviewRequest
    # A ideia é esta, mas tem de ser o Item Repository
)

'''
def validID(id):
    return True


Não valides o ID aqui
'''
def validScore(id,score):

    # Aqui dentro tens de ver se o score dado é válido e depois contactar o Item Repository.

    if (0<=score<6):

        # O score é válido. Contacta o Item Repository
        # Do item repository tiras as cenas que precisas para fazer as contas
        # Quando tiveres o score novo, chamas uma função do ItemRepository para dar update (tens de coordenar com a Tânia)

        return 0 # Muda isto para ter em conta a resposta do item repository
    
    else:
        #O score é inválido. Retorna só o error code certo
        return 1
    
