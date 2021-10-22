"""Starter code for the DS3500 Orders API"""

from api_errors import PriorityValueError
from database_simulator import DatabaseSimulator

from typing import Final


# PriorityValueError: custom exception class
# DatabaseSimulator: class
# abort: function
# Flask: class
# jsonify: function
# request: variable


# define constants
PAGE_SIZE: Final = 50  # API page size

data = DatabaseSimulator(20).generate_orders()  # get a list of 20 orders [{id: int, priority: str, date: ISO 8601 str, quantity: int}]

def no_content():
    """Custom 204 status handler
    Returns:
        flask.Response"""
    
    # 204 sends a blank response with status code 204
    pass

# errors to handle: 400 Bad Request, 401 Unauthorized, 404 Not Found 

def bad_request(error):
    """Custom 400 error handler
    Parameters:
        error (dict): the error
    Returns:
        flask.Response"""

    pass

def home() -> str:
    """The API's homepage
    Returns:
        str: HTML of the homepage as a string"""
        
    return '<p>DS3500 Orders API</p>'

def get_orders():
    """Get all orders upto page limit
    Returns:
        flask.Response: API response"""
    
    pass

def get_order():
    """Get an order using it's ID
    Returns:
        flask.Response: API response"""

    pass

def get_orders_by_priority():
    """Get all orders of a certain priority value
    Returns:
        flask.Response: API response"""

    pass

def verify_key(api_key) -> bool:
    """Verify the API key for v2 APIs
    Parameters:
        api_key (str): the API key
    Returns:
        bool: whether the key is valid or not"""

    pass

def get_orders_auth():
    """Get all orders upto page limit after auth
    Returns:
        flask.Response: API response"""

    pass

def add_order():
    """Add an order after auth
    Returns:
        flask.Response: API response"""

    pass

    
if __name__ == '__main__':
    pass