import json
import requests

from order import Order
from priority_queue import PriorityQueue
# from pprint import pprint


def compare_orders(ord_1: Order, ord_2: Order):  # return 1 if ord_1 has higher priority, else return 2
    ord_1_props, ord_2_props = ord_1.get_props(), ord_2.get_props()

    # check priority: H > M > L
    if Order.PRIORITY_MAP[ord_1_props['priority']] > Order.PRIORITY_MAP[ord_2_props['priority']]:
        return 1
    elif Order.PRIORITY_MAP[ord_1_props['priority']] < Order.PRIORITY_MAP[ord_2_props['priority']]:
        return 2
    else:  # check date: old > new
        if ord_1_props['o_date'] < ord_2_props['o_date']:
            return 1
        elif ord_1_props['o_date'] > ord_2_props['o_date']:
            return 2
        else:  # check quantity: more > less
            if ord_1_props['quantity'] > ord_2_props['quantity']:
                return 1
            elif ord_1_props['quantity'] < ord_2_props['quantity']:
                return 2
            else:  # check id: smaller > bigger
                if ord_1_props['o_id'] < ord_2_props['o_id']:
                    return 1
                else:
                    return 2

def get_data(url, headers = {}, params = {}, payload = {}) -> tuple:

    try:
        res = requests.get(url, headers = headers, data = payload, params = params)

        print('Status: {}\nTime taken: {}s\nURL: {}'.format(res.status_code, res.elapsed, res.url))

        res.raise_for_status()

        # pprint(res.json())

        return True, res.json()

    except requests.exceptions.ConnectionError:
        print('Connection Error')
        return False, None

    except requests.exceptions.HTTPError:  # some 4xx or 5xx error:
        print(res.json()['message'])
        return False, None

    except json.decoder.JSONDecodeError:  # 204 status code:
        print('Blank response - 204')
        return False, None

def add_to_queue(data, pq: PriorityQueue) -> PriorityQueue:
    for ord in data:
        order_obj = Order(ord['id'], ord['priority'], ord['date'], ord['quantity'])

        if order_obj.validate():
            pq.enqueue(order_obj, compare_orders)

    return pq

def main():
    # reply = get_data('http://127.0.0.1:5000/ds3500/api/v1/orders')
    # reply = get_data('http://127.0.0.1:5000/ds3500/api/v1/order', params = {'id': 22})
    reply = get_data('http://127.0.0.1:5000/ds3500/api/v2/orders', headers = {'x-api-key': '11133'})

    if reply[0]:
        pq = PriorityQueue()

        pq = add_to_queue(reply[1]['data'], pq) 

        print(pq.__str__())  # string representation of the queue after all original orders are processed
        print(pq.size())        

if __name__ == '__main__':
    main()