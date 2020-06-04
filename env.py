import node
import ledger

class Env:


    def __init__(self, n):
        self.nodes = []
        self.lastProps = [[], [], [], []]
        self.lastVals = [ledger.Ledger()] * n
        for i in range(n):
            self.nodes.append(node.Node(self, i))
        self.round = 0
        self.stringarray = []

    def start(self, ledger_):
        for temp in self.nodes:
            temp.start(ledger_)

    def add_string(self, input):
        self.stringarray.append(input)

    def broadcast(self, message, i):
        #print("received: from " + str(i) + str(message))
        if isinstance(message, ledger.Ledger):
            #print("received: from " + str(i) + str(message))
            self.lastVals[i] = message
        else:
            #print("received: from " + str(i) +str(message))
            self.lastProps[i] = message

    def receive(self):
        for temp in self.nodes:
            temp.lastVals = self.lastVals.copy()
            temp.propositions = self.lastProps.copy()

def classify_string(input_strin):
    return True


if __name__ == "__main__":
    n = 50
    file_obj = open("data/data.txt", "w+")
    env = Env(4)
    genesis_ledger = ledger.Ledger()
    env.lastVals = [genesis_ledger, genesis_ledger, genesis_ledger, genesis_ledger]
    env.receive()
    for node_ in env.nodes:
        node_.start(genesis_ledger)
        node_.broadcast(genesis_ledger)
    env.receive()
    env.round = env.lastVals[0].sequence_num
    while env.lastVals[3].sequence_num < n or env.lastVals[1].sequence_num < n \
            or env.lastVals[2].sequence_num < n or env.lastVals[0].sequence_num < n:
        #print(str(env.lastVals[0].sequence_num) + " " + str(env.lastVals[1].sequence_num) + " " + str(env.lastVals[2].sequence_num) + " " + str(env.lastVals[3].sequence_num))
        
        for node_ in env.nodes:
            node_.update()
        env.receive()
    print(len(env.stringarray))
    for temp in env.stringarray:
        print(temp)


