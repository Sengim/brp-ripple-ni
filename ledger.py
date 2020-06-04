
class Ledger:

    @staticmethod
    def earliest_common(ledger_list):
        if Ledger.compare_list(ledger_list):
            return ledger_list[0]
        max_ident = ledger_list[0].identifier

        for ledger in ledger_list:
            if ledger.identifier > max_ident:
                max_ident = ledger.identifier
        new_ledger_list = ledger_list
        for i in range(len(ledger_list)):
            if ledger_list[i].identifier == max_ident:
                new_ledger_list[i] = ledger_list[i].prevLedger
        return Ledger.earliest_common(ledger_list)

    @staticmethod
    def compare_list(ledger_list):
        ident = ledger_list[0].identifier
        for ledger in ledger_list:
            if ledger.identifier != ident:
                return False
        return True

    @staticmethod
    def ancestor_contains(ledger_, lowerledger):
        while ledger_.sequence_num < lowerledger.sequence_num:
            lowerledger = lowerledger.prevLedger
        return lowerledger.identifier == ledger_.identifier

    def create_new(self, transactions):
        for ledg in self.children:
            if self.identifier + sum(transactions) == ledg.identifier:
                return ledg
        return Ledger(prevLedger=self, transactions=transactions)

    def __init__(self, prevLedger=None, transactions=[]):
        if prevLedger is None:
            self.identifier = 0
            self.prevLedger = None
            self.children = []
            self.sequence_num = 0
        else:
            self.identifier = prevLedger.identifier + sum(transactions)
            self.prevLedger = prevLedger
            self.children = []
            self.sequence_num = prevLedger.sequence_num + 1
            if not prevLedger.children_exists(self):
                prevLedger.children.append(self)

    def children_exists(self, ledger):
        for temp in self.children:
            if temp.identifier == ledger.identifier:
                return True
        return False



