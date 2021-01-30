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
        return 'not (' + self.left.toString() + ')'

    def interpret(self, env):
        return not (self.left.interpret(env))

    def grow(plist, new_plist):
        for i in plist:
            if(isinstance(i,Lt)):
                new_plist.append(Not(i))
                #print("not")



class And(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def toString(self):
        return "(" + self.left.toString() + " and " + self.right.toString() + ")"

    def interpret(self, env):
        return self.left.interpret(env) and self.right.interpret(env)

    def grow(plist, new_plist):
        #print(len(plist))
        for i in plist:
            if (isinstance(i, Lt)):
                for j in plist:
                    if (isinstance(j, Lt)):
                        #print(len(plist))
                        new_plist.append(And(i,j))
                        #print("and")


class Lt(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def toString(self):
        return "(" + self.left.toString() + " < " + self.right.toString() + ")"

    def interpret(self, env):
        return self.left.interpret(env) < self.right.interpret(env)

    def grow(plist, new_plist):
        for i in plist:
            if(isinstance(i,Var) or isinstance(i,Num) or isinstance(i,Plus) or isinstance(i,Times)):
                for j in plist:
                    if (isinstance(j, Var) or isinstance(j, Num) or isinstance(j, Plus) or isinstance(j, Times)):
                             new_plist.append(Lt(i,j))
                             #print("LT")







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

    def grow(plist, new_plist):
        for i in plist:
            if(isinstance(i,Lt) or isinstance(i,And) or isinstance(i,Not)):
                for j in plist:
                    if(isinstance(j,Var) or isinstance(j,Plus) or isinstance(j,Times)):
                        for k in plist:
                            if(isinstance(k,Var)or isinstance(k,Plus) or isinstance(k,Times)):
                                new_plist.append(Ite(i,j,k))
                                #print("lte")

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
        for i in plist:
            if(isinstance(i,Var) or isinstance(i,Plus) or isinstance(i,Times)or isinstance(i,Ite)):
                for j in plist:
                    if (isinstance(j, Var) or isinstance(j, Plus) or isinstance(j, Times)or isinstance(j,Ite)):
                        new_plist.append(Plus(i,j))
                        #print("plus")

class Times(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def toString(self):
        return "(" + self.left.toString() + " * " + self.right.toString() + ")"

    def interpret(self, env):
        return self.left.interpret(env) * self.right.interpret(env)


    def grow(plist, new_plist):
        for i in plist:
            if (isinstance(i, Var) or isinstance(i, Plus) or isinstance(i, Times) or isinstance(i, Ite)):
                 for j in plist:
                    if (isinstance(j, Var) or isinstance(j, Plus) or isinstance(j, Times) or isinstance(j, Ite)):
                        new_plist.append(Times(i, j))
                        #print("times")



class BottomUpSearch():
    def grow(self, plist, integer_operations,input_output):
            new_plist = []
            size = []
            #calculate maximum size of the tree in the previous iteration
            for j in range(len(plist)):
                size.append(plist[j].toString().count("+") + plist[j].toString().count("*") + plist[j].toString().count("<") + plist[j].toString().count("if") + plist[j].toString().count("not") + plist[j].toString().count("x") + plist[j].toString().count("y"))
            m2=max(size)

            #grow tree
            for op in integer_operations:
                op.grow(plist,new_plist)


            # CALCULATE minimum number higher then the AST SIZE
            size = []
            for j in range(len(new_plist)):
                size.append(new_plist[j].toString().count("+") + new_plist[j].toString().count("*") + new_plist[j].toString().count("<") + new_plist[j].toString().count("if") + new_plist[j].toString().count("not")+new_plist[j].toString().count("x")+new_plist[j].toString().count("y"))

            #set the maximum size of AST in current iteration
            m=min(size)
            if(m<=m2):
                if(m==m2):
                    x=m+1
                else:
                    x=m2+1
                while(True):
                    if(x in size):
                        m=x
                        break
                    x=x+1


            #print("lenght of newplist",len(new_plist))
           # print("minimum value",m)

            #remove AST having larger than the preset size
            for j in list(new_plist):
                if(j.toString().count("+") + j.toString().count("*") + j.toString().count("<") + j.toString().count("if") + j.toString().count("not")+j.toString().count("x")+j.toString().count("y")>m):
                    new_plist.remove(j)

            #insert programs from new_plist to p_list
            dummy = []
            for j in new_plist:
                flag = 0
                for k in plist:
                    #print("compare")
                    flag2 = 0
                    for l in input_output:
                        if (j.interpret(l) == k.interpret(l)):
                            flag2 = flag2 + 1
                    if (flag2 == len(input_output)):
                        flag = flag + 1
                if (flag == 0):
                    dummy.append(j)
            plist.extend(dummy)




    def synthesize(self, bound, integer_operations, integer_values, variables, input_output):
        plist = [Var("x"),Var("y")]
        flag=0
        Number_of_eval = 0
        for i in range(bound):
            #print(i)
            self.grow(plist, integer_operations,input_output)

            for j in range(Number_of_eval,len(plist)):
                Number_of_eval=Number_of_eval+1
                if(self.iscorrect(plist[j],input_output)):
                    print("Program: ", end=" ")
                    print(plist[j].toString())
                    flag=1
                    break
            if(flag==1):
                break
        if(flag==0):
            print("No suitable program found in the search Bound")
        print("program Generated:", len(plist))
        print("Program evaluated:", Number_of_eval)

    def iscorrect(self, prog, input_output):
        flag=0
        #print("is correct")
        for i in input_output:
            if (i['out'] == prog.interpret(i)):
                flag=flag+1
        if(flag==len(input_output)):
            return True
        else:
            return False

from datetime import datetime
synthesizer = BottomUpSearch()
print(datetime.now().time())
synthesizer.synthesize(3, [Lt, Ite], [1, 2], ['x', 'y'],[{'x': 5, 'y': 10, 'out': 5}, {'x': 10, 'y': 5, 'out': 5}, {'x': 4, 'y': 3, 'out': 3}])
print(datetime.now().time())
synthesizer.synthesize(3, [And, Plus, Times, Lt, Ite, Not], [10], ['x', 'y'],[{'x': 5, 'y': 10, 'out': 5}, {'x': 10, 'y': 5, 'out': 5}, {'x': 4, 'y': 3, 'out': 4},{'x': 3, 'y': 4, 'out': 4}])
print(datetime.now().time())
synthesizer.synthesize(3, [And, Plus, Times, Lt, Ite, Not], [-1, 5], ['x', 'y'], [{'x': 10, 'y': 7, 'out': 17},{'x': 4, 'y': 7, 'out': -7},{'x': 10, 'y': 3, 'out': 13},{'x': 1, 'y': -7, 'out': -6},{'x': 1, 'y': 8, 'out': -8}])
print(datetime.now().time())



