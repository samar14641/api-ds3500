"""The DS3500 Orders API"""

from api_errors import PriorityValueError
from database_simulator import DatabaseSimulator
from flask import abort, Flask, jsonify, request
from typing import Final


# PriorityValueError: custom exception class
# DatabaseSimulator: class
# abort: function
# Flask: class
# jsonify: function
# request: variable

app = Flask(__name__)  # create a Flask object
app.config['DEBUG'] = True  # start the debugger

# define constants
PAGE_SIZE: Final = 50  # API page size

data = DatabaseSimulator(20).generate_orders()  # get a list of 20 orders [{id: int, priority: str, date: ISO 8601 str, quantity: int}]

def no_content():
    """Custom 204 status handler
    Returns:
        flask.Response"""

    res = jsonify({})
    res.status_code = 204

    # other option: create an emtpy response with status code 200, e.g.:
    # {'size': 0, 'message': str}

    return res  # 204 sends a blank response with status code 204

@app.errorhandler(400)
def bad_request(error):
    """Custom 400 error handler
    Parameters:
        error (dict): the error
    Returns:
        flask.Response"""

    res =  jsonify({
        'error': True,
        'message': error.description
    })
    res.status_code = 400

    return res

@app.errorhandler(401)
def unauthorized(error):
    """Custom 401 error handler
    Parameters:
        error (dict): the error
    Returns:
        flask.Response"""

    res =  jsonify({
        'error': True,
        'message': error.description
    })
    res.status_code = 401

    return res

@app.errorhandler(404)
def not_found(args):
    """Custom 404 error handler
    Returns:
        flask.Response"""

    res =  jsonify({
        'error': True,
        'message': 'Not Found'
    })
    res.status_code = 404

    return res

@app.route('/ds3500/api/v1/orders', methods = ['GET'])
def get_orders():
    """Get all orders upto page limit
    (Note: full pagination not implemented)
    Returns:
        flask.Response: API response"""
    
    has_more = True if len(data) > PAGE_SIZE else False  # pagination flag

    return jsonify({
        'size': len(data[: PAGE_SIZE]),
        'data': data[: PAGE_SIZE],
        'has_more': has_more,
        'error': False,
        'meta': {'message': 'full pagination not implemented'}
    })

@app.route('/ds3500/api/v1/order', methods = ['GET'])
def get_order():
    """Get an order using it's ID
    Returns:
        flask.Response: API response"""

    ord_id = None

    if 'id' in request.args:
        try:
            ord_id = int(request.args['id'])
        except ValueError:
            return abort(400, description = 'Invalid ID type')

        for ord in data:
            if ord['id'] == ord_id:
                return jsonify({
                    'size': 1,
                    'data': [ord],
                    'error': False
                })

        return no_content()

    else:
        return abort(400, description = 'Missing order ID')

@app.route('/ds3500/api/v1/orders/priority', methods = ['GET'])
def get_orders_by_priority():
    """Get all orders of a certain priority value
    Returns:
        flask.Response: API response"""

    ord_priority = None

    if 'priority' in request.args:
        try:
            ord_priority = request.args['priority']

            if ord_priority not in DatabaseSimulator.PRIORITIES:
                raise PriorityValueError

        except PriorityValueError:
            return abort(400, description = 'Invalid priority value')

        filtered_orders = []  # list of orders of the requested priority

        for ord in data:
            if ord['priority'] == ord_priority:
                filtered_orders.append(ord)

        has_more = True if len(filtered_orders) > PAGE_SIZE else False

        if len(filtered_orders) > 0:
            return jsonify({
                'size': len(filtered_orders[: PAGE_SIZE]),
                'data': filtered_orders[: PAGE_SIZE],
                'has_more': has_more,
                'error': False,
                'meta': {'message': 'full pagination not implemented'}
            })
        else:
            return no_content()

    else:
        return abort(400, 'Missing priority value')

def verify_key(api_key) -> bool:
    """Verify the API key for v2 APIs
    Parameters:
        api_key (str): the API key
    Returns:
        bool: whether the key is valid or not"""

    try:
        if len(api_key) == 5 and int(api_key) % 3 == 0:  # a valid key has 5 digits AND is divisible by 3 
            return True
        else:
            return False
    
    except ValueError:
        return False

@app.route('/ds3500/api/v2/orders', methods = ['GET'])
def get_orders_auth():
    """Get all orders upto page limit after auth
    (Note: full pagination not implemented)
    Returns:
        flask.Response: API response"""

    api_key = request.headers.get('x-api-key', None)
    
    if api_key is not None and verify_key(api_key):  # key is present and valid
        has_more = True if len(data) > PAGE_SIZE else False

        return jsonify({
            'size': len(data[: PAGE_SIZE]),
            'data': data[: PAGE_SIZE],
            'has_more': has_more,
            'error': False,
            'meta': {'message': 'full pagination not implemented'}
        })

    elif api_key is not None and not verify_key(api_key):  # key is present and invalid i.e. HTTP 401
        return abort(401, description = 'Invalid API key')
    else:  # key not present
        return abort(401, description = 'Missing API key')

    
if __name__ == '__main__':
    app.run()