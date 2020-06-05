import node


class FastConsensus(node.Node):

    def checkConsensus(self):
        compare_set = [set(self.propositions[0])]
        scores = [0, 0, 0, 0]
        for temp in self.propositions:
            for i in range(len(compare_set)):
                if set(temp) == compare_set[i]:
                    scores[i] = scores[i] + 1
        return max(scores) >= 3
