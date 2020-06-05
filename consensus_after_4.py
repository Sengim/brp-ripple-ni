import node


class Consensus4(node.Node):

    def update(self):
        if self.currentLedger.sequence_num > 0 and self.currentLedger != self.prefferedLedger():
            self.roundstring = self.roundstring + "PB1 F"
            self.env.add_string(self.roundstring, self.id)
            self.start(self.prefferedLedger())
        else:
            if self.round == 0:
                self.generateTransactions()
                self.broadcast(self.transactions)
                self.round = self.round + 1
            elif self.round == 4:
                self.roundstring = self.roundstring + "T"
                self.currentLedger = self.currentLedger.create_new(transactions=self.propositions[0])
                self.env.add_string(self.roundstring, self.id)
                self.start(self.currentLedger)
            else:
                self.updatePosition()
                if self.checkConsensus():
                    self.roundstring = self.roundstring + "T"
                    self.env.add_string(self.roundstring, self.id)
                    #print(str(self.id) + "node found transactionset: " + str(self.transactions) + "on ledger: " + str(self.currentLedger.identifier))
                    self.currentLedger = self.currentLedger.create_new(transactions=self.transactions)
                    self.broadcast(self.currentLedger)
                    self.start(self.currentLedger)

