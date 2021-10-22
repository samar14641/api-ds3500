"""Custom exceptions for the DS3500 Orders API"""

class APIError(Exception):
    pass

class PriorityValueError(APIError):
    """Exception to handle an incorrect priority value"""
    
    pass