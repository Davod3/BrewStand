import unittest
from unittest.mock import MagicMock, patch
import xmlrunner
import sys


sys.modules['inventory_service_pb2'] = MagicMock()
sys.modules['inventory_service_pb2_grpc'] = MagicMock()
sys.modules['handlers'] = MagicMock()
sys.modules['handlers.itemHandlerReview'] = MagicMock()
sys.modules['ItemHandlerReview'] = MagicMock()  

from reviewHandler import review
from itemHandlerReview import getBatchScore, getNvotos, validateBatch, updateScore

batch_id = 123

class TestReviewHandler(unittest.TestCase):

    #########################################___________ITEMHANDLERREVIEW___________________###########################################

    def test_validateBatch_batch_exists(self):
        sys.modules['inventory_service_pb2_grpc'].InventoryServiceStub().validateItemService().response_code = 0
        self.assertTrue(validateBatch(batch_id))

    def test_validateBatch_batch_not_exists(self):
        sys.modules['inventory_service_pb2_grpc'].InventoryServiceStub().validateItemService().response_code = 1
        self.assertFalse(validateBatch(batch_id))

    def test_getBatchScore(self):
        sys.modules['inventory_service_pb2_grpc'].InventoryServiceStub().getBatchScoreService().score = 10
        self.assertEqual(getBatchScore(batch_id), 10)

    def test_getNvotos(self):
        sys.modules['inventory_service_pb2_grpc'].InventoryServiceStub().getBatchUsersReviewService().n_users_review = 50
        self.assertEqual(getNvotos(batch_id), 50)

    def test_updateScore(self):
        sys.modules['inventory_service_pb2_grpc'].InventoryServiceStub().updateScoreService().response_code = 8
        self.assertEqual(updateScore(batch_id, 8), 8)



    #########################################___________REVIEWHANDLER___________________###########################################
    

    
  
    @patch('reviewHandler.ItemHandlerReview')
    def test_review_valid_score_item_exists(self, mock_itemHandlerReview):

        batch_id = 123
        
        mock_itemHandlerReview.validateBatch.return_value = True
        mock_itemHandlerReview.getBatchScore.return_value = 7
        mock_itemHandlerReview.getNvotos.return_value = 1
        mock_itemHandlerReview.updateScore.return_value = 7.5

        self.assertEqual(review(batch_id, 8), 7.5)

    @patch('reviewHandler.ItemHandlerReview')
    def test_review_invalid_score_item(self, mock_itemHandlerReview):

        batch_id = 123
        
        mock_itemHandlerReview.validateBatch.return_value = True
        mock_itemHandlerReview.getBatchScore.return_value = 11

        self.assertEqual(review(batch_id, 11),1)


    @patch('reviewHandler.ItemHandlerReview')
    def test_review_valid_score_item_not_exists(self, mock_itemHandlerReview):


        mock_itemHandlerReview.validateBatch.return_value = False
        mock_itemHandlerReview.getBatchScore.return_value = 7

        self.assertEqual(review(12345, 7),2)



if __name__ == '__main__':
    with open('./test-reports/review_service_tests.xml', 'wb') as output:
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=output))