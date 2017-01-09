import telex.stl as stl
import telex.parametrizer as parametrizer
import telex.scorer as scorer
import telex.inputreader as inputreader
#import bayesopt
import numpy as np
import scipy.optimize 
from random import uniform
import logging
from time import clock
import os 



LOG_FILENAME = 'synth.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

def find_filenames (path, suffix=".csv"):
    filenames = os.listdir(path)
    return map(lambda x: os.path.join(path, x), [filename for filename in filenames if filename.endswith(suffix)] )

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


def simoptimize(stl, tracelist,scorefun=scorer.smartscore,optmethod='HYBRID'):
    prmlist = parametrizer.getParams(stl)
    prmcount = len(prmlist)
    lb = np.zeros((prmcount,))
    ub = np.ones((prmcount,))
    boundlist = []
    uniform_tuple = lambda t: uniform(*t)
    for prm in prmlist:
        boundlist.append((float(prm.left),float(prm.right)))
    start = clock()
    costfunc = lambda paramval : -1*cumscoretracelist(stl,paramval,tracelist,scorefun)
    done = False
    attempts = 0
    initguess = map(uniform_tuple, boundlist)
    bestCost = 0
    while not done and attempts < 10:
        attempts = attempts + 1
        if optmethod == 'HYBRID':
            if attempts % 2 == 0:
                res = scipy.optimize.minimize(costfunc, initguess, bounds=boundlist,method='L-BFGS-B')
            else:
                res = scipy.optimize.minimize(costfunc, initguess, bounds=boundlist,method='TNC')
        elif optmethod == 'DE':
            res = scipy.optimize.differential_evolution(costfunc, bounds = boundlist)
        else:
            res = scipy.optimize.minimize(costfunc, initguess, bounds=boundlist,method=optmethod)

        logging.debug("Attempt : {} with Cost: {}/{} Param: {}".format(attempts, res.fun, bestCost, res.x))
        if res.fun > 1.01* bestCost and res.fun < 0.99 * bestCost:
            done = True # Converged
        if res.fun < 0:
            if res.fun < bestCost:
                bestCost = res.fun
                bestX = res.x
            initguess = map(lambda e: 1.01*e,bestX)
        else:
            initguess = map(uniform_tuple, boundlist)

    if bestCost >= 0:
        raise ValueError("Template {} could not be completed. Rerun to try again. Numerical optimization experienced convergence problems.".format(stl))

    mvalue = bestCost
    x_out = bestX
    prmvalue = {}
    i = 0
    for prm in prmlist:
        prmvalue[prm.name] = x_out[i]
        i = i + 1
    stlfinal = parametrizer.setParams(stl, prmvalue)
    return (stlfinal, mvalue, clock()-start)






def bayesoptimize(stl, tracelist, iter_learn, iter_relearn, init_samples, mode, steps=10, NumAttempts = 10):
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
    costfunc = lambda paramval : -1*cumscoretracelist(stl,paramval,tracelist,scorer.smartscore)
    if mode == "discrete":
        steps = steps + 1
        x_set = np.zeros(shape = (prmcount, steps))
        i = 0
        for prm in prmlist:
            x_set[i] = np.linspace(lb[i],ub[i],steps)
            i = i + 1
        x_set = np.transpose(x_set)
        done = False
        attempts = 0
        while not done:
            attempts = attempts + 1
            print "Attempt: {}".format(attempts)
            if attempts >= NumAttempts:
                done = True
            try:
                mvalue, x_out, error = bayesopt.optimize_discrete(costfunc, x_set, params)
                if mvalue < 0:
                    done = True
                else:
                    print "Min cost is positive: {}".format(mvalue)

            except RuntimeError:
                print "Runtime error"
                #raise ValueError("Template {} could not be completed. Rerun to try again. Bayesian optimization experienced a nondeterministic (nonpersistent) runtime numerical error.".format(stl))

    elif mode == "continuous":
        done = False
        attempts = 0
        while not done:
            attempts = attempts + 1
            print "Attempt: {}".format(attempts)
            if attempts >= NumAttempts:
                done = True
            try:
                mvalue, x_out, error = bayesopt.optimize(costfunc, prmcount, lb, ub, params)
                if mvalue < 0:
                    done = True
                else:
                    print "Min cost is positive: {}".format(mvalue)
            except RuntimeError:
                print "Runtime error"
                #raise ValueError("Template {} could not be completed. Rerun to try again. Bayesian optimization experienced a nondeterministic (nonpersistent) runtime numerical error.".format(stl))
        
    #print "Final cost is", mvalue, " at ", x_out
    #print "Synthesis time:", clock() - start, "seconds"
    prmvalue = {}
    i = 0
    for prm in prmlist:
        prmvalue[prm.name] = x_out[i]
        i = i + 1
    stlfinal = parametrizer.setParams(stl, prmvalue)
    return (stlfinal, mvalue, clock()-start)




def synthSTLParam(tlStr, tracedir, optmethod = 'DE'):
    stlex = stl.parse(tlStr)
    param = parametrizer.getParams(stlex)
    logging.debug("\nTo Synthesize STL Template: {}".format(stlex))
   
    tracenamelist = find_filenames (tracedir, suffix=".csv")
    tracelist = []
    for tracename in tracenamelist:
        tracelist.append(inputreader.readtracefile(tracename))

    #stlsyn = synth.bayesoptimize(stlex, [x,x1], 50, 1, 2, "discrete", steps = 10)
    #stlsyn, value, dur = synth.bayesoptimize(stlex, [x,x1], 100, 1, 2, "continuous")

    stlsyn, value, dur = simoptimize(stlex, tracelist, optmethod = optmethod)
    logging.debug("Synthesized STL: {}".format(stlsyn))
    logging.debug("Synthesis: Cost is {}, Time taken is {}".format(value, dur))
    return stlsyn, value, dur


def verifySTL(stlex, tracedir):
    #param = parametrizer.getParams(stlex) -- add check that this is empty list
    #logging.debug("Testing STL: {} on trajectories in {} ", stlex, tracedir)
    tracenamelist = find_filenames (tracedir, suffix=".csv")
    tracelist = []
    for tracename in tracenamelist:
        tracelist.append(inputreader.readtracefile(tracename))
    boolscorelist = []
    quantscorelist = []
    for trace in tracelist:
        try:
            boolscorelist.append(scorer.qualitativescore(stlex, trace, 0))
            quantscorelist.append(scorer.quantitativescore(stlex, trace, 0))
        except ValueError:
            boolscorelist.append( False )
            quantscorelist.append(-float('inf'))
    return boolscorelist,quantscorelist
