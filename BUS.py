import time
import itertools
import math


class Node:
    def toString(self):
        raise Exception('Unimplemented method')

    def interpret(self):
        raise Exception('Unimplemented method')

    def grow(self, plist, new_plist):
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



class Not(Node):
    def __init__(self, left):
        self.left = left

    def toString(self):
        return 'not (' + self.left.toString() + ')'

    def interpret(self, env):
        return not (self.left.interpret(env))

    def grow(plist, new_plist, variables, int_str, size,dict):
        for i in plist:
            if (isinstance(i, Lt)):
                new_plist.append(Not(i))



class And(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def toString(self):
        return "(" + self.left.toString() + " and " + self.right.toString() + ")"

    def interpret(self, env):
        return self.left.interpret(env) and self.right.interpret(env)

    def grow(plist, new_plist, variables, int_str, size,dict):
        prog = find_and(plist)
        for i in prog:
            for j in prog:
                if (i != j and (nodeCount(i, int_str) + nodeCount(j, int_str) <= size)):
                    new_plist.append(And(i, j))
                    # print("and")


def find_and(plist):
    temp = []
    for i in plist:
        if (isinstance(i, Lt)):
            temp.append(i)
    return temp


class Lt(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def toString(self):
        return "(" + self.left.toString() + " < " + self.right.toString() + ")"

    def interpret(self, env):
        return self.left.interpret(env) < self.right.interpret(env)

    def grow(plist, new_plist, variables, int_str, size,dict):
        x = find_lt(plist, size,dict)
        for i in x:
            for j in x:
                if (i!= j and (nodeCount(i,int_str)+nodeCount(j,int_str)<=size)):
                    new_plist.append(Lt(i, j))



def find_lt(plist, size,dict):
    temp = []
    for i in range(1,size+1):
        if i in dict.keys():
            temp.extend(dict[i])
        for i in list(temp):
            if(isinstance(i,Lt) or isinstance(i,Not) or isinstance(i,And)):
                temp.remove(i)
    return temp




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

    def grow(plist, new_plist, variables, int_str, size,dict):
        x=find_condition(plist,dict,size)
        y=find_true_case(plist,dict,size,int_str)
        z=find_false_case(plist,dict,size,int_str)
        comb=itertools.product(x,y,z)
        for i in comb:
            if(nodeCount(i[0],int_str)+nodeCount(i[1],int_str)+nodeCount(i[2],int_str)<=size+3): # value 3 is used here by trial and error
                new_plist.append(Ite(i[0],i[1],i[2]))


def find_false_case(plist,dict,size,int_str):
    temp=[]
    for i in plist:
        if (isinstance(i, Num) or isinstance(i, Var) or isinstance(i, Plus) or isinstance(i,Times) and(nodeCount(i,int_str)<math.floor(size/3))):
            temp.append(i)
    return temp




def find_true_case(plist,dict,size,int_str):
    temp = []
    for i in range(1, size-2):
        if (i in dict.keys()):
            temp.extend(dict[i])
        for i in list(temp):
            if(isinstance(i,Lt) or isinstance(i,Not) or isinstance(i,And)):
                temp.remove(i)
    return temp

def find_condition(plist,dict,size):
    temp = []
    for i in range(1, size -2):
        if (i in dict.keys()):
            temp.extend(dict[i])
    for i in list(temp):
        if(not isinstance(i,Lt)):
            temp.remove(i)
    return temp


class Plus(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def toString(self):
        return "(" + self.left.toString() + " + " + self.right.toString() + ")"

    def interpret(self, env):
        return self.left.interpret(env) + self.right.interpret(env)

    def grow(plist, new_plist, variables, int_str, size,dict):
        x=find_programs(plist,dict,size,int_str)
        for i in variables:
            for j in x:
                new_plist.append(Plus(i, j))


def find_programs(plist,dict,size,int_str): #find the programs which can be combined in Plus and Times
    temp = []
    for i in range(1, math.floor(size/2)-1):
        if (i in dict.keys()):
            temp.extend(dict[i])
        for i in list(temp):
            if(isinstance(i,Lt) or isinstance(i,Not) or isinstance(i,And)):
                temp.remove(i)
    return temp


def nodeCount(p, int_str): #count the number of nodes in AST of a program
    return sum(p.toString().count(x) for x in ("x", "y", "+", "*", "<", "and","not")) + sum(p.toString().count(x) for x in int_str)



class Times(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def toString(self):
        return "(" + self.left.toString() + " * " + self.right.toString() + ")"

    def interpret(self, env):
        return self.left.interpret(env) * self.right.interpret(env)

    def grow(plist, new_plist, variables, int_str, size,dict):
        x=find_programs(plist,dict,size,int_str)
        for i in variables:
            for j in x:
                new_plist.append(Times(i, j))


class BottomUpSearch():
    def __init__(self):
        self.f = 0
        self.output = set()
        self.generated_program=0
        self.size=0

    def grow(self, plist, integer_operations, input_output, integer_values, dict,variables):
        new_plist = []
        max1 = 0
        max2 = 0
        self.size +=1
        size_list = []
        int_str = []

        for i in integer_values:
            int_str.append(str(i))
        for i in plist:
            size_list.append(nodeCount(i, int_str))
        size = max(size_list)



        # grow tree
        for op in integer_operations:
            op.grow(plist, new_plist, variables, int_str, self.size,dict)

        self.generated_program += len(new_plist)
        for i in range(0, len(new_plist)):
            out = []
            for j in input_output:
                out.append(new_plist[i].interpret(j))
            new_output = tuple(out)
            f3 = 0
            for j in self.output:
                if (j == new_output):
                    f3 = 1
                    break
            if (f3 == 0):
                length=nodeCount(new_plist[i],int_str)
                if(length in dict.keys()):
                    dict[length].append(new_plist[i])
                else:
                    dict[length]=[]
                    dict[length].append(new_plist[i])
                plist.append(new_plist[i])
                self.output.add(new_output)


    def synthesize(self, bound, integer_operations, integer_values, variables, input_output):
        plist = []
        #CREATE PROGRAM LIST WITH TERMINAL SYMBOLS
        for i in variables:
            plist.append(Var(i))
        for i in integer_values:
            plist.append(Num(i))
        self.generated_program += len(plist)

        #CREATE LIST COMBINING INTEGER VALUES AND VARIABLES
        var = []
        for i in variables:
            var.append(Var(i))
        for i in integer_values:
            var.append(Num(i))

        # CREATE TUPLE FOR OUTPUT
        for i in plist:
            out = []
            for j in input_output:
                out.append(i.interpret(j))
            self.output.add(tuple(out))


        #CREATE DICTIONARY
        int_str = []
        for i in integer_values:
            int_str.append(str(i))
        dict={}
        dict[1]=[]
        for i in plist:
            dict[1].append(i)

        flag = 0
        Number_of_eval = 0
        for i in range(bound):
            self.grow( plist, integer_operations, input_output, integer_values, dict,var)
            for j in range(Number_of_eval, len(plist)):
                Number_of_eval = Number_of_eval + 1
                if (self.iscorrect(plist[j], input_output)):
                    print("\nProgram: ", end=" ")
                    print(plist[j].toString())
                    print("Program Generated: ",  len(plist))
                    self.generated_program=0
                    print("Program Evaluated: ", Number_of_eval)
                    #print("Iteration Needed: ", i+1)
                    self.size=0
                    flag = 1
                    break

            if (flag == 1):
                break
        if (flag == 0):
            print("Program Generated: ", len(plist))
            print("Program Evaluated: ", Number_of_eval)
            print("No suitable program found within the search range")

    def iscorrect(self, prog, input_output):
        flag = 0
        for i in input_output:
            if (i['out'] == prog.interpret(i)):
                flag = flag + 1
        if (flag == len(input_output)):
            return True
        else:
            return False


synthesizer = BottomUpSearch()
start = time.time()
synthesizer.synthesize(10, [Lt, Ite], [1, 2], ['x', 'y'],[{'x': 5, 'y': 10, 'out': 5}, {'x': 10, 'y': 5, 'out': 5}, {'x': 4, 'y': 3, 'out': 3}])
end = time.time()
print(f"Execution time: {end - start}")

print("#############################################")
start = time.time()
synthesizer.synthesize(10, [And, Plus, Times, Lt, Ite, Not], [10], ['x', 'y'],[{'x': 5, 'y': 10, 'out': 5}, {'x': 10, 'y': 5, 'out': 5}, {'x': 4, 'y': 3, 'out': 4},{'x': 3, 'y': 4, 'out': 4}])
end = time.time()
print(f"Execution time: {end - start}")

print("#############################################")
start = time.time()
synthesizer.synthesize(10, [And, Plus, Times, Lt, Ite, Not], [-1, 5], ['x', 'y'],[{'x': 10, 'y': 7, 'out': 17}, {'x': 4, 'y': 7, 'out': -7}, {'x': 10, 'y': 3, 'out': 13},{'x': 1, 'y': -7, 'out': -6}, {'x': 1, 'y': 8, 'out': -8}])
end = time.time()
print(f"Execution time: {end - start}")

