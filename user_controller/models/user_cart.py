# THIS CODE WAS AUTO GENERATED BY SWAGGER EDITOR

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from models.base_model_ import Model
from models.order_items import OrderItems  # noqa: F401,E501
from utils import util


class UserCart(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, items: List[OrderItems]=None, total_cost: float=None):  # noqa: E501
        """UserCart - a model defined in Swagger

        :param items: The items of this UserCart.  # noqa: E501
        :type items: List[OrderItems]
        :param total_cost: The total_cost of this UserCart.  # noqa: E501
        :type total_cost: float
        """
        self.swagger_types = {
            'items': List[OrderItems],
            'total_cost': float
        }

        self.attribute_map = {
            'items': 'items',
            'total_cost': 'totalCost'
        }
        self._items = items
        self._total_cost = total_cost

    @classmethod
    def from_dict(cls, dikt) -> 'UserCart':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The UserCart of this UserCart.  # noqa: E501
        :rtype: UserCart
        """
        return util.deserialize_model(dikt, cls)

    @property
    def items(self) -> List[OrderItems]:
        """Gets the items of this UserCart.


        :return: The items of this UserCart.
        :rtype: List[OrderItems]
        """
        return self._items

    @items.setter
    def items(self, items: List[OrderItems]):
        """Sets the items of this UserCart.


        :param items: The items of this UserCart.
        :type items: List[OrderItems]
        """

        self._items = items

    @property
    def total_cost(self) -> float:
        """Gets the total_cost of this UserCart.

        Total cost of the items in the cart in euros.  # noqa: E501

        :return: The total_cost of this UserCart.
        :rtype: float
        """
        return self._total_cost

    @total_cost.setter
    def total_cost(self, total_cost: float):
        """Sets the total_cost of this UserCart.

        Total cost of the items in the cart in euros.  # noqa: E501

        :param total_cost: The total_cost of this UserCart.
        :type total_cost: float
        """

        self._total_cost = total_cost