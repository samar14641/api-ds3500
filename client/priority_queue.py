"""Generic priortiy queue class"""

class PriorityQueue():
    def __init__(self) -> None:
        """Constructor to initialise a blank list that serves as the base of the priority queue
        Returns:
            None"""

        self.pq = []

    def is_empty(self) -> bool:
        """Checks if the list is empty
        Returns:
            bool: whether the list is empty or not"""

        return len(self.pq) == 0

    def size(self) -> int:
        """Get the size of the list
        Returns:
            int: the size of the list"""

        return len(self.pq)

    def enqueue(self, item, compare) -> None:
        """Adds an object to the list using the comparator for position
        Parameters:
            item (object): the object to enqueue
            comapre (function): the comparator function to use for enqueuing
        Returns:
            None"""

        inserted = False

        if self.is_empty():
            self.pq.append(item)
        else:
            for i in range(self.size()):
                if compare(item, self.pq[i]) == 1:
                    self.pq.insert(i, item)
                    inserted = True
                    break

            if not inserted:
                self.pq.append(item)

    def dequeue(self) -> tuple:
        """Removes the first object from the queue
        Returns:
            tuple: a tuple with a status code (1 for success, 0 for error) and 
            an object (success) or error message (0)"""

        if not self.is_empty():
            item = self.pq.pop(0)
            return 1, item
        else:
            return 0, 'Underflow - PriorityQueue is empty'

    def get_id_list(self) -> list:
        """Get the list of object IDs in the queue
        Returns:
            list: a list of object IDs"""

        if not self.is_empty():
            id_list = []

            for o in self.pq:
                id_list.append(o.props()['o_id'])

            return id_list
        else:
            return []

    def peek(self) -> tuple:
        """Get the first object from the list without dequeuing it
        Returns:
            tuple: a tuple with a status code (1 for success, 0 for error) and 
            an object (success) or error message (0)"""

        try:
            return 1, self.pq[0].props()
        except IndexError:
            return 0, 'Underflow - PriorityQueue is empty'

    def clear(self) -> None:
        """Clears the queue
        Returns:
            None"""

        self.pq = []

    def __str__(self) -> str:
        """String representation of the queue
        Returns:
            str: the string representation of the queue"""

        if not self.is_empty():
            s = 'PriorityQueue['

            for item in self.pq:
                s += item.__str__() + ', '

            s = s[: -2] + ']'

            return s
        else:
            return 'PriorityQueue[]'