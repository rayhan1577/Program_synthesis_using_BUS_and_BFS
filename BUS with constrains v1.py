import time
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
#abc
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
            prog=find_and(plist)
            for i in prog:
                for j in prog:
                    if(i!=j):
                        new_plist.append(And(i,j))
                        #print("and")

def find_and(plist):
    temp=[]
    for i in plist:
        if(isinstance(i,Lt)):
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

    def grow(plist, new_plist,int_str,size):
        x=find_lt(plist,size)
        print("hello")
        c_m=current_minimum(new_plist,int_str)
        for i in x:
            for j in x:
                if(i!=j):
                    new_plist.append(Lt(i,j))
                                 #print("LT")
def find_lt(plist,size):
    temp=[]
    for i in plist:
        if((isinstance(i,Var) or isinstance(i, Num) or isinstance(i, Plus) or isinstance(i,Times))):
            temp.append(i)
    return temp


def current_minimum(new_plist,int_str):
    if(len(new_plist)==0):
        return 0
    else:
        m_size = []
        for i in new_plist:
            m_size.append(nodeCount(i, int_str))
        return min(m_size)




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

    def grow(plist, new_plist,int_str,size):
        x=find_condition(plist)
        y=find_case(plist)
        c_m=current_minimum(new_plist,int_str)
        for i in x:
            for j in y:
                for k in y:
                    if(j!=k and (nodeCount(i,int_str)+nodeCount(j,int_str)+nodeCount(k,int_str)<=c_m)):
                        new_plist.append(Ite(i, j, k))





def find_case(plist):
    temp=[]
    for i in plist:
        if(isinstance(i,Num) or isinstance(i,Var) or isinstance(i,Plus) or isinstance(i,Times) ):
            temp.append(i)
    return temp

def find_condition(plist):
    temp=[]
    for i in plist:
        if(isinstance(i,Lt) or isinstance(i,And) or isinstance(i,Not)):
            temp.append(i)
    return temp

class Plus(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def toString(self):
        return "(" + self.left.toString() + " + " + self.right.toString() + ")"

    def interpret(self, env):
        return self.left.interpret(env) + self.right.interpret(env)

    def grow(plist, new_plist,a):
        for i in a:
            for j in plist:
                new_plist.append(Plus(i, j))

def nodeCount(p,int_str):
    return sum(p.toString().count(x) for x in ("x", "y", "+", "*", "<", "and")) + sum(p.toString().count(x) for x in int_str)

class Times(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def toString(self):
        return "(" + self.left.toString() + " * " + self.right.toString() + ")"

    def interpret(self, env):
        return self.left.interpret(env) * self.right.interpret(env)


    def grow(plist, new_plist,a):
        for i in a:
            for j in plist:
                new_plist.append(Times(i, j))
                        #print("times")



class BottomUpSearch():
    def __init__(self):
        self.f=0
        self.output= set()
        self.sample = open('a.txt', 'w')


    def grow(self, plist, integer_operations,input_output,integer_values,a):
        new_plist = []
        max1=0
        max2=0
        size=0
        size_list=[]
        int_str=[]

        for i in integer_values:
            int_str.append(str(i))
        for i in plist:
            size_list.append(nodeCount(i,int_str))
        size=max(size_list)
        #programs to be expanded
        #n_plist=self.findPrograms(plist,integer_operations,integer_values)




        # grow tree
        for op in integer_operations:
            if(op==Plus or op==Times):
                op.grow(plist, new_plist,a)
            elif(op==And or op==Not):
                op.grow(plist, new_plist)
            elif(op==Ite or op==Lt):
                op.grow(plist, new_plist,int_str,size)
                
                
            

        #Max height of the AST in current itiration:

        for i in range(0,len(new_plist)):
            out=[]
            for j in input_output:
                out.append(new_plist[i].interpret(j))
            new_output=tuple(out)
            f3=0
            for j in self.output:
                if(j==new_output):
                    f3=1
                    break
            if(f3==0):
                plist.append(new_plist[i])
                self.output.add(new_output)
        for i in plist:
            print(i.toString())


    def synthesize(self, bound, integer_operations, integer_values, variables, input_output):
        plist = []

        for i in variables:
            plist.append(Var(i))
        for i in integer_values:
            plist.append(Num(i))

        a=[]
        for i in variables:
            a.append(Var(i))
        for i in integer_values:
            a.append(Num(i))


        for i in  plist:
            out=[]
            for j in  input_output:
                out.append(i.interpret(j))
            self.output.add(tuple(out))

        int_str=[]
        for i in integer_values:
            int_str.append(str(i))

        """
        dict={}
        for i in plist:
            x=sum(i.toString().count(x) for x in ("x","y","+", "*", "<", "and","not","1","2")) + sum(i.toString().count(x) for x in int_str)
            t=Num(x)
            if t.toString() in dict.keys():
                dict[t.toString()].append(i)
            else:
                dict[t.toString()]=[]
                dict[t.toString()].append(i)
        """
        flag=0
        Number_of_eval = 0
        for i in range(bound):
            self.grow(plist, integer_operations,input_output,integer_values,a)
            for i in plist:
                print(i.toString(), file=self.sample)
            for j in range(Number_of_eval,len(plist)):
                Number_of_eval=Number_of_eval+1
                if(self.iscorrect(plist[j],input_output)):
                    print("\nProgram: ", end=" ")
                    print(plist[j].toString())
                    print("Program Generated: ", len(plist))
                    print("Program Evaluated: ", Number_of_eval)
                    flag=1
                    break
            if(flag==1):
                break
        if(flag==0):
            print("Program Generated: ", len(plist))
            print("Program Evaluated: ", Number_of_eval)
            print("No suitable program found within the search range")


    def iscorrect(self, prog, input_output):
        flag=0
        for i in input_output:
            if (i['out'] == prog.interpret(i)):
                flag=flag+1
        if(flag==len(input_output)):
            return True
        else:
            return False



synthesizer = BottomUpSearch()
start = time.time()
synthesizer.synthesize(3, [Lt, Ite], [1, 2], ['x', 'y'],[{'x': 5, 'y': 10, 'out': 5}, {'x': 10, 'y': 5, 'out': 5}, {'x': 4, 'y': 3, 'out': 3}])
end = time.time()
print(f"Runtime of the program is {end - start}")


print("#############################################")
start = time.time()
#synthesizer.synthesize(3, [And, Plus, Lt, Ite, Not], [10], ['x', 'y'],[{'x': 5, 'y': 10, 'out': 5}, {'x': 10, 'y': 5, 'out': 5}, {'x': 4, 'y': 3, 'out': 4},{'x': 3, 'y': 4, 'out': 4}])
end = time.time()
print(f"Runtime of the program is {end - start}")


print("#############################################")
start = time.time()
synthesizer.synthesize(6, [And, Plus, Times , Lt, Ite, Not], [-1, 5], ['x', 'y'], [{'x': 10, 'y': 7, 'out': 17},{'x': 4, 'y': 7, 'out': -7},{'x': 10, 'y': 3, 'out': 13},{'x': 1, 'y': -7, 'out': -6},{'x': 1, 'y': 8, 'out': -8}])
end = time.time()
print(f"Runtime of the program is {end - start}")



