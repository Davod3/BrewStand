import unittest
from unittest.mock import MagicMock, patch
import sys
import xmlrunner

sys.modules['user_repository_pb2'] = MagicMock()
sys.modules['user_service_pb2'] = MagicMock()
sys.modules['user_repository_pb2_grpc'] = MagicMock()
sys.modules['handlers.itemHandler'] = MagicMock()
sys.modules['handlers'] = MagicMock()
sys.modules['ItemHandler'] = MagicMock()

username="testeAPP"
address = "Lisboa"
user_id = 1234
batch_id = 555
volume = 50
from userHandler import *

class TestUserHandler(unittest.TestCase):

     # def test_valid_username(self):

    #     valid_usernames = ["username", "user123", "user_name"]
    #     for username in valid_usernames:
    #         self.assertTrue(__validateUsername(username))

    # def test_invalid_username_length(self):

    #     invalid_usernames = ["us", "use", "___"]
    #     for username in invalid_usernames:
    #         self.assertFalse(__validateUsername(username))

    # def test_invalid_username_characters(self):
 
    #     invalid_usernames = ["user name", "user-name", "user@name"]
    #     for username in invalid_usernames:
    #         self.assertFalse(__validateUsername(username))
    

    @patch('userHandler.client.InsertUser')
    @patch('userHandler.__getToken')
    @patch('userHandler.__validateUsername')
    def test_register_user_success(self, mock_validateUsername, mock_getToken, mock_InsertUser):
        mock_validateUsername.return_value = True
        mock_getToken.return_value = "fake_token_success"
        mock_response = MagicMock()
        mock_response.response_code = 0
        mock_InsertUser.return_value = mock_response

        result = registerUser(username=username, address=address)

        expected_result = (0, "fake_token_success")
        self.assertEqual(result, expected_result)


    @patch('userHandler.client.InsertUser')
    @patch('userHandler.__getToken')
    @patch('userHandler.__validateUsername')
    def test_register_user_bad_credentials(self, mock_validateUsername, mock_getToken, mock_InsertUser):
        mock_validateUsername.return_value = False

        result = registerUser(username=1234, address="Not necessary")

        expected_result = (2, '')
        self.assertEqual(result, expected_result)

    @patch('userHandler.client.InsertUser')
    @patch('userHandler.__getToken')
    @patch('userHandler.__validateUsername')
    def test_register_user_token_failure(self, mock_validateUsername, mock_getToken, mock_InsertUser):
        mock_validateUsername.return_value = True
        mock_getToken.return_value = None

        result = registerUser(username=username, address=address)

        expected_result = (3, '')
        self.assertEqual(result, expected_result)

    @patch('userHandler.client.InsertUser')
    @patch('userHandler.__getToken')
    @patch('userHandler.__validateUsername')
    def test_register_user_already_exist(self, mock_validateUsername, mock_getToken, mock_InsertUser):
        # Mocking successful validation and token retrieval, but failure in user insertion
        mock_validateUsername.return_value = True
        mock_getToken.return_value = "fake_token"
        mock_response = MagicMock()
        mock_response.response_code = 1  
        mock_InsertUser.return_value = mock_response

        result = registerUser(username="André", address=address)

        expected_result = (1, 'fake_token')
        self.assertEqual(result, expected_result)



    @patch('userHandler.client.GetUser')
    def test_get_user_by_id_success(self, mock_GetUser):
        mock_response = MagicMock()
        mock_response.user_id = 123
        mock_response.response_code = 0
        mock_response.username = username
        mock_response.address=address
        mock_GetUser.return_value = mock_response

        result = getUserByID(user_id=123)

        self.assertEqual(result, mock_response)
    



    @patch('userHandler.client.GetUser')
    def test_get_user_by_id_failure(self, mock_GetUser):
        mock_response = MagicMock()
        mock_response.response_code=1
        mock_GetUser.return_value = None

        result = getUserByID(user_id=123)

        self.assertIsNone(result,mock_response)

    @patch('userHandler.client.GetUserByToken')
    def test_trade_token_success(self, mock_GetUserByToken):

        mock_response = MagicMock()
        mock_response.response_code = 0
        mock_response.user_id = 123  
        mock_GetUserByToken.return_value = mock_response

        result = tradeToken(token='dummy_token')

        self.assertEqual(result, (0, 123))

    @patch('userHandler.client.GetUserByToken')
    def test_trade_token_failure(self, mock_GetUserByToken):

        mock_response = MagicMock()
        mock_response.response_code = 1  
        mock_GetUserByToken.return_value = mock_response

        result = tradeToken(token='dummy_token')

        self.assertEqual(result, (1, ''))

    @patch('userHandler.ItemHandler')
    def test_add_to_cart_valid_item(self, mock_UserCartAdd):

        mock_UserCartAdd.validateItem.return_value = 0
        sys.modules['user_repository_pb2_grpc'].UserRepositoryStub().UserCartAdd().response_code = 0
        self.assertEqual(addToCart(user_id, batch_id, volume),0)
    
    @patch('userHandler.ItemHandler')
    def test_add_to_cart_valid_item_zero_volume(self, mock_UserCartAdd):

        mock_UserCartAdd.validateItem.return_value = 0
        sys.modules['user_repository_pb2_grpc'].UserRepositoryStub().UserCartAdd().response_code = 3
        self.assertEqual(addToCart(user_id, batch_id, 0),3)

    @patch('userHandler.ItemHandler')
    def test_add_to_cart_valid_item_no_exist(self, mock_UserCartAdd):

        mock_UserCartAdd.validateItem.return_value = 1
        sys.modules['user_repository_pb2_grpc'].UserRepositoryStub().UserCartAdd().response_code = 1
        self.assertEqual(addToCart(user_id, 1, volume),1)

    @patch('userHandler.ItemHandler.getBatchCost')
    @patch('userHandler.client')
    def test_get_cart_successful_response(self, mock_client, mock_getBatchCost):
        # Create a mock response object
        mock_response = MagicMock()
        mock_response.response_code = 0
        mock_response.content = [
            MagicMock(batch_id=1, volume=10), 
            MagicMock(batch_id=2, volume=20)
        ]
        mock_client.UserCartGet.return_value = mock_response

        user_id = "valid_user_id"
        mock_getBatchCost.return_value = 20

        result = getCartContent(user_id)
        expected_result = (0, [
            CartContent(batch_id=1, volume=10),
            CartContent(batch_id=2, volume=20)
            ], 600)

        self.assertEqual(result, expected_result)



    @patch('userHandler.client.UserCartGet')
    def test_get_cart_content_user_not_found(self, mock_UserCartGet):
        mock_response = MagicMock()
        mock_response.response_code = 1  
        mock_UserCartGet.return_value = mock_response

        result = getCartContent(user_id=123)

        expected_result = (1, [], 0)
        self.assertEqual(result, expected_result)

    @patch('userHandler.client.UserCartDelete')
    def test_delete_from_cart_success(self, mock_UserCartDelete):

        mock_response = MagicMock()
        mock_response.response_code = 0
        mock_UserCartDelete.return_value = mock_response


        result = deleteFromCart(user_id=123, batch_id=555)

        self.assertEqual(result, 0)

    @patch('userHandler.client.UserCartDelete')
    def test_delete_from_cart_default_user_not_found(self, mock_UserCartDelete):

        mock_response = MagicMock()
        mock_response.response_code = 1
        mock_UserCartDelete.return_value = mock_response

        result = deleteFromCart(37817382,89898)

        self.assertEqual(result, 1)

    @patch('userHandler.client.UserCartDelete')
    def test_delete_from_cart_default_batch_not_found(self, mock_UserCartDelete):
        
        mock_response = MagicMock()
        mock_response.response_code = 2
        mock_UserCartDelete.return_value = mock_response

        result = deleteFromCart(123,89898)

        self.assertEqual(result, 2)


    # @patch('userHandler.http.client.HTTPSConnection')
    # def test_get_token_success(self, mock_https_conn):
    #     mock_response = MagicMock()
    #     mock_response.status = 200
    #     mock_response.read.return_value = b'{"access_token": "test_token"}'
    #     mock_https_conn.return_value.getresponse.return_value = mock_response

    #     token = __getToken()

    #     self.assertEqual(token, "test_token")

    # @patch('userHandler.http.client.HTTPSConnection')
    # def test_get_token_failure(self, mock_https_conn):
    #     mock_response = MagicMock()
    #     mock_response.status = 404
    #     mock_https_conn.return_value.getresponse.return_value = mock_response

    #     token = __getToken()

    #     self.assertIsNone(token)


if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
