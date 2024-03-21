# THIS CODE WAS AUTO GENERATED BY SWAGGER EDITOR

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from models.base_model_ import Model
from utils import util


class Invoice(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, invoice_id: int=None, price: float=None, order_id: int=None, customer_id: int=None, fiscal_address: str=None, details: str=None):  # noqa: E501
        """Invoice - a model defined in Swagger

        :param invoice_id: The invoice_id of this Invoice.  # noqa: E501
        :type invoice_id: int
        :param price: The price of this Invoice.  # noqa: E501
        :type price: float
        :param order_id: The order_id of this Invoice.  # noqa: E501
        :type order_id: int
        :param customer_id: The customer_id of this Invoice.  # noqa: E501
        :type customer_id: int
        :param fiscal_address: The fiscal_address of this Invoice.  # noqa: E501
        :type fiscal_address: str
        :param details: The details of this Invoice.  # noqa: E501
        :type details: str
        """
        self.swagger_types = {
            'invoice_id': int,
            'price': float,
            'order_id': int,
            'customer_id': int,
            'fiscal_address': str,
            'details': str
        }

        self.attribute_map = {
            'invoice_id': 'invoiceID',
            'price': 'price',
            'order_id': 'orderID',
            'customer_id': 'customerID',
            'fiscal_address': 'fiscalAddress',
            'details': 'details'
        }
        self._invoice_id = invoice_id
        self._price = price
        self._order_id = order_id
        self._customer_id = customer_id
        self._fiscal_address = fiscal_address
        self._details = details

    @classmethod
    def from_dict(cls, dikt) -> 'Invoice':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Invoice of this Invoice.  # noqa: E501
        :rtype: Invoice
        """
        return util.deserialize_model(dikt, cls)

    @property
    def invoice_id(self) -> int:
        """Gets the invoice_id of this Invoice.

        A unique identifier assigned to each invoice processed.  # noqa: E501

        :return: The invoice_id of this Invoice.
        :rtype: int
        """
        return self._invoice_id

    @invoice_id.setter
    def invoice_id(self, invoice_id: int):
        """Sets the invoice_id of this Invoice.

        A unique identifier assigned to each invoice processed.  # noqa: E501

        :param invoice_id: The invoice_id of this Invoice.
        :type invoice_id: int
        """

        self._invoice_id = invoice_id

    @property
    def price(self) -> float:
        """Gets the price of this Invoice.

        The total cost for the order.  # noqa: E501

        :return: The price of this Invoice.
        :rtype: float
        """
        return self._price

    @price.setter
    def price(self, price: float):
        """Sets the price of this Invoice.

        The total cost for the order.  # noqa: E501

        :param price: The price of this Invoice.
        :type price: float
        """

        self._price = price

    @property
    def order_id(self) -> int:
        """Gets the order_id of this Invoice.

        The order id. Used for tracking purposes.  # noqa: E501

        :return: The order_id of this Invoice.
        :rtype: int
        """
        return self._order_id

    @order_id.setter
    def order_id(self, order_id: int):
        """Sets the order_id of this Invoice.

        The order id. Used for tracking purposes.  # noqa: E501

        :param order_id: The order_id of this Invoice.
        :type order_id: int
        """

        self._order_id = order_id

    @property
    def customer_id(self) -> int:
        """Gets the customer_id of this Invoice.

        The id of the user who initiated the payment process.  # noqa: E501

        :return: The customer_id of this Invoice.
        :rtype: int
        """
        return self._customer_id

    @customer_id.setter
    def customer_id(self, customer_id: int):
        """Sets the customer_id of this Invoice.

        The id of the user who initiated the payment process.  # noqa: E501

        :param customer_id: The customer_id of this Invoice.
        :type customer_id: int
        """

        self._customer_id = customer_id

    @property
    def fiscal_address(self) -> str:
        """Gets the fiscal_address of this Invoice.

        The address used for billing purposes.  # noqa: E501

        :return: The fiscal_address of this Invoice.
        :rtype: str
        """
        return self._fiscal_address

    @fiscal_address.setter
    def fiscal_address(self, fiscal_address: str):
        """Sets the fiscal_address of this Invoice.

        The address used for billing purposes.  # noqa: E501

        :param fiscal_address: The fiscal_address of this Invoice.
        :type fiscal_address: str
        """

        self._fiscal_address = fiscal_address

    @property
    def details(self) -> str:
        """Gets the details of this Invoice.

        Optional details and extra notes about the order.  # noqa: E501

        :return: The details of this Invoice.
        :rtype: str
        """
        return self._details

    @details.setter
    def details(self, details: str):
        """Sets the details of this Invoice.

        Optional details and extra notes about the order.  # noqa: E501

        :param details: The details of this Invoice.
        :type details: str
        """

        self._details = details
