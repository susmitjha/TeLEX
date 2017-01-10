from telex.stl import *

def getParamsDir(stl, dir):
    if isinstance(stl, Globally):
        return list(set().union(getParamsDir(stl.interval, 1), getParamsDir(stl.subformula, 0) ) )
    elif isinstance(stl, Future):
        return list(set().union(getParamsDir(stl.interval, -1), getParamsDir(stl.subformula, 0) ) )
    elif isinstance(stl, Interval):
        #For intervals
        #dir 1 means, expand as much as possible
        #dir -1 means contract as much as possible
        if dir==1:
            return list(set().union(getParamsDir(stl.left, -1), getParamsDir(stl.right, 1))) 
        elif dir == -1:
            return list(set().union(getParamsDir(stl.left, 1), getParamsDir(stl.right, -1)))      
        else:
            raise NotImplementedError
    elif isinstance(stl, (Or, And, Implies, Expr)):
        return list(set().union(getParamsDir(stl.left, 0), getParamsDir(stl.right, 0)))
    elif isinstance(stl,Not):
        return getParamsDir(stl.subformula, 0)
    elif isinstance(stl, Constraint):
        if (stl.relop == "<" or stl.relop == "<="):
            return list(set().union(getParamsDir(stl.term,0), getParamsDir(stl.bound, -1)))
        elif (stl.relop == ">" or stl.relop == ">="):
            return list(set().union(getParamsDir(stl.term,0), getParamsDir(stl.bound, 1)))
        else:
            list(set().union(getParamsDir(stl.term,0), getParamsDir(stl.bound, 0)))
    elif isinstance(stl, (Atom, Var)):
        return []
    elif isinstance(stl, Param):
        #For params
        #dir 1 means, increase as much as possible
        #dir -1 means decrease as much as possible
        return [(stl.name, dir)]
    elif isinstance(stl, Constant):
        return []
    else:
        return NotImplementedError



def getParams(stl):
    if isinstance(stl, (Globally, Future)):
        return list(set().union(getParams(stl.interval), getParams(stl.subformula)))
    elif isinstance(stl, (Interval, Or, And, Implies, Expr)):
        return list(set().union(getParams(stl.left), getParams(stl.right)))
    elif isinstance(stl,Not):
        return getParams(stl.subformula)
    elif isinstance(stl, Constraint):
        return list(set().union(getParams(stl.term), getParams(stl.bound)))
    elif isinstance(stl, (Atom, Var)):
        return []
    elif isinstance(stl, Param):
        return [stl]
    elif isinstance(stl, Constant):
        return []
    else:
        return NotImplementedError



def setParams(stl,valuemap):
    if isinstance(stl, (Globally, Future)):
        return eval(type(stl).__name__)(setParams(stl.interval, valuemap),setParams(stl.subformula, valuemap) )
    elif isinstance(stl, (Interval, Or, And, Implies)):
        return eval(type(stl).__name__)(setParams(stl.left,valuemap),setParams(stl.right, valuemap))
    elif isinstance(stl, Expr):
        return eval(type(stl).__name__)(stl.arithop, setParams(stl.left,valuemap),setParams(stl.right, valuemap))
    elif isinstance(stl,Not):
        return eval(type(stl).__name__)(setParams(stl.subformula, valuemap))
    elif isinstance(stl, Constraint):
        return eval(type(stl).__name__)(stl.relop, setParams(stl.term, valuemap), setParams(stl.bound, valuemap))
    elif isinstance(stl, (Atom, Var)):
        return stl
    elif isinstance(stl, Param):
        return Constant(valuemap[stl.name])
    elif isinstance(stl, Constant):
        return stl
    else:
        return NotImplementedError 

