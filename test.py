def f(x, y):
    if y==0:
        return x
    return f(x+1, y-1)
    
def g(x, y):
    if y==0:
        return 0
    if y%2==0:
        return g(f(x, x), y/2)
    return f(g(x, y-1), x)

def h(x, y):
    if y==0:
        return 1
    return g(h(x, y-1), x)

def i(x, y):
    if(x < y):
        return 0
    return f(1, i(x-y, y))

def SlowSolve(x, y):
    return f(x, y) + g(x, y) + h(x, y) + i(x, y) 
    
print(SlowSolve(2,2))