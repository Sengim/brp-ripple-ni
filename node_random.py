import node
import random

class RandomNode(node.Node):

    def generateTransactions(self):
        new_transaction_list = []
        if random.randint(1, 2) == 2:
            new_transaction_list = [1, 5, 7]
            self.transactions = new_transaction_list.copy()
            return
        elif random.randint(1, 3) == 2:
            new_transaction_list = [5, 8, 19]
            self.transactions = new_transaction_list.copy()
            return

        for i in range(20):

            # Add any seperate transaction to the list with probability 0.25
            if random.randint(1, 3) == 2:
                new_transaction_list.append(i)
        self.transactions = new_transaction_list.copy()

    def updatePosition(self):
        self.generateTransactions()

        self.broadcast(self.transactions)
