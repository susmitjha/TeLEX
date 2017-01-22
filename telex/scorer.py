import sys
import math
from random import randint

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
    (maxtime, rangetime) = gettime(x, left, right)
    return all(qualitativescore(stl.subformula, x, min(t+t1, maxtime)) for t1 in rangetime)


@qualitativescore.register(Future)
def _(stl, x, t):
    (left, right) = stl.interval
    left = float(left) 
    right = float(right) 
    if left>right:
        raise ValueError("Interval [{},{}] empty for {}".format(left, right, stl))    
    (maxtime, rangetime) = gettime(x, left, right)
    return any(qualitativescore(stl.subformula, x, min(t+t1, maxtime)) for t1 in rangetime)


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
    raise NotImplementedError("No quantitativescore for {} of class {}".format(stl, stl.__class__))

@quantitativescore.register(Globally)
def _(stl, x, t):
    (left, right) = stl.interval
    (maxtime, rangetime) = gettime(x, left, right)
    return  min(quantitativescore(stl.subformula, x, min(t+t1, maxtime)) for t1 in rangetime)

@quantitativescore.register(Future)
def _(stl, x, t):
    (left, right) = stl.interval
    (maxtime, rangetime) = gettime(x, left, right)
    return max(quantitativescore(stl.subformula, x, min(t+t1, maxtime)) for t1 in rangetime)


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





@singledispatch
def smartscore(stl, x, t):
    raise NotImplementedError("No smartscore for {} of class {}".format(stl, stl.__class__))

@smartscore.register(Globally)
def _(stl, x, t):
    (left, right) = stl.interval
    intervalwidth = right - left + 1
    (maxtime, rangetime) = gettime(x, left, right)
    #rangetime =  x[(x['time'] <= right) & (x['time'] >= left)]["time"]
    return  2/(1 + math.exp(-0.01 * intervalwidth) ) * min(smartscore(stl.subformula, x, min(t+t1, maxtime)) for t1 in rangetime)

@smartscore.register(Future)
def _(stl, x, t):
    (left, right) = stl.interval
    intervalwidth = right - left + 1
    (maxtime, rangetime) = gettime(x, left, right)
    return  2/(1 + math.exp(0.01 * intervalwidth) ) * max(smartscore(stl.subformula, x, min(t+t1, maxtime)) for t1 in rangetime)


@smartscore.register(Or)
def _(stl, x, t):
    return max(smartscore(stl.left, x, t), smartscore(stl.right, x, t))

@smartscore.register(And)
def _(stl, x, t):
    return min(smartscore(stl.left, x, t), smartscore(stl.right, x, t))

@smartscore.register(Implies)
def _(stl, x, t):
    return max( (-1*  smartscore(stl.left, x, t) ), smartscore(stl.right, x, t) )

@smartscore.register(Not)
def _(stl, x, t):
    return -1 * smartscore(stl.subformula, x, t)

robusttable = { "<" : lambda x,y: y-x, "<=" : lambda x,y: y-x, ">" : lambda x,y: x-y , ">=": lambda x,y: x-y, "==" : lambda x,y: -abs(x,y) }

@smartscore.register(Constraint)
def _(stl, x, t):
    rawscore = robusttable[stl.relop](getval(stl.term, x, t), getval(stl.bound, x, t))
    
    #randomscorefun = randint(1,3)
    #if randomscorefun == 1:
    #return -0.6+1/(rawscore -1 + math.exp(-rawscore+1))
    #elif randomscorefun == 2:
    return 1/(rawscore + math.exp(-1*rawscore)) - math.exp(-1*rawscore) 
    #else :
    #    return rawscore*math.exp(1-rawscore)

@smartscore.register(Atom)
def _(stl, x, t):
    if x[stl.name][t]:
        return 1
    else:
        return 0




def gettime(x, left, right):
    ts = sorted(x['time'].keys())
    maxtime = ts[-1]
    rangetime = filter(lambda v: (v<= right) & (v >= left), ts)
    return maxtime, rangetime
