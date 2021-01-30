class Node:
    def toString(self):
        raise Exception('Unimplemented method')

    def interpret(self):
        raise Exception('Unimplemented method')

    def grow(self, plist, new_plist):
        pass


class Not(Node):
    def __init__(self, left):
        self.left = left

    def toString(self):
        return 'not (' + self.left + ')'

    def interpret(self, env):
        return not (self.left)

    def grow(plist, new_plist):
        pass


class And(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def toString(self):
        return "(" + self.left.toString() + " and " + self.right.toString() + ")"

    def interpret(self, env):
        return self.left.interpret(env) and self.right.interpret(env)

    def grow(plist, new_plist):
        pass


class Lt(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def toString(self):
        return "(" + self.left.toString() + " < " + self.right.toString() + ")"

    def interpret(self, env):
        return self.left.interpret(env) < self.right.interpret(env)

    def grow(plist, new_plist):
        pass


class Ite(Node):
    def __init__(self, condition, true_case, false_case):
        self.condition = condition
        self.true_case = true_case
        self.false_case = false_case

    def toString(self):
        return "(if" + self.condition.toString() + " then " + self.true_case.toString() + " else " + self.false_case.toString() + ")"

    def interpret(self, env):
        if self.condition.interpret(env):
            return self.true_case.interpret(env)
        else:
            return self.false_case.interpret(env)

    def grow(plist, new_plist):
        pass


class Num(Node):
    def __init__(self, value):
        self.value = value

    def toString(self):
        return str(self.value)

    def interpret(self, env):
        return self.value


class Var(Node):
    def __init__(self, name):
        self.name = name

    def toString(self):
        return self.name

    def interpret(self, env):
        return env[self.name]


class Plus(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def toString(self):
        return "(" + self.left.toString() + " + " + self.right.toString() + ")"

    def interpret(self, env):
        return self.left.interpret(env) + self.right.interpret(env)

    def grow(plist, new_plist):
        pass


class Times(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def toString(self):
        return "(" + self.left.toString() + " * " + self.right.toString() + ")"

    def interpret(self, env):
        return self.left.interpret(env) * self.right.interpret(env)

    def grow(plist, new_plist):
        pass


class BottomUpSearch():

    def grow(self, plist, integer_operations):
        pass

    def synthesize(self, bound, integer_operations, integer_values, variables, input_output):
        pass


synthesizer = BottomUpSearch()
synthesizer.synthesize(3, [Lt, Ite], [1, 2], ['x', 'y'],
                       [{'x': 5, 'y': 10, 'out': 5}, {'x': 10, 'y': 5, 'out': 5}, {'x': 4, 'y': 3, 'out': 3}])
synthesizer.synthesize(3, [And, Plus, Times, Lt, Ite, Not], [10], ['x', 'y'],
                       [{'x': 5, 'y': 10, 'out': 5}, {'x': 10, 'y': 5, 'out': 5}, {'x': 4, 'y': 3, 'out': 4},
                        {'x': 3, 'y': 4, 'out': 4}])
synthesizer.synthesize(3, [And, Plus, Times, Lt, Ite, Not], [-1, 5], ['x', 'y'], [{'x': 10, 'y': 7, 'out': 17},
                                                                                  {'x': 4, 'y': 7, 'out': -7},
                                                                                  {'x': 10, 'y': 3, 'out': 13},
                                                                                  {'x': 1, 'y': -7, 'out': -6},
                                                                                  {'x': 1, 'y': 8, 'out': -8}])
