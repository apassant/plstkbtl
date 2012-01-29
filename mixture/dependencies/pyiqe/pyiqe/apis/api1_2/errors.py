# -*- coding: UTF-8 -*-

from textwrap import dedent
class APIError(Exception):
    """Base Class for All API Errors"""
    pass

class APIDuplicateObjectCustomIDError(APIError):
    """You are trying to assign  a custom_id to an object. However there is already another object in the same collection that has this custom_id"""
    pass

        