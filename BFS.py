import time
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

    def grow(p,integer_values,variables,new_plist):
        pass


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

    def grow(p,new_plist,l1):
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

    def grow(p,new_plist,l1):
        pass


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


def findChildren(p,var_num,integer_operations):
    new_plist = []
    temp = []
    if (p.toString() == 'S'):
        new_plist.extend(var_num)
        if(Plus in integer_operations):
            new_plist.append(Plus(Var('S'), Var('S')))
        if(Times in integer_operations):
            new_plist.append(Times(Var('S'), Var('S')))
        if(Ite in integer_operations):
            new_plist.append(Ite(Var('B'), p, p))



    elif (isinstance(p, Lt)):
        if(Lt in integer_operations):
            if ('S' in p.left.toString()):
                if (p.left.toString() == 'S'):
                    for i in var_num:
                        new_plist.append(Lt(i,p.right))
                else:
                    temp.extend(findChildren(p.left,var_num,integer_operations))
                    for i in temp:
                        if(not isinstance(i,Ite)):
                             new_plist.append(Lt(i,p.right))
            elif ('S' in p.right.toString()):
                    if (p.right.toString() == 'S'):
                        for i in var_num:
                            new_plist.append(Lt(p.left, i))
                    else:
                        temp.extend(findChildren(p.right,integer_operations))
                        for i in temp:
                            if (not isinstance(i, Ite)):
                                 new_plist.append(Lt(p.left,i))


    elif(isinstance(p,Ite)):
        if (Ite in integer_operations):
            if(p.condition.toString()=="B"):
                new_plist.append(Ite(Lt(Var('S'),Var('S')),Var('S'),Var('S')))
            else:
                temp.extend(findChildren(p.condition,var_num,integer_operations))
                if(len(temp)!=0):
                    for i in temp:
                        if (isinstance(i,Lt)):
                             new_plist.append(Ite(i, p.true_case, p.false_case))
                else:
                    temp.extend(findChildren(p.true_case,var_num,integer_operations))
                    if (len(temp) != 0):
                        for i in temp:
                              new_plist.append(Ite(p.condition, i, p.false_case))
                    else:
                        temp.extend(findChildren(p.false_case,var_num,integer_operations))
                        if (len(temp) != 0):
                            for i in temp:
                                new_plist.append(Ite(p.condition, p.true_case, i))


    elif(isinstance(p,Plus)):
        if(Plus in integer_operations):
            if ('S' in p.left.toString()):
                if (p.left.toString() == 'S'):
                    for i in var_num:
                        new_plist.append(Plus(i,p.right))
                else:
                    temp.extend(findChildren(p.left,var_num,integer_operations))
                    for i in temp:
                        if(not isinstance(i,Ite)):
                             new_plist.append(Plus(i,p.right))
            elif ('S' in p.right.toString()):
                    if (p.right.toString() == 'S'):
                        for i in var_num:
                            new_plist.append(Plus(p.left, i))
                    else:
                        temp.extend(findChildren(p.right,integer_operations))
                        for i in temp:
                            if (not isinstance(i, Ite)):
                                 new_plist.append(Plus(p.left,i))



    elif (isinstance(p, Times)):
        if (Times in integer_operations):
            if ('S' in p.left.toString()):
                if (p.left.toString() == 'S'):
                    for i in var_num:
                        new_plist.append(Times(i, p.right))
                else:
                    temp.extend(findChildren(p.left, var_num, integer_operations))
                    for i in temp:
                        if (not isinstance(i, Ite)):
                            new_plist.append(Times(i, p.right))
            elif ('S' in p.right.toString()):
                if (p.right.toString() == 'S'):
                    for i in var_num:
                        new_plist.append(Times(p.left, i))
                else:
                    temp.extend(findChildren(p.right, integer_operations))
                    for i in temp:
                        if (not isinstance(i, Ite)):
                            new_plist.append(Times(p.left, i))

    return new_plist


class BreadthFirstSearch():


    def synthesize(self, bound, integer_operations, integer_values, variables, input_output):
        output = set()
        prog_generated=0
        prog_evaluated=0
        _open = [Var('S')]
        var_num=[]
        for i in variables:
            var_num.append(Var(i))
        for i in integer_values:
            var_num.append(Num(i))
            sample = open('a.txt', 'w')
        while (len(_open) != 0):
            p = _open.pop(0)
            children = findChildren(p,var_num,integer_operations)
            prog_generated+=len(children)
            for i in children:
                flag=0
                for j in _open:
                    if(i.toString()==j.toString()):
                        flag=1
                        break
                if(flag==0):
                    _open.append(i)
                    print(i.toString(), file = sample)
                    if(self.iscomplete(i)):
                        prog_evaluated+=1
                        if(self.iscorrect(i, input_output)):
                            print("Suitable Program:" ,i.toString())
                            print("Program Generated: ", prog_generated)
                            print("program evaluated: ", prog_evaluated)
                            sample.close()
                            return


    def iscomplete(self,prog):
        if('B' not in prog.toString() and 'S' not in prog.toString()):
            return True
        else:
            return False


    def iscorrect(self, prog, input_output):
        flag=0
        for i in input_output:
            if (i['out'] == prog.interpret(i)):
                flag=flag+1
        if(flag==len(input_output)):
            return True
        else:
            return False

synthesizer = BreadthFirstSearch()
start = time.time()
synthesizer.synthesize(3, [ Lt, Ite], [1, 2], ['x', 'y'],[{'x': 5, 'y': 10, 'out': 5}, {'x': 10, 'y': 5, 'out': 5}, {'x': 4, 'y': 3, 'out': 3}])
end = time.time()
print(f"Runtime of the program is {end - start}")
print("#############################################\n")


start = time.time()
synthesizer.synthesize(3, [And, Plus, Times, Lt, Ite, Not], [10], ['x', 'y'],[{'x': 5, 'y': 10, 'out': 5}, {'x': 10, 'y': 5, 'out': 5}, {'x': 4, 'y': 3, 'out': 4},{'x': 3, 'y': 4, 'out': 4}])
end = time.time()
print(f"Runtime of the program is {end - start}")
print("#############################################\n")


start = time.time()
synthesizer.synthesize(3, [And, Plus, Times, Lt, Ite, Not], [-1, 5], ['x', 'y'], [{'x': 10, 'y': 7, 'out': 17},{'x': 4, 'y': 7, 'out': -7},{'x': 10, 'y': 3, 'out': 13},{'x': 1, 'y': -7, 'out': -6},{'x': 1, 'y': 8, 'out': -8}])
end = time.time()
print(f"Runtime of the program is {end - start}")
print("#############################################\n")
#