import unittest
from unittest.mock import MagicMock, patch
import xmlrunner
import sys

sys.modules['handlers'] = MagicMock()
sys.modules['handlers.itemHandlerReview'] = MagicMock()
sys.modules['itemHandlerReview'] = MagicMock()

from reviewHandler import review

class TestReviewHandler(unittest.TestCase):

    @patch('reviewHandler.itemHandlerReview')
    def test_review_valid_score_item_exists(self, mock_itemHandlerReview):

        batch_id = 123
        
        mock_itemHandlerReview.validateBatch.return_value = True
        mock_itemHandlerReview.getBatchScore.return_value = 7
        mock_itemHandlerReview.getNvotos.return_value = 1
        mock_itemHandlerReview.updateScore.return_value = 7.5

        self.assertEqual(review(batch_id, 8), 7.5)

    @patch('reviewHandler.itemHandlerReview')
    def test_review_invalid_score_item(self, mock_itemHandlerReview):

        batch_id = 123
        
        mock_itemHandlerReview.validateBatch.return_value = True
        mock_itemHandlerReview.getBatchScore.return_value = 11

        self.assertEqual(review(batch_id, 11),1)

    @patch('reviewHandler.itemHandlerReview')
    def test_review_valid_score_item_not_exists(self, mock_itemHandlerReview):

        
        mock_itemHandlerReview.validateBatch.return_value = False
        mock_itemHandlerReview.getBatchScore.return_value = 7

        self.assertEqual(review(12345, 7),2)

if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))