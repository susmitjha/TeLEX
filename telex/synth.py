import stl
import parametrizer
import bayesopt
import numpy as np
import scorer

from time import clock


def explore(paramlist):
    paramvalue = {} 
    for param in paramlist:
        paramvalue[param.name] = param.left 
    return paramvalue


def quantscoretracelist(stl, tracelist, paramvalue):
    score = 0;
    paramlist = parametrizer.getParams(stl)
    valmap = {}
    i = 0
    for param in paramlist:
        valmap[param.name] = paramvalue[i]
        i = i + 1
    stlcand = parametrizer.setParams(stl, valmap)
    for trace in tracelist:
        try:
            quantscore = scorer.quantitativescore(stlcand, trace, 0)
            #print(stlcand, trace)
            #print(quantscore)
        except ValueError:
            quantscore = -10000
        score = score + quantscore 
    return -score

def bayesoptimize(stl, tracelist, iter_learn, iter_relearn, init_samples, mode, steps=10):
    params = {}
    params['n_iterations'] = iter_learn
    params['n_iter_relearn'] = iter_relearn
    params['n_init_samples'] = init_samples
    prmlist = parametrizer.getParams(stl)
    prmcount = len(prmlist)
    start = clock()
    costfunc = lambda paramval : quantscoretracelist(stl,tracelist,paramval)
    if mode == "discrete":
        steps = steps + 1
        x_set = np.zeros(shape = (prmcount, steps))
        i = 0
        for prm in prmlist:
            x_set[i] = np.linspace(lb[i],ub[i],steps)
            i = i + 1
        x_set = np.transpose(x_set)
        mvalue, x_out, error = bayesopt.optimize_discrete(costfunc, x_set, params)
    elif mode == "continuous":
        lb = np.zeros((prmcount,))
        ub = np.ones((prmcount,))
        i = 0
        for prm in prmlist:
            lb[i] = float(prm.left)
            ub[i] = float(prm.right)
            i = i +1 
        mvalue, x_out, error = bayesopt.optimize(costfunc, prmcount, lb, ub, params)
        
    print "Final cost is", mvalue, " at ", x_out
    print "Synthesis time:", clock() - start, "seconds"
    prmvalue = {}
    i = 0
    for prm in prmlist:
        prmvalue[prm.name] = x_out[i]
        i = i + 1
    stlfinal = parametrizer.setParams(stl, prmvalue)
    return stlfinal
