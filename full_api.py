"""Full demo API for DS3500"""

from database_simulator import DatabaseSimulator
from flask import abort, Flask, jsonify, request
from typing import Final

# DatabaseSimulator: class
# abort: function
# Flask: class
# jsonify: function
# request: variable

app = Flask(__name__)  # create a Flask object
app.config['DEBUG'] = True  # start the debugger

# define constants
PAGE_SIZE: Final = 10  # API page size

data = DatabaseSimulator(20).generate_orders()  # get a list of 20 orders [{id: int, priority: str, date: ISO 8601 str, quantity: int}]

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

@app.errorhandler(404)
def not_found(error):
    """Custom 404 error handler
    Parameters:
        error (dict): the error
    Returns:
        flask.Response"""

    res =  jsonify({
        'error': True,
        'message': error.description
    })
    res.status_code = 404

    return res

@app.route('/ds3500/api/v1/orders', methods = ['GET'])
def get_all_orders():
    """Get all orders upto page limit
    (Note: full pagination not implemented)
    Returns:
        flask.Response: API response"""
    
    has_more = True if len(data) > PAGE_SIZE else False

    return jsonify({
        'size': len(data[: PAGE_SIZE]),
        'data': data[: PAGE_SIZE],
        'has_more': has_more,
        'error': False,
        'meta': {'message': 'full pagination not implemented'}
    })

@app.route('/ds3500/api/v1/order')
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
                    'data': ord,
                    'error': False
                })

        return abort(404, description = 'Order not found')

    else:
        return abort(400, description = 'Missing order ID')
    
if __name__ == '__main__':
    app.run()