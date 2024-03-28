def validateBatch(batch_id):
    #TODO - vai falar com o inventory_service para ver se o batchID existe
    request = GetBatchId(batch_id=batch_id)
    
    return 0

def getBatchScore(batch_id):
    #TODO - vai falar com o inventory_service para ver o score do batch
    request = GetBatchScoreRequest(batch_id=batch_id)
    response = GetBatchScore(request)
    return response

def getNvotos(batch_id):
    #TODO - vai falar com o inventory_service para ver o numero de votos do batch
    request = GetBatchNvotosRequest(batch_id=batch_id)
    response = GetBatchNvotos(request)
    return response