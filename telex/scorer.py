import sys
if (sys.version_info > (3, 0)):
    from functools import singledispatch
else:
    from singledispatch import singledispatch

from telex.stl import *
import operator as op

@singledispatch
def qualitativescore(stl, x, t):
    raise NotImplementedError("No qualitativescore for {} of class {}".format(stl, stl.__class__))

@qualitativescore.register(Globally)
def _(stl, x, t):
    (left, right) = stl.interval
    left = float(left) 
    right = float(right)  
    if left>right:
        raise ValueError("Interval [{},{}] empty for {}".format(left, right, stl))
    return all(qualitativescore(stl.subformula, x, min(t+t1, x.index[-1])) for t1 in x[(x.index <= right) & (x.index >= left)].index)


@qualitativescore.register(Future)
def _(stl, x, t):
    (left, right) = stl.interval
    left = float(left) 
    right = float(right) 
    if left>right:
        raise ValueError("Interval [{},{}] empty for {}".format(left, right, stl))    
    return any(qualitativescore(stl.subformula, x, min(t+t1, x.index[-1])) for t1 in x[(x.index <= right) & (x.index >= left)].index)


@qualitativescore.register(Or)
def _(stl, x, t):
    return qualitativescore(stl.left, x, t) or qualitativescore(stl.right, x, t) 

@qualitativescore.register(And)
def _(stl, x, t):
    return qualitativescore(stl.left, x, t) and qualitativescore(stl.right, x, t) 

@qualitativescore.register(Implies)
def _(stl, x, t):
    return (not  qualitativescore(stl.left, x, t) ) or qualitativescore(stl.right, x, t)

@qualitativescore.register(Not)
def _(stl, x, t):
    return not qualitativescore(stl.subformula, x, t)

optable = { "<" : op.lt, ">" : op.gt, "<=" : op.le, ">=" : op.ge, "==": op.eq, "+" : op.add, "-" : op.sub, "*" : op.mul, "/" : op.truediv }


 
@qualitativescore.register(Constraint)
def _(stl, x, t):
    return optable[stl.relop](getval(stl.term, x, t), getval(stl.bound, x, t))

@qualitativescore.register(Atom)
def _(stl, x, t):
    return x[stl.name][t]


@singledispatch

def getval(term, x, t):
    raise NotImplementedError("No getval for {} of class {}".format(stl, stl.__class__))


@getval.register(Expr)
def _(term, x, t):
    return optable[term.arithop](getval(term.left, x, t), getval(term.right, x, t))

@getval.register(Var)
def _(term, x, t):
    return x[term.name][t]

@getval.register(Constant)
def _(term, x, t):
    return term 
    
@getval.register(Param)
def _(term, x, t):
    raise NotImplementedError("No getval for parameter {}".format(term))



@singledispatch
def quantitativescore(stl, x, t):
    raise NotImplementedError("No qualitativescore for {} of class {}".format(stl, stl.__class__))

@quantitativescore.register(Globally)
def _(stl, x, t):
    (left, right) = stl.interval
    return (right - left + 1) * min(quantitativescore(stl.subformula, x, min(t+t1, x.index[-1])) for t1 in x[(x.index <= right) & (x.index >= left)].index)

@quantitativescore.register(Future)
def _(stl, x, t):
    (left, right) = stl.interval
    return 1/(right - left + 1) * max(quantitativescore(stl.subformula, x, min(t+t1, x.index[-1])) for t1 in x[(x.index <= right) & (x.index >= left)].index)


@quantitativescore.register(Or)
def _(stl, x, t):
    return max(quantitativescore(stl.left, x, t), quantitativescore(stl.right, x, t))

@quantitativescore.register(And)
def _(stl, x, t):
    return min(quantitativescore(stl.left, x, t), quantitativescore(stl.right, x, t))

@quantitativescore.register(Implies)
def _(stl, x, t):
    return max( (-1*  quantitativescore(stl.left, x, t) ), quantitativescore(stl.right, x, t) )

@quantitativescore.register(Not)
def _(stl, x, t):
    return -1 * quantitativescore(stl.subformula, x, t)

#optable = { "<" : op.lt, ">" : op.gt, "<=" : op.le, ">=" : op.ge, "==": op.eq, "+" : op.add, "-" : op.sub, "*" : op.mul, "/" : op.truediv }

robusttable = { "<" : lambda x,y: y-x, "<=" : lambda x,y: y-x, ">" : lambda x,y: x-y , ">=": lambda x,y: x-y, "==" : lambda x,y: -abs(x,y) }

@quantitativescore.register(Constraint)
def _(stl, x, t):
    #print(stl,  robusttable[stl.relop](getval(stl.term, x, t), getval(stl.bound, x, t)) )
    return robusttable[stl.relop](getval(stl.term, x, t), getval(stl.bound, x, t))

@quantitativescore.register(Atom)
def _(stl, x, t):
    if x[stl.name][t]:
        return 1
    else:
        return 0

