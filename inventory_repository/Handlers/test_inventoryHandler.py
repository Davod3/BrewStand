import unittest
from unittest.mock import MagicMock, patch
import grpc
import sys
import xmlrunner

sys.modules['inventory_repository_pb2'] = MagicMock()

from inventoryHandler import *


class TestOrderService(unittest.TestCase):

    @patch('psycopg2.connect')
    def test_getBatchCost_success(self, conn):
        sys.modules['inventory_repository_pb2'].GetBatchCostResponse().response_code = 0
        conn = MagicMock()
        mock_context = MagicMock()
        request = MagicMock()
        response = getBatchCost(request, mock_context)
        self.assertEqual(response.response_code, 0)

    @patch('psycopg2.connect')
    def test_getBatchCost_failure(self, mock_connect):
        sys.modules['inventory_repository_pb2'].GetBatchCostResponse().response_code = 1
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        mock_context = MagicMock()
        request = MagicMock()
        response = getBatchCost(request, mock_context)
        self.assertEqual(response.response_code, 1)

    @patch('psycopg2.connect')
    def test_getBatchScore_success(self, conn):
        sys.modules['inventory_repository_pb2'].GetBatchScoreResponse().response_code = 0
        conn = MagicMock()
        mock_context = MagicMock()
        request = MagicMock()
        response = getBatchScore(request, mock_context)
        self.assertEqual(response.response_code, 0)

    @patch('psycopg2.connect')
    def test_getBatchScore_failure(self, mock_connect):
        sys.modules['inventory_repository_pb2'].GetBatchScoreResponse().response_code = 1
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        mock_context = MagicMock()
        request = MagicMock()
        response = getBatchScore(request, mock_context)
        self.assertEqual(response.response_code, 1)

    @patch('psycopg2.connect')
    def test_getBatchVolume_success(self, conn):
        sys.modules['inventory_repository_pb2'].GetVolumeResponse().response_code = 0
        conn = MagicMock()
        mock_context = MagicMock()
        request = MagicMock()
        response = getBatchVolume(request, mock_context)
        self.assertEqual(response.response_code, 0)

    @patch('psycopg2.connect')
    def test_getBatchVolume_failure(self, mock_connect):
        sys.modules['inventory_repository_pb2'].GetVolumeResponse().response_code = 1
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        mock_context = MagicMock()
        request = MagicMock()
        response = getBatchVolume(request, mock_context)
        self.assertEqual(response.response_code, 1)

    @patch('psycopg2.connect')
    def test_getBatchUsersReview_success(self, conn):
        sys.modules['inventory_repository_pb2'].GetBatchUsersReviewResponse().response_code = 0
        conn = MagicMock()
        mock_context = MagicMock()
        request = MagicMock()
        response = getBatchUsersReview(request, mock_context)
        self.assertEqual(response.response_code, 0)

    @patch('psycopg2.connect')
    def test_getBatchUsersReview_failure(self, mock_connect):
        sys.modules['inventory_repository_pb2'].GetBatchUsersReviewResponse().response_code = 1
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        mock_context = MagicMock()
        request = MagicMock()
        response = getBatchUsersReview(request, mock_context)
        self.assertEqual(response.response_code, 1)

    @patch('psycopg2.connect')
    def test_getBatch_success(self, conn):
        sys.modules['inventory_repository_pb2'].GetBatchResponse().response_code = 0
        conn = MagicMock()
        mock_context = MagicMock()
        request = MagicMock()
        response = getBatch(request, mock_context)
        self.assertEqual(response.response_code, 0)

    @patch('psycopg2.connect')
    def test_getBatch_failure(self, mock_connect):
        sys.modules['inventory_repository_pb2'].GetBatchResponse().response_code = 1
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        mock_context = MagicMock()
        request = MagicMock()
        response = getBatch(request, mock_context)
        self.assertEqual(response.response_code, 1)

    @patch('psycopg2.connect')
    def test_getBatches_success(self, conn):
        sys.modules['inventory_repository_pb2'].GetBatchesResponse().response_code = 0
        conn = MagicMock()
        mock_context = MagicMock()
        request = MagicMock()
        response = getBatches(request, mock_context)
        self.assertEqual(response.response_code, 0)

    @patch('psycopg2.connect')
    def test_getBatches_failure(self, mock_connect):
        sys.modules['inventory_repository_pb2'].GetBatchesResponse().response_code = 1
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        mock_context = MagicMock()
        request = MagicMock()
        response = getBatches(request, mock_context)
        self.assertEqual(response.response_code, 1)

    @patch('psycopg2.connect')
    def test_updateUserScore_success(self, mock_connect):
        sys.modules['inventory_repository_pb2'].UpdateUserScoreResponse().response_code = 0
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        mock_context = MagicMock()
        request = MagicMock()
        response = updateUserScore(request, mock_context)
        self.assertEqual(response.response_code, 0)

    @patch('psycopg2.connect')
    def test_updateUserScore_failure(self, mock_connect):
        sys.modules['inventory_repository_pb2'].UpdateUserScoreResponse().response_code = 1
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        mock_context = MagicMock()
        request = MagicMock()
        response = updateUserScore(request, mock_context)
        self.assertEqual(response.response_code, 1)

    @patch('psycopg2.connect')
    def test_updateVolume_success(self, mock_connect):
        sys.modules['inventory_repository_pb2'].UpdateVolumeResponse().response_code = 0
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        mock_context = MagicMock()
        request = MagicMock()
        response = updateVolume(request, mock_context)
        self.assertEqual(response.response_code, 0)

    @patch('psycopg2.connect')
    def test_updateVolume_failure(self, mock_connect):
        sys.modules['inventory_repository_pb2'].UpdateVolumeResponse().response_code = 1
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        mock_context = MagicMock()
        request = MagicMock()
        response = updateVolume(request, mock_context)
        self.assertEqual(response.response_code, 1)


if __name__ == '__main__':
    with open('./test-reports/inventory_repository_tests.xml', 'wb') as output:
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=output))