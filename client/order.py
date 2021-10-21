from datetime import datetime
from typing import Final

class Error(Exception):
    pass

class PriorityError(Error):
    pass

class Order():

    PRIORITY_MAP: Final = {'H': 3, 'M': 2, 'L': 1}

    def __init__(self, o_id, priority, o_date, quantity) -> None:
        """Constructor to initialise an order object
        Parameters:
            o_id (int): unique order ID
            priority (str): order priority 
            o_date (ISO 8601 date str): order date
            quantity (int): order quantity
        Returns:
            None"""
            
        self.o_id = o_id
        self.priority = priority
        self.o_date = o_date
        self.quantity = quantity

    def get_props(self) -> dict:
        """Get properties of an order
        Returns:
            dict: a dictionary with the properties"""

        return {'o_id': self.o_id, 'priority': self.priority, 'o_date': self.o_date, 'quantity': self.quantity}

    def __str__(self) -> str:
        """String representation of the order
        Returns:
            str: the string representation of the order"""

        return 'Order({0}, {1}, {2}, {3})'.format(self.o_id, self.priority, self.o_date, self.quantity)

    def set_date(self, iso_date) -> None:
        """Sets the order date
        Parameters:
            iso_date (datetime): order date as an ISO 8601 date type"""

        self.o_date = iso_date

    def validate(self) -> bool:
        """Checks if the order properties are valid
        Returns:
            bool: whether or not the order is valid"""

        try:
            if self.priority not in self.PRIORITY_MAP:
                raise PriorityError
        except PriorityError:
            print('PriorityError in order {}, did not add to PriorityQueue'.format(self.o_id))
            return False
            
        try:
            iso_date = datetime.fromisoformat(self.o_date)
            self.set_date(iso_date)
        except ValueError:
            print('ValueError (date) in order {}, did not add to PriorityQueue'.format(self.o_id))
            return False

        return True