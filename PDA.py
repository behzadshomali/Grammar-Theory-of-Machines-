import re, pprint

LAMBDA = '\u03BB'

def clean_whitespaces(string): # Preprocess the strings to simplify tokenizing
    spaces = re.compile(r'\s+')
    return re.sub(spaces, '', string)

def grammar_tokenizer():
    tokens = {}
    print('Enter the grammar in the form of Greibach normal form:')
    line = clean_whitespaces(input())
    while line != 'END':
        origin = line[0]
        start = line.find('->')
        destinations = line[start+2: ].split('|')
        tokens[origin] = destinations
        line = clean_whitespaces(input())
    return tokens

def extract_transitions(tokens):
    transitions = {}
    transitions['q0,%s,z' %(LAMBDA)] = ['q1,%sz' %(list(tokens.keys())[0])] # We manually add state 'q0'
    for token in tokens.items():
        for destination in token[1]:
            destination = clean_whitespaces(destination)
            stack_value = destination[1:] if len(destination) > 1 else LAMBDA
            element = 'q1,%s,%s' %(destination[0:1], token[0])
            transitions.setdefault(element, []).append('q1, %s' %(stack_value))
    transitions['q1,%s,z' %(LAMBDA)] = ['qf,z'] # We manually add state 'qf'
    return transitions

def states_initializer(transitions):
    q0 = State(name='q0', isStart=True, isFinal=False)
    q1 = State(name='q1', isStart=False, isFinal=False)
    q2 = State(name='qf', isStart=False, isFinal=True)

    for transition in transitions.items():
        if 'q0' in transition[0]:
            q0.output_transitions.append({transition[0]: transition[1]})
        if 'q0' in transition[1]:
            q0.input_transitions.append({transition[0]: transition[1]})
        if 'q1' in transition[0]:
            q1.output_transitions.append({transition[0]: transition[1]})
        if 'q1' in transition[1]:
            q1.input_transitions.append({transition[0]: transition[1]})
        if 'q2' in transition[0]:
            q2.output_transitions.append({transition[0]: transition[1]})
        if 'q2' in transition[1]:
            q2.input_transitions.append({transition[0]: transition[1]})

    return q0, q1, q2

class State:

    def __init__(self, name, isStart=False, isFinal=False):
        self.name = name
        self.isFinal = isFinal
        self.input_transitions = []
        self.output_transitions = []


class PDA: #Pushdown automaton
    def __init__(self, states, transitions):
        self.states = states
        self.tokens = tokens
        self.stack = ['z']
        self.state = states[0]

    def check_string(self, string, stack, current_state):
        string_orig = string
        state_orig = current_state
        stack_copy = [x for x in stack]

        for transition in transitions.items():
            for t in transition[1]:
                t = clean_whitespaces(t)
                if current_state.name == transition[0].split(',')[0]:
                    if len(string) == 0 and len(stack) != 1:
                        break
                    if len(string) == 0 and len(stack) == 1:
                        print("ACCEPTED :)")
                        exit(0)

                    if string[0] == transition[0].split(',')[1] or transition[0].split(',')[1] == LAMBDA:
                        if stack[-1] == transition[0].split(',')[2]:
                            for state in self.states:
                                if state.name == t.split(',')[0]:
                                    current_state = state
                                    break
                            if transition[0].split(',')[1] != LAMBDA:
                                string = string[1:]
                            stack.pop()
                            if t.split(',')[1] != LAMBDA:
                                stack += list(t.split(',')[1][::-1])
                            if current_state.isFinal and len(string) == 0:
                                print(transition)
                                print('ACCEPTED :)')
                                exit(0)

                            self.check_string(string, stack, current_state)
                string = string_orig
                stack = [x for x in stack_copy]
                state = state_orig


#===================================================

tokens = grammar_tokenizer()
transitions = extract_transitions(tokens)
states = list(states_initializer(transitions))
pda = PDA(states, transitions)

pprint.pprint(transitions)

input_string = input('Enter the string: ')
while input_string == '': # To check whether the string is empty
    input_string = input('Enter the string: ')

pda.check_string(input_string, pda.stack, pda.state)
print("NOT ACCEPTED :(")