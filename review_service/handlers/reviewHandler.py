import os
import grpc
import handlers.itemHandlerReview as itemHandlerReview


def review(batch_id,score):

    # Aqui dentro tens de ver se o score dado é válido e depois contactar o Item Repository.

    if (0<=score<=10):

        # O score é válido. Contacta o Item Repository

        if(itemHandlerReview.validateBatch(batch_id)):

            # Batch exists. Calculate and update score

            oldScore = itemHandlerReview.getBatchScore(batch_id)
            numero_pessoas= itemHandlerReview.getNvotos(batch_id)
            newscore = ((oldScore * numero_pessoas) + score) / (numero_pessoas + 1)

            result = itemHandlerReview.updateScore(batch_id, newscore)

            return result

        else:
            return 2 # Item not found
    
    else:
        #O score é inválido. Retorna só o error code certo
        return 1
    
