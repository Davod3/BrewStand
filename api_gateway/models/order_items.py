# THIS CODE WAS AUTO GENERATED BY SWAGGER EDITOR

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from models.base_model_ import Model
from utils import util


class OrderItems(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, item_id: int=None, volume: float=None):  # noqa: E501
        """OrderItems - a model defined in Swagger

        :param item_id: The item_id of this OrderItems.  # noqa: E501
        :type item_id: int
        :param volume: The volume of this OrderItems.  # noqa: E501
        :type volume: float
        """
        self.swagger_types = {
            'item_id': int,
            'volume': float
        }

        self.attribute_map = {
            'item_id': 'itemID',
            'volume': 'volume'
        }
        self._item_id = item_id
        self._volume = volume

    @classmethod
    def from_dict(cls, dikt) -> 'OrderItems':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Order_items of this OrderItems.  # noqa: E501
        :rtype: OrderItems
        """
        return util.deserialize_model(dikt, cls)

    @property
    def item_id(self) -> int:
        """Gets the item_id of this OrderItems.

        A unique identifier assigned to each batch of beer produced.  # noqa: E501

        :return: The item_id of this OrderItems.
        :rtype: int
        """
        return self._item_id

    @item_id.setter
    def item_id(self, item_id: int):
        """Sets the item_id of this OrderItems.

        A unique identifier assigned to each batch of beer produced.  # noqa: E501

        :param item_id: The item_id of this OrderItems.
        :type item_id: int
        """

        self._item_id = item_id

    @property
    def volume(self) -> float:
        """Gets the volume of this OrderItems.

        The volume of the item being acquired, in liters.  # noqa: E501

        :return: The volume of this OrderItems.
        :rtype: float
        """
        return self._volume

    @volume.setter
    def volume(self, volume: float):
        """Sets the volume of this OrderItems.

        The volume of the item being acquired, in liters.  # noqa: E501

        :param volume: The volume of this OrderItems.
        :type volume: float
        """

        self._volume = volume