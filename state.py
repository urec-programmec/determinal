class state:
    def __init__(self, rules, flag=None):
        if flag != None:
            self.liter = rules[2]
        else:
            self.liter = rules[0]
        self.symbol_to_next_state = []
        self.add_transition(rules, flag)

        # symbtns = [
        # ["symb1", "state1", "state2"]
        # ["", "state1", "state2", "state3"]
        # ["symb3", "state1"]
        # ]



    def add_transition(self, rules, flag=None):
        if not flag is None:
            return

        master = [i[0] for i in self.symbol_to_next_state]
        symbol = rules[1] if len(rules) == 2 else rules[2]

        if symbol in master:
            i = master.index(symbol)
            self.symbol_to_next_state[i].append(rules[1] if len(rules) == 2 else rules[2])
        else:
            self.symbol_to_next_state.append(["", rules[1]] if len(rules) == 2 else [rules[1], rules[2]])
