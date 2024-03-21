# THIS CODE WAS AUTO GENERATED BY SWAGGER EDITOR

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from models.base_model_ import Model
from models.order_items import OrderItems  # noqa: F401,E501
from utils import util


class Order(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, id: int=None, items: List[OrderItems]=None, ship_date: datetime=None, status: str=None, complete: bool=None, destination_address: str=None):  # noqa: E501
        """Order - a model defined in Swagger

        :param id: The id of this Order.  # noqa: E501
        :type id: int
        :param items: The items of this Order.  # noqa: E501
        :type items: List[OrderItems]
        :param ship_date: The ship_date of this Order.  # noqa: E501
        :type ship_date: datetime
        :param status: The status of this Order.  # noqa: E501
        :type status: str
        :param complete: The complete of this Order.  # noqa: E501
        :type complete: bool
        :param destination_address: The destination_address of this Order.  # noqa: E501
        :type destination_address: str
        """
        self.swagger_types = {
            'id': int,
            'items': List[OrderItems],
            'ship_date': datetime,
            'status': str,
            'complete': bool,
            'destination_address': str
        }

        self.attribute_map = {
            'id': 'id',
            'items': 'items',
            'ship_date': 'shipDate',
            'status': 'status',
            'complete': 'complete',
            'destination_address': 'destinationAddress'
        }
        self._id = id
        self._items = items
        self._ship_date = ship_date
        self._status = status
        self._complete = complete
        self._destination_address = destination_address

    @classmethod
    def from_dict(cls, dikt) -> 'Order':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Order of this Order.  # noqa: E501
        :rtype: Order
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this Order.

        The order id  # noqa: E501

        :return: The id of this Order.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this Order.

        The order id  # noqa: E501

        :param id: The id of this Order.
        :type id: int
        """

        self._id = id

    @property
    def items(self) -> List[OrderItems]:
        """Gets the items of this Order.


        :return: The items of this Order.
        :rtype: List[OrderItems]
        """
        return self._items

    @items.setter
    def items(self, items: List[OrderItems]):
        """Sets the items of this Order.


        :param items: The items of this Order.
        :type items: List[OrderItems]
        """

        self._items = items

    @property
    def ship_date(self) -> datetime:
        """Gets the ship_date of this Order.

        The date the order was sent to shipping  # noqa: E501

        :return: The ship_date of this Order.
        :rtype: datetime
        """
        return self._ship_date

    @ship_date.setter
    def ship_date(self, ship_date: datetime):
        """Sets the ship_date of this Order.

        The date the order was sent to shipping  # noqa: E501

        :param ship_date: The ship_date of this Order.
        :type ship_date: datetime
        """

        self._ship_date = ship_date

    @property
    def status(self) -> str:
        """Gets the status of this Order.

        The status of the order  # noqa: E501

        :return: The status of this Order.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status: str):
        """Sets the status of this Order.

        The status of the order  # noqa: E501

        :param status: The status of this Order.
        :type status: str
        """
        allowed_values = ["placed", "approved", "delivered"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def complete(self) -> bool:
        """Gets the complete of this Order.


        :return: The complete of this Order.
        :rtype: bool
        """
        return self._complete

    @complete.setter
    def complete(self, complete: bool):
        """Sets the complete of this Order.


        :param complete: The complete of this Order.
        :type complete: bool
        """

        self._complete = complete

    @property
    def destination_address(self) -> str:
        """Gets the destination_address of this Order.

        The address to where the order will be sent.  # noqa: E501

        :return: The destination_address of this Order.
        :rtype: str
        """
        return self._destination_address

    @destination_address.setter
    def destination_address(self, destination_address: str):
        """Sets the destination_address of this Order.

        The address to where the order will be sent.  # noqa: E501

        :param destination_address: The destination_address of this Order.
        :type destination_address: str
        """

        self._destination_address = destination_address
