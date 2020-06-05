import node
import ledger
import node_random
import random
import fast_consensus
import consensus_after_4


class Env:

    def __init__(self, n):
        self.nodes = []
        self.lastProps = [[], [], [], []]
        self.lastVals = [ledger.Ledger()] * n
        for i in range(n):
            if i == 3:

                self.nodes.append(node.Node(self, i))
            else:
                self.nodes.append(node_random.RandomNode(self, i))
        self.round = 0
        self.stringarray = []

    def start(self, ledger_):
        for temp in self.nodes:
            temp.start(ledger_)

    def add_string(self, input, ident=0):
        if ident == 3:
            self.stringarray.append(input)

    def broadcast(self, message, i):
        if isinstance(message, ledger.Ledger):
            self.lastVals[i] = message
        else:
            self.lastProps[i] = message

    def receive(self):
        for temp in self.nodes:
            temp.lastVals = self.lastVals
            temp.propositions = self.lastProps.copy()


if __name__ == "__main__":
    random.seed(9889999)

    env = Env(4)
    for i in range(4):
        if i == 3:
            env.nodes[i] = consensus_after_4.Consensus4(env, i)
        else:
            env.nodes[i] = node_random.RandomNode(env, i)
    genesis_ledger = ledger.Ledger()
    env.lastVals = [genesis_ledger, genesis_ledger, genesis_ledger, genesis_ledger]
    env.receive()
    for node_ in env.nodes:
        node_.start(genesis_ledger)
        node_.broadcast(genesis_ledger)

    env.receive()
    env.round = env.lastVals[0].sequence_num
    for i in range(4000):
    #while env.lastVals[3].sequence_num < n or env.lastVals[1].sequence_num < n \
     #       or env.lastVals[2].sequence_num < n or env.lastVals[0].sequence_num < n:
        #print(str(env.lastVals[0].sequence_num) + " " + str(env.lastVals[1].sequence_num) + " " + str(env.lastVals[2].sequence_num) + " " + str(env.lastVals[3].sequence_num))
        
        for node_ in env.nodes:
            node_.update()
        env.receive()

    for i in range(4):
        if i == 3:
            env.nodes[i] = consensus_after_4.Consensus4(env, i)
        else:
            env.nodes[i] = node.Node(env, i)

    genesis_ledger = ledger.Ledger()
    env.lastVals = [genesis_ledger, genesis_ledger, genesis_ledger, genesis_ledger]
    env.receive()
    for node_ in env.nodes:
        node_.start(genesis_ledger)
        node_.broadcast(genesis_ledger)

    env.receive()
    env.round = env.lastVals[0].sequence_num
    for i in range(70):
        # while env.lastVals[3].sequence_num < n or env.lastVals[1].sequence_num < n \
        #       or env.lastVals[2].sequence_num < n or env.lastVals[0].sequence_num < n:
        # print(str(env.lastVals[0].sequence_num) + " " + str(env.lastVals[1].sequence_num) + " " + str(env.lastVals[2].sequence_num) + " " + str(env.lastVals[3].sequence_num))

        for node_ in env.nodes:
            node_.update()
        env.receive()

    temp = genesis_ledger.create_new([1,2,3])
    temp4 = genesis_ledger.create_new([1,2,3])
    temp2 = temp.create_new([1,5,3])
    temp3 = genesis_ledger.create_new([1,4])
    env.lastVals = [temp2, temp2, temp2, temp2]
    env.receive()
    for node_ in env.nodes:
        node_.start(temp3)
    for j in range(800):


        for i in range(random.randint(2,3)):
            env.nodes[i] = node_random.RandomNode(env, i)

        env.lastVals = [temp2, temp2, temp2, temp3]
        env.receive()
        for node_ in env.nodes:
            node_.start(temp3)

        for i in range(3):
            for node_ in env.nodes:
                node_.update()

            env.receive()
        env.lastVals = [temp2, temp2, temp2, temp2]
        env.receive()
        for node_ in env.nodes:
            node_.update()

    #print(len(env.stringarray))

    file_obj = open("data/data.txt", "w+")
    file_obj.write(str(len(env.stringarray)) + " 7 \r\n")

    for temp in env.stringarray:
        array = temp.split(" ")
        if array[-1] == "F":
            tempstring = "0 " + str(len(array)-1) + " "
        else:
            tempstring = "1 " + str(len(array)-1) + " "
        for element in array:
            if not( element == "F" or element == "T"):
                tempstring  = tempstring + element + " "
        tempstring = tempstring + "\r\n"
        file_obj.write(tempstring)


