import telex.stl as stl
import telex.parametrizer as parametrizer
import telex.scorer as scorer
import bayesopt
import numpy as np


from time import clock


def explore(paramlist):
    paramvalue = {} 
    for param in paramlist:
        paramvalue[param.name] = param.left 
    return paramvalue


def cumscoretracelist(stl, paramvalue, tracelist, scorerfun):
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
            quantscore = scorerfun(stlcand, trace, 0)
        except ValueError:
            quantscore = -10000
        score = score + quantscore 
    return score

def bayesoptimize(stl, tracelist, iter_learn, iter_relearn, init_samples, mode, steps=10):
    params = {}
    params['n_iterations'] = iter_learn
    params['n_iter_relearn'] = iter_relearn
    params['n_init_samples'] = init_samples
    params['verbose_level'] = 5
    prmlist = parametrizer.getParams(stl)

    prmcount = len(prmlist)
    lb = np.zeros((prmcount,))
    ub = np.ones((prmcount,))
    i = 0
    for prm in prmlist:
        lb[i] = float(prm.left)
        ub[i] = float(prm.right)
        i = i +1 
    start = clock()
    costfunc = lambda paramval : -1*cumscoretracelist(stl,paramval,tracelist,scorer.quantitativescore)
    if mode == "discrete":
        steps = steps + 1
        x_set = np.zeros(shape = (prmcount, steps))
        i = 0
        for prm in prmlist:
            x_set[i] = np.linspace(lb[i],ub[i],steps)
            i = i + 1
        x_set = np.transpose(x_set)
        try:
            mvalue, x_out, error = bayesopt.optimize_discrete(costfunc, x_set, params)
        except RuntimeError:
            raise RuntimeError("Template {} could not be completed. Rerun to try again. Bayesian optimization experienced a nondeterministic (nonpersistent) runtime numerical error.".format(stl))
    elif mode == "continuous":
        try:
            mvalue, x_out, error = bayesopt.optimize(costfunc, prmcount, lb, ub, params)
        except RuntimeError:
            raise RuntimeError("Template {} could not be completed. Rerun to try again. Bayesian optimization experienced a nondeterministic (nonpersistent) runtime numerical error.".format(stl))
        
    #print "Final cost is", mvalue, " at ", x_out
    #print "Synthesis time:", clock() - start, "seconds"
    prmvalue = {}
    i = 0
    for prm in prmlist:
        prmvalue[prm.name] = x_out[i]
        i = i + 1
    stlfinal = parametrizer.setParams(stl, prmvalue)
    return (stlfinal, mvalue, clock()-start)
