# THIS CODE WAS AUTO GENERATED BY SWAGGER EDITOR

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from models.base_model_ import Model
from utils import util


class UserIdCartBody(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, batch_id: int=None, volume: float=None):  # noqa: E501
        """UserIdCartBody - a model defined in Swagger

        :param batch_id: The batch_id of this UserIdCartBody.  # noqa: E501
        :type batch_id: int
        :param volume: The volume of this UserIdCartBody.  # noqa: E501
        :type volume: float
        """
        self.swagger_types = {
            'batch_id': int,
            'volume': float
        }

        self.attribute_map = {
            'batch_id': 'batchID',
            'volume': 'volume'
        }
        self._batch_id = batch_id
        self._volume = volume

    @classmethod
    def from_dict(cls, dikt) -> 'UserIdCartBody':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The userId_cart_body of this UserIdCartBody.  # noqa: E501
        :rtype: UserIdCartBody
        """
        return util.deserialize_model(dikt, cls)

    @property
    def batch_id(self) -> int:
        """Gets the batch_id of this UserIdCartBody.


        :return: The batch_id of this UserIdCartBody.
        :rtype: int
        """
        return self._batch_id

    @batch_id.setter
    def batch_id(self, batch_id: int):
        """Sets the batch_id of this UserIdCartBody.


        :param batch_id: The batch_id of this UserIdCartBody.
        :type batch_id: int
        """

        self._batch_id = batch_id

    @property
    def volume(self) -> float:
        """Gets the volume of this UserIdCartBody.


        :return: The volume of this UserIdCartBody.
        :rtype: float
        """
        return self._volume

    @volume.setter
    def volume(self, volume: float):
        """Sets the volume of this UserIdCartBody.


        :param volume: The volume of this UserIdCartBody.
        :type volume: float
        """

        self._volume = volume
