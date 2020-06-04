import random
import math
import ledger
import numpy as np

class Node:

    def __init__(self, env, id):
        self.queue = []
        self.transactions = []
        self.lastVals = []
        self.propositions = []
        self.currentLedger = ledger.Ledger(None, [])
        self.round = 0
        self.id = id
        self.env = env
        self.roundstring = ""

    def __init__(self, env, id, ledg):
        self.queue = []
        self.transactions = []
        self.lastVals = []
        self.propositions = []
        self.currentLedger = ledg
        self.round = 0
        self.id = id
        self.env = env
        self.roundstring = ""

    def start(self, L):
        self.currentLedger = L
        self.generateTransactions()
        #self.broadcast(self.transactions)
        self.round = 0
        self.roundstring = ""
        if self.prefferedLedger() != self.currentLedger:
            self.roundstring = "PB1 "
        else:
            self.roundstring = "PB0 "

    def generateTransactions(self):
        new_transaction_list = []
        for i in range(20):

            # Add any seperate transaction to the list with probability 0.25
            if random.randint(1, 3) == 2:
                new_transaction_list.append(i)
        self.transactions = new_transaction_list.copy()

    def updateString(self):
        comp_set = [set(self.propositions[0])]
        count = 0
        for prop in self.propositions:
            temp = False
            temp2 = count+1
            for comp in comp_set:
                if set(prop) == comp:
                    temp2 = count
                    temp = True
            if not temp:
                count = count + 1
                comp_set.append(set(prop))

            self.roundstring = self.roundstring + "P" + str(temp2) + " "
        self.roundstring = self.roundstring + "RR "


    def update(self):
        if self.currentLedger.sequence_num > 0 and self.currentLedger != self.prefferedLedger():
            self.roundstring = self.roundstring + "PB1 F"
            self.env.add_string(self.roundstring)
            self.start(self.prefferedLedger)
        else:
            if self.round == 0:
                self.generateTransactions()
                self.broadcast(self.transactions)
                self.round = self.round + 1
            elif self.round == 4:
                self.roundstring = self.roundstring + "F"
                self.start(self.currentLedger)
            else:
                self.updatePosition()
                if self.checkConsensus():
                    self.roundstring = self.roundstring + "T"
                    self.env.add_string(self.roundstring)
                    #print(str(self.id) + "node found transactionset: " + str(self.transactions) + "on ledger: " + str(self.currentLedger.identifier))
                    self.currentLedger = self.currentLedger.create_new(transactions=self.transactions)
                    self.broadcast(self.currentLedger)
                    self.start(self.currentLedger)

    def updatePosition(self):
        positions = []
        scores = [0] * 20
        self.updateString()
        for listr in self.propositions:
            for k in listr:
                scores[k] = scores[k] + 1
        for i in range(20):
            if int(math.ceil(self.threshold() * 4)) <= scores[i]:
                positions.append(i)
        self.transactions = positions
        self.broadcast(positions)

    def threshold(self):
        if self.round == 0:
            return .5
        elif self.round == 1:
            return 0.75
        elif self.round == 2:
            return .9
        elif self.round == 3:
            return .95

    def checkConsensus(self):
        compare_set = set(self.propositions[0])
        n = 0
        for temp in self.propositions:
            if set(temp) == compare_set:
                n = n + 1
        return n >= 4

    def prefferedLedger(self):
        adam = ledger.Ledger.earliest_common(self.lastVals)
        done = False
        while len(adam.children) > 0 and not done:
            temp = []
            for adam_child in adam.children:
                temp.append(self.branch_support(adam_child))
            index_arr = np.argsort(temp)

            delta = self.branch_support(adam.children[index_arr[0]])
            if len(adam.children) > 1:
                delta = delta - self.branch_support(adam.children[index_arr[1]]) + self.phi(
                    self.branch_support(adam.children[index_arr[0]]), self.branch_support(adam.children[index_arr[1]]))
            if delta > self.uncommitted(adam.sequence_num + 1):
                adam = self.branch_support(adam.children[index_arr[0]])
            else:
                done = True
        if ledger.Ledger.ancestor_contains(adam, self.currentLedger):
            return self.currentLedger
        return adam

    def branch_support(self, ledger_):
        supp = 0
        for newledger in self.lastVals:
            if ledger.Ledger.ancestor_contains(ledger_, newledger):
                supp = supp + 1

        return supp

    def uncommitted(self, s):
        supp = 0
        for newledger in self.lastVals:
            if newledger.sequence_num < max(s, self.currentLedger.sequence_num):
                supp = supp + 1

        return supp

    def phi(self, l1, l2):
        if l1.sequence_num > l2.sequence_num:
            return 1
        return 0

    def broadcast(self, message):
        self.env.broadcast(message, self.id)

