import unittest
from unittest.mock import MagicMock, patch
import xmlrunner
import sys


sys.modules['inventory_service_pb2'] = MagicMock()
sys.modules['inventory_repository_pb2_grpc'] = MagicMock()
sys.modules['inventory_repository_pb2'] = MagicMock()

from inventoryServiceHandler import *



class TestInventoryServiceHandler(unittest.TestCase):

    def testValidateItemService_success(self):
        context_mock = MagicMock()
        request = MagicMock(batch_id=123)
        sys.modules['inventory_repository_pb2_grpc'].InventoryRepositoryStub().getBatch().response_code = 0
        self.assertTrue(validateItemService(request,context_mock ))

    def testValidateItemService_fail(self):
        sys.modules['inventory_repository_pb2_grpc'].InventoryRepositoryStub().getBatch().response_code = MagicMock()
        sys.modules['inventory_service_pb2'].ValidateItemServiceResponse().response_code = 1
        context_mock = MagicMock()
        request = MagicMock(batch_id = 1)
        response= validateItemService(request, context_mock)
        self.assertEqual(response.response_code, 1)

    def testgetBatchCostService_success(self):
        context_mock = MagicMock()
        sys.modules['inventory_repository_pb2_grpc'].InventoryRepositoryStub().getBatchCost().response_code = MagicMock()
        sys.modules['inventory_service_pb2'].GetBatchCostServiceResponse().response_code = 0
        sys.modules['inventory_service_pb2'].GetBatchCostServiceResponse().cost = "131"
        request = MagicMock(cost = "131")
        response= getBatchCostService(request, context_mock)
        self.assertEqual(response.response_code, 0)
        self.assertEqual(response.cost, "131")

    def testgetBatchCostService_fail(self):
        context_mock = MagicMock()
        sys.modules['inventory_repository_pb2_grpc'].InventoryRepositoryStub().getBatchCost().response_code = MagicMock()
        sys.modules['inventory_service_pb2'].GetBatchCostServiceResponse().response_code = 1
        request = MagicMock(cost = "131")
        response= getBatchCostService(request, context_mock)
        self.assertEqual(response.response_code, 1)
        
    def testgetBatchScoreService_success(self):
        context_mock = MagicMock()
        sys.modules['inventory_repository_pb2_grpc'].InventoryRepositoryStub().getBatchScore().response_code = MagicMock()
        sys.modules['inventory_service_pb2'].GetBatchScoreServiceResponse().response_code = 0
        sys.modules['inventory_service_pb2'].GetBatchScoreServiceResponse().score = "5"
        request = MagicMock(score="5")
        response= getBatchScoreService(request, context_mock)
        self.assertEqual(response.response_code, 0)
        self.assertEqual(response.score, "5")

    def testgetBatchScoreService_fail(self):
        context_mock = MagicMock()
        sys.modules['inventory_repository_pb2_grpc'].InventoryRepositoryStub().getBatchScore().response_code = MagicMock()
        sys.modules['inventory_service_pb2'].GetBatchScoreServiceResponse().response_code = 1
        request = MagicMock(score="5")
        response= getBatchScoreService(request, context_mock)
        self.assertEqual(response.response_code, 1)
        
    def testgetBatchUsersReviewService_success(self):
        context_mock = MagicMock()
        sys.modules['inventory_repository_pb2_grpc'].InventoryRepositoryStub().getBatchUsersReview().response_code = MagicMock()
        sys.modules['inventory_service_pb2'].GetBatchUsersReviewServiceResponse().response_code = 0
        sys.modules['inventory_service_pb2'].GetBatchUsersReviewServiceResponse().n_users_review = "5"
        request = MagicMock(n_users_review="5")
        response= getBatchUsersReviewService(request, context_mock)
        self.assertEqual(response.response_code, 0)
        self.assertEqual(response.n_users_review, "5")

    def testgetBatchUsersReviewService_fail(self):
        context_mock = MagicMock()
        sys.modules['inventory_repository_pb2_grpc'].InventoryRepositoryStub().getBatchUsersReview().response_code = MagicMock()
        sys.modules['inventory_service_pb2'].GetBatchUsersReviewServiceResponse().response_code = 1
        request = MagicMock(n_users_review="5")
        response= getBatchUsersReviewService(request, context_mock)
        self.assertEqual(response.response_code, 1)

    def testgetBatchService_success(self):
        context_mock = MagicMock()
        sys.modules['inventory_repository_pb2_grpc'].InventoryRepositoryStub().getBatch().response_code = MagicMock()
        sys.modules['inventory_service_pb2'].GetBatchServiceResponse().response_code = 0
        request = MagicMock()
        response= getBatchService(request, context_mock)
        self.assertEqual(response.response_code, 0)
        
    def testgetBatchService_fail(self):
        context_mock = MagicMock()
        sys.modules['inventory_repository_pb2_grpc'].InventoryRepositoryStub().getBatch().response_code = MagicMock()
        sys.modules['inventory_service_pb2'].GetBatchServiceResponse().response_code = 1
        request = MagicMock()
        response= getBatchService(request, context_mock)
        self.assertEqual(response.response_code, 1)
        
 
    def testgetBatchesService_success(self):
        context_mock = MagicMock()
        sys.modules['inventory_repository_pb2_grpc'].InventoryRepositoryStub().getBatches().response_code = MagicMock()
        sys.modules['inventory_service_pb2'].GetBatchesServiceResponse().response_code = 0
        request = MagicMock()
        response= getBatchesService(request, context_mock)
        self.assertEqual(response.response_code, 0)

    def testgetBatchesService_fail(self):
        context_mock = MagicMock()
        sys.modules['inventory_repository_pb2_grpc'].InventoryRepositoryStub().getBatches().response_code = MagicMock()
        sys.modules['inventory_service_pb2'].GetBatchesServiceResponse().response_code = 1
        request = MagicMock()
        response= getBatchesService(request, context_mock)
        self.assertEqual(response.response_code, 1)

    def testupdateScoreService_success(self):
        context_mock = MagicMock()
        sys.modules['inventory_repository_pb2_grpc'].InventoryRepositoryStub().updateUserScore().response_code = 0
        sys.modules['inventory_service_pb2'].UpdateScoreServiceResponse().response_code = 0
        request = MagicMock()
        response= updateScoreService(request, context_mock)
        self.assertEqual(response.response_code, 0)

    def testupdateScoreService_fail(self):
        context_mock = MagicMock()
        sys.modules['inventory_repository_pb2_grpc'].InventoryRepositoryStub().updateUserScore().response_code = 1
        sys.modules['inventory_service_pb2'].UpdateScoreServiceResponse().response_code = 1
        request = MagicMock()
        response= updateScoreService(request, context_mock)
        self.assertEqual(response.response_code, 1)

    def testvalidateOrderService_volume_exceeds(self):
        sys.modules['inventory_repository_pb2'].GetVolumeRequest().response_code = 0
        sys.modules['inventory_repository_pb2_grpc'].InventoryRepositoryStub().getBatchVolume().response_code = 0
        sys.modules['inventory_repository_pb2_grpc'].InventoryRepositoryStub().getBatchVolume().volume = 0
        sys.modules['inventory_service_pb2'].ValidateOrderServiceResponse().response_code = 1
        context_mock = MagicMock()
        request = MagicMock()
        request.volume_order = 1
        response= validateOrderService(request, context_mock)
        self.assertEqual(response.response_code, 1)

    def testvalidateOrderService_success(self):
        sys.modules['inventory_repository_pb2'].GetVolumeRequest().response_code = 0
        sys.modules['inventory_repository_pb2_grpc'].InventoryRepositoryStub().getBatchVolume().response_code = 0
        sys.modules['inventory_repository_pb2_grpc'].InventoryRepositoryStub().getBatchVolume().volume = 1
        sys.modules['inventory_service_pb2'].ValidateOrderServiceResponse().response_code = 0
        context_mock = MagicMock()
        request = MagicMock()
        request.volume_order = 0
        response= validateOrderService(request, context_mock)
        self.assertEqual(response.response_code, 0)

    def testvalidateOrderService_failure(self):
        sys.modules['inventory_repository_pb2'].GetVolumeRequest().response_code = 1
        sys.modules['inventory_repository_pb2_grpc'].InventoryRepositoryStub().getBatchVolume().response_code = 1
        sys.modules['inventory_service_pb2'].ValidateOrderServiceResponse().response_code = 1
        context_mock = MagicMock()
        request = MagicMock()
        response= validateOrderService(request, context_mock)
        self.assertEqual(response.response_code, 1)   
         
    
    def test_updateVolume_success(self):
        sys.modules['inventory_repository_pb2'].GetVolumeRequest().response_code = 0
        sys.modules['inventory_repository_pb2_grpc'].InventoryRepositoryStub().getBatchVolume().response_code = 0
        sys.modules['inventory_repository_pb2'].UpdateVolumeRequest().response_code = 0
        sys.modules['inventory_repository_pb2_grpc'].InventoryRepositoryStub().updateVolume().response_code = 0
        sys.modules['inventory_service_pb2'].UpdateVolumeServiceResponse().response_code = 0
        mock_context = MagicMock()
        request = MagicMock()
        response = updateVolumeService(request, mock_context)
        self.assertEqual(response.response_code, 0)

    def test_updateVolume_subtract_error(self):
        sys.modules['inventory_repository_pb2'].GetVolumeRequest().response_code = 0
        sys.modules['inventory_repository_pb2_grpc'].InventoryRepositoryStub().getBatchVolume().response_code = 0
        sys.modules['inventory_repository_pb2'].UpdateVolumeRequest().response_code = 1
        sys.modules['inventory_repository_pb2_grpc'].InventoryRepositoryStub().updateVolume().response_code = 1
        sys.modules['inventory_service_pb2'].UpdateVolumeServiceResponse().response_code = 1
        mock_context = MagicMock()
        request = MagicMock()
        response = updateVolumeService(request, mock_context)
        self.assertEqual(response.response_code, 1)

    def test_updateVolume_failure(self):
        sys.modules['inventory_repository_pb2'].GetVolumeRequest().response_code = 1
        sys.modules['inventory_repository_pb2_grpc'].InventoryRepositoryStub().getBatchVolume().response_code = 1
        sys.modules['inventory_service_pb2'].UpdateVolumeServiceResponse().response_code = 1
        mock_context = MagicMock()
        request = MagicMock()
        response = updateVolumeService(request, mock_context)
        self.assertEqual(response.response_code, 1)


if __name__ == '__main__':
    with open('./test-reports/inventory_service_tests.xml', 'wb') as output:
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=output))