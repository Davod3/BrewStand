import unittest
from unittest.mock import MagicMock, patch
from cartHandler import *
import sys
import xmlrunner

sys.modules['models.user'] = MagicMock()

class TestAddToCart(unittest.TestCase):

    @patch('cartHandler.User.objects')
    def test_invalid_user(self, mock_objects):
        mock_objects.with_id.return_value = None

        user_id = "invalid_user_id"
        batch_id = 123
        volume = 1

        result = addToCart(user_id, batch_id, volume)

        self.assertEqual(result, 1)

    @patch('cartHandler.User.objects')
    def test_item_not_in_cart(self, mock_objects):
        mock_user = MagicMock()
        mock_user.cart = []
        mock_objects.with_id.return_value = mock_user

        user_id = "valid_user_id"
        batch_id = 123
        volume = 2

        result = addToCart(user_id, batch_id, volume)

        self.assertEqual(result, 0)

    @patch('cartHandler.User.objects')
    def test_item_already_in_cart(self, mock_objects):
        mock_user = MagicMock()
        mock_user.cart = [CartItem(batch_id=123, volume=5)]
        mock_objects.with_id.return_value = mock_user

        user_id = "valid_user_id"
        batch_id = 123
        volume = 2

        result = addToCart(user_id, batch_id, volume)

        self.assertEqual(result, 0)

    @patch('cartHandler.User.objects')
    def test_valid_user_cart(self, mock_objects):
        mock_user = MagicMock()
        mock_user.cart = [CartItem(batch_id=123, volume=5)]
        mock_objects.with_id.return_value = mock_user

        user_id = "valid_user_id"

        result = getCart(user_id)

        self.assertEqual(result, mock_user.cart)

    @patch('cartHandler.User.objects')
    def test_invalid_user_cart(self, mock_objects):
        mock_objects.with_id.return_value = None

        user_id = "invalid_user_id"

        result = getCart(user_id)

        self.assertEqual(result, None)

    @patch('cartHandler.User.objects')
    def test_invalid_user_remove(self, mock_objects):
        mock_objects.with_id.return_value = None

        user_id = "invalid_user_id"
        batch_id = 123

        result = removeFromCart(user_id, batch_id)

        self.assertEqual(result, 1)

    @patch('cartHandler.User.objects')
    def test_remove_whole_cart(self, mock_objects):
        mock_user = MagicMock()
        mock_user.cart = [CartItem(batch_id=123, volume=5)]
        mock_objects.with_id.return_value = mock_user

        user_id = "valid_user_id"
        batch_id = 0

        result = removeFromCart(user_id, batch_id)

        self.assertEqual(result, 0)
        self.assertEqual(mock_user.cart, [])

    @patch('cartHandler.User.objects')
    def test_remove_item_from_cart(self, mock_objects):
        mock_user = MagicMock()
        mock_user.cart = [CartItem(batch_id=123, volume=5)]
        mock_objects.with_id.return_value = mock_user

        user_id = "valid_user_id"
        batch_id = 123

        result = removeFromCart(user_id, batch_id)

        self.assertEqual(result, 0)
        self.assertNotIn(CartItem(batch_id=123, volume=5), mock_user.cart)
        self.assertEqual(mock_user.cart, [])

    @patch('cartHandler.User.objects')
    def test_remove_item_not_in_cart(self, mock_objects):
        mock_user = MagicMock()
        mock_user.cart = [CartItem(batch_id=123, volume=5)]
        mock_objects.with_id.return_value = mock_user

        user_id = "valid_user_id"
        batch_id = 456

        result = removeFromCart(user_id, batch_id)

        self.assertEqual(result, 2)
        self.assertEqual(mock_user.cart, [CartItem(batch_id=123, volume=5)])

if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
