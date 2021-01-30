
def isodd(test):
    i=test%2
    if(i==1):
        return True
    else:
        return False

x=isodd(13)

if(x==True):
    print("odd Number")
else:
    print("Even Number")