# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from models.base_model_ import Model
from utils import util


class CartPaymentBody(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, card_number: str=None, card_expiry: str=None, card_cvc: str=None):  # noqa: E501
        """CartPaymentBody - a model defined in Swagger

        :param card_number: The card_number of this CartPaymentBody.  # noqa: E501
        :type card_number: str
        :param card_expiry: The card_expiry of this CartPaymentBody.  # noqa: E501
        :type card_expiry: str
        :param card_cvc: The card_cvc of this CartPaymentBody.  # noqa: E501
        :type card_cvc: str
        """
        self.swagger_types = {
            'card_number': str,
            'card_expiry': str,
            'card_cvc': str
        }

        self.attribute_map = {
            'card_number': 'cardNumber',
            'card_expiry': 'cardExpiry',
            'card_cvc': 'cardCvc'
        }
        self._card_number = card_number
        self._card_expiry = card_expiry
        self._card_cvc = card_cvc

    @classmethod
    def from_dict(cls, dikt) -> 'CartPaymentBody':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The cart_payment_body of this CartPaymentBody.  # noqa: E501
        :rtype: CartPaymentBody
        """
        return util.deserialize_model(dikt, cls)

    @property
    def card_number(self) -> str:
        """Gets the card_number of this CartPaymentBody.


        :return: The card_number of this CartPaymentBody.
        :rtype: str
        """
        return self._card_number

    @card_number.setter
    def card_number(self, card_number: str):
        """Sets the card_number of this CartPaymentBody.


        :param card_number: The card_number of this CartPaymentBody.
        :type card_number: str
        """

        self._card_number = card_number

    @property
    def card_expiry(self) -> str:
        """Gets the card_expiry of this CartPaymentBody.


        :return: The card_expiry of this CartPaymentBody.
        :rtype: str
        """
        return self._card_expiry

    @card_expiry.setter
    def card_expiry(self, card_expiry: str):
        """Sets the card_expiry of this CartPaymentBody.


        :param card_expiry: The card_expiry of this CartPaymentBody.
        :type card_expiry: str
        """

        self._card_expiry = card_expiry

    @property
    def card_cvc(self) -> str:
        """Gets the card_cvc of this CartPaymentBody.


        :return: The card_cvc of this CartPaymentBody.
        :rtype: str
        """
        return self._card_cvc

    @card_cvc.setter
    def card_cvc(self, card_cvc: str):
        """Sets the card_cvc of this CartPaymentBody.


        :param card_cvc: The card_cvc of this CartPaymentBody.
        :type card_cvc: str
        """

        self._card_cvc = card_cvc
