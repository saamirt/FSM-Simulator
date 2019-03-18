import itertools
from functools import reduce

class State:
    def __init__(self, name, alphabet):
        self.__name = name
        self.__next = {i: [] for i in alphabet}

    def get_name(self):
        return self.__name

    def set_name(self, s):
        self.__name = s

    def add_next(self, c, state):
        self.__next[c].append(state)

    def get_next(self, c):
        tmp = self.__next.get(c, [])
        if (len(tmp) < 1):
            return None
        return tmp

    def __str__(self):
        return self.get_name()


def find_state(states, name):
    for i in range(len(states)):
        if states[i].get_name() == name:
            return i
    return -1

def get_int(msg):
    while 1:
        try:
            result = int(input(msg))
            break
        except Exception:
            print("Enter a positive integer")
    return result

def init():
    alph = []
    for i in range(get_int("How many characters in the alphabet? ")):
        alph.append(input("What is character #" + str(i) + "? "))
    states = []
    final = []
    for i in range(get_int("How many states? ")):
        states.append(State(input("State " + str(i) + " name: "), alph))
    for i in range(int(input("How many final states? "))):
        while 1:
            tmp = input("final state " + str(i) + " name: ")
            if (find_state(states, tmp) > -1):
                final.append(tmp)
                break
            print("State does not exist")
    while 1:
        start = input("What is the start state? ")
        if (find_state(states, start) > -1):
            break
        else:
            print("State does not exist")

    for i in states:
        for j in alph:
            for _ in range(get_int("How many states does '" + str(i.get_name()) + "' lead into through " + str(j) + "? ")):
                i.add_next(
                    j,
                    states[find_state(states, input(str(i.get_name()) + ":" + str(j) + ">"))]
                )
    return {
        'alphabet':alph,
        'states': states,
        'start': states[find_state(states,start)],
        'final': final
    }


def traverse(current_states, s):
    if len(s) <= 0:
        return current_states
    new_states = []
    for i in current_states:
        tmp = i.get_next(s[0])
        if not (tmp is None or tmp in new_states):
            new_states.extend(tmp)
    return traverse(new_states, s[1:])

def gen_all_strings(alphabet,max_len):
    s = []
    for i in range(max_len+1):
        s.extend([''.join(x) for x in itertools.product(alphabet, repeat=i)])
    return s

def traverse_batch(start,s,final):
    for i in s:
        tmp = [str(j) for j in traverse([start], i)]
        if tmp and reduce(lambda x, y: x or y in final, tmp, False):
            print(str(i))
            '''
            print("String : " + str(i))
            print("Possible States: " + ", ".join(tmp) + "\n")
            '''
