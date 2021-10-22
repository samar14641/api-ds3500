# api-ds3500
APIs demo for DS3500 (Fall'21)

Required modules:

* [Flask](https://pypi.org/project/Flask/)
* [NumPy](https://pypi.org/project/numpy/)
* [Requests](https://pypi.org/project/requests/)
* [python-dotenv](https://pypi.org/project/python-dotenv/)

Directories:

1. server: Contains files to simulate an API service. This API service i.e. the DS3500 Orders API has GET and POST methods for order data (note - the data is generated from a database simulator, and is not actually *stored* in a database).

2. client: Contains files to simulate a client application. This client application is a priority queue, and it receives data from the DS3500 Orders API. 

Running the applications:

1. Install modules listed above

2. Run the apps: 

```
python full_api.py
```
for the API (runs on port 5000), and
```
python order_manager.py
```
for the client.