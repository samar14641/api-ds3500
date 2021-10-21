import numpy as np

from typing import Final


class DatabaseSimulator():

    PRIORITIES: Final = ('H', 'M', 'L')

    def __init__(self, n) -> None:
        """Constructor to initialise the database sim
        Parameters: 
            n (int): the number of samples to generate
        Returns:
            None"""

        self.n = n
        # self.priorities = ('H', 'M', 'L')
        self.dates = ('2021-10-19', '2021-10-20', '2021-10-21', '2021-10-22')

    def generate_orders(self) -> list:
        """Generates n orders with 4 attributes (ID, priority, date, quantity)
        Returns:
            list: a list of dictionaries of orders
        """

        generated_orders = []

        for i in range(1, self.n + 1):
            # generate order attributes
            ord_priority = self.PRIORITIES[np.random.randint(0, len(self.PRIORITIES))]
            ord_date = self.dates[np.random.randint(0, len(self.dates))]
            ord_quantity = np.random.randint(1, 101)

            # add to orders list as a dictionary
            generated_orders.append({
                'id': i,
                'priority': ord_priority,
                'date': ord_date,
                'quantity': ord_quantity
            })

        return generated_orders

    def get_sample_size(self) -> int:
        """Get the number of samples being generated
        Returns:
            int: the number of samples"""

        return self.n

    def set_sample_size(self, n) -> int:
        """Set the value for number of samples to generate
        Returns:
            int: the new value for the number of samples to generate"""

        self.n = n
        return self.n

def main():
    db_sim = DatabaseSimulator(5)

    print(db_sim.generate_orders())


if __name__ == '__main__':
    main()