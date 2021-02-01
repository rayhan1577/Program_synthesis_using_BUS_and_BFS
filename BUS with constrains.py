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
        return 'not (' + self.left.toString() + ')'

    def interpret(self, env):
        return not (self.left.interpret(env))

    def grow(plist, new_plist,size):
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

    def grow(plist, new_plist,size):
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

    def grow(plist, new_plist,size):
        for i in plist:
            if(isinstance(i,Var) or isinstance(i,Num) or isinstance(i,Plus) or isinstance(i,Times)):
                for j in plist:
                    if(i!=j):
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

    def grow(plist, new_plist,size):
        print(size)
        for i in plist:
            if((sum(i.toString().count(x) for x in ("x", "y", "+", "*", "<", "and","not")))+3<size):
                if(isinstance(i,Lt) or isinstance(i,And) or isinstance(i,Not)):
                    for j in plist:
                        if(isinstance(j,Var) or isinstance(j,Times) or isinstance(j,Ite)or isinstance(j,Plus)):
                            for k in plist:
                                    if(isinstance(k,Var) or isinstance(k,Times)or isinstance(k,Ite)):
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

    def grow(plist, new_plist,size):
        for i in plist:
            if(isinstance(i,Var) or isinstance(i,Plus) or isinstance(i,Times)or isinstance(i, Ite)):
                for j in plist:
                    if (isinstance(j, Var) or isinstance(j, Plus) or isinstance(j, Times)or isinstance(j, Ite)):
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


    def grow(plist, new_plist,size):
        for i in plist:
            if (isinstance(i, Var) or isinstance(i, Plus) or isinstance(i, Times) or isinstance(i, Ite) ):
                 for j in plist:
                    if (isinstance(j, Var) or isinstance(j, Plus) or isinstance(j, Times)or isinstance(j, Num)or isinstance(j, Ite)):
                        new_plist.append(Times(i, j))
                        #print("times")



class BottomUpSearch():
    def __init__(self):
        self.f=0
        self.output= set()
        self.sample = open('a.txt', 'w')

    def grow(self, plist, integer_operations,input_output,integer_values):
        new_plist = []
        max1=0
        max2=0
        size=0
        int_str=[]
        for i in integer_values:
            int_str.append(str(i))
        #max height of the AST in last itiration:
        size_list=[]
        for i in plist:
            size_list.append((sum(i.toString().count(x) for x in ("x", "y", "+", "*", "<", "and","not","1","2")) + sum(i.toString().count(x) for x in int_str)))
        size=max(size_list)+2



        # grow tree
        for op in integer_operations:
            op.grow(plist, new_plist,size)

        """
        #min height of the AST in current itiration:
        size_list=[]
        for i in new_plist:
            size_list.append((sum(i.toString().count(x) for x in ("x", "y", "+", "*", "<", "and","not","1","2")) + sum(i.toString().count(x) for x in int_str)))
        max2=max(size_list)

        size=max1+1
        while(True):
            if size in size_list:
                break
            size+=1

        for i in list(new_plist):
            if ((sum(i.toString().count(x) for x in ("x", "y", "+", "*", "<", "and","not","1","2")) + sum(i.toString().count(x) for x in int_str))>size):
                new_plist.remove(i)
        """
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


    def synthesize(self, bound, integer_operations, integer_values, variables, input_output):
        plist = [Var("x"),Var("y")]
        for i in integer_values:
            plist.append(Num(i))
        for i in  plist:
            out=[]
            for j in  input_output:
                out.append(i.interpret(j))
            self.output.add(tuple(out))
        flag=0
        Number_of_eval = 0
        for i in range(bound):
            self.grow(plist, integer_operations,input_output,integer_values)
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
                flag=0
                break


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
synthesizer.synthesize(16, [Lt, Ite], [1, 2], ['x', 'y'],[{'x': 5, 'y': 10, 'out': 5}, {'x': 10, 'y': 5, 'out': 5}, {'x': 4, 'y': 3, 'out': 3}])
end = time.time()
print(f"Runtime of the program is {end - start}")


print("#############################################")
start = time.time()
synthesizer.synthesize(20, [And, Plus, Lt, Ite, Not], [10], ['x', 'y'],[{'x': 5, 'y': 10, 'out': 5}, {'x': 10, 'y': 5, 'out': 5}, {'x': 4, 'y': 3, 'out': 4},{'x': 3, 'y': 4, 'out': 4}])
end = time.time()
print(f"Runtime of the program is {end - start}")


print("#############################################")
start = time.time()
synthesizer.synthesize(6, [And, Plus, Times , Lt, Ite, Not], [-1, 5], ['x', 'y'], [{'x': 10, 'y': 7, 'out': 17},{'x': 4, 'y': 7, 'out': -7},{'x': 10, 'y': 3, 'out': 13},{'x': 1, 'y': -7, 'out': -6},{'x': 1, 'y': 8, 'out': -8}])
end = time.time()
print(f"Runtime of the program is {end - start}")


