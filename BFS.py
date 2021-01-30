class Node:
    def toString(self):
        raise Exception('Unimplemented method')

    def interpret(self):
        raise Exception('Unimplemented method')

    def grow(self, p,integer_values):
        pass


class Not(Node):
    def __init__(self, left):
        self.left = left

    def toString(self):
        return 'not (' + self.left.toString() + ')'

    def interpret(self, env):
        return not (self.left)

    def grow(p,integer_values):
        new_plist=[]





class And(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def toString(self):
        return "(" + self.left.toString() + " and " + self.right.toString() + ")"

    def interpret(self, env):
        return self.left.interpret(env) and self.right.interpret(env)

    def grow(p,integer_values):
        new_plist=[]
        if (isinstance(p.left, Var) and p.left.toString()=='B'):
            new_plist.append(And(Var('B'), Var('B'))
            new_plist.append(Not(Var('B')))
            new_plist.append(Ite(Not(Var('B')), p.true_case, p.false_case))



class Lt(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def toString(self):
        return "(" + self.left.toString() + " < " + self.right.toString() + ")"

    def interpret(self, env):
        return self.left.interpret(env) < self.right.interpret(env)

    def grow(p,integer_values):
        new_plist=[]
        if('S'in p.left.toString()):
            x=p.left.grow(integer_values)
            for i in x:
                new_plist.append(Lt(i,p.right))
        elif('S' in p.right.toString()):
            x=p.right.grow(integer_values)
            for i in x:
                new_plist.append(Lt(p.left,i))
        return new_plist



class Ite(Node):
    def __init__(self, condition, true_case, false_case):
        self.condition = condition
        self.true_case = true_case
        self.false_case = false_case

    def toString(self):
        return "(if " + self.condition.toString() + " then " + self.true_case.toString() + " else " + self.false_case.toString() + ")"

    def interpret(self, env):
        if self.condition.interpret(env):
            return self.true_case.interpret(env)
        else:
            return self.false_case.interpret(env)

    def grow(p,integer_values):
        new_plist=[]
        if(isinstance(p.condition,Var)):
            new_plist.append(Ite(Lt(Var('S'),Var('S')),p.true_case,p.false_case))
            new_plist.append(Ite(And(Var('B'),Var('B')),p.true_case,p.false_case))
            new_plist.append(Ite(Not(Var('B')),p.true_case,p.false_case))
        elif(isinstance(p.condition,Lt) or isinstance(p.condition, Not)):
            x=p.grow(integer_values)
            for i in x:
                new_plist.append(Ite(i,p.true_case,p.false_case))
        elif('S' in p.true_case.toString()):
            x=p.true_case.grow(integer_values)
            for i in x:
                new_plist.append(Ite(p.condition,i,p.false_case))

        elif('S' in p.false_case.toString()):
            x=p.true_case.grow(integer_values)
            for i in x:
                new_plist.append(Ite(p.condition,p.true_case,i))
        return new_plist






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
    def grow( p,integer_values):
        new_plist=[]
        if(p.toString()=='S'):
            new_plist.append(Var('x'))
            new_plist.append(Var('y'))
            for i in integer_values:
                new_plist.append(Num(i))
            new_plist.append(Plus(Var('S'), Var('S')))
            new_plist.append(Times(Var('S'), Var('S')))
            new_plist.append(Ite(Var('B'), Var('S'),Var('S')))
        elif(p.toString()=='B'):
            new_plist.append(Ite(Lt(Var('S'), Var('S')), p.true_case, p.false_case))
            new_plist.append(Ite(And(Var('B'), Var('B')), p.true_case, p.false_case))
            new_plist.append(Ite(Not(Var('B')), p.true_case, p.false_case))
        return new_plist


class Plus(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def toString(self):
        return "(" + self.left.toString() + " + " + self.right.toString() + ")"

    def interpret(self, env):
        return self.left.interpret(env) + self.right.interpret(env)

    def grow(p,integer_values):
        new_plist=[]
        if('S' in p.left.toString()):
            x=p.left.grow(integer_values)
            for i in x:
                new_plist.append(Plus(i,p.right))
        elif ('S' in p.right.toString()):
            x = p.right.grow(integer_values)
            for i in x:
                new_plist.append(Plus(p.left,i))
        return new_plist

class Times(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def toString(self):
        return "(" + self.left.toString() + " * " + self.right.toString() + ")"

    def interpret(self, env):
        return self.left.interpret(env) * self.right.interpret(env)

    def grow(p,integer_values):
        new_plist = []
        if ('S' in p.left.toString()):
            x = p.left.grow(integer_values)
            for i in x:
                new_plist.append(Times(i, p.right))
        elif ('S' in p.right.toString()):
            x = p.right.grow(integer_values)
            for i in x:
                new_plist.append(Times(p.left, i))
        return new_plist


class BreadthFirstSearch():

    def children(self, p, integer_operations,integer_values):
        new_plist=[]
        for op in integer_operations:
                op.grow(p, integer_values)
        return new_plist

    def synthesize(self, bound, integer_operations, integer_values, variables, input_output):
        open=[Var('S')]
        while(len(open)!=0):
            p=open.pop(0)
            if(not isinstance(p,Num) and p.toString()!='x' and p.toString()!='y'):
                 child=p.grow(integer_values)
                 for i in child:
                    print(i.toString())
                    open.append(i)



synthesizer = BreadthFirstSearch()
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
