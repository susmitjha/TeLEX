from telex.stl import *

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

