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
    score = 0; #-10000; #proxy for -inf, putting -inf makes optimizers angry
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
            quantscore = -10000 #proxy for -inf, putting -inf makes optimizers angry
        score = (score + quantscore) 
    return score


def minscoretracelist(stl, paramvalue, tracelist, scorerfun):
    score = 10000; #proxy for inf, putting inf makes optimizers angry
    paramlist = parametrizer.getParams(stl)
    stlcand = parametrizer.setParams(stl, paramvalue)
    for trace in tracelist:
        try:
            quantscore = scorerfun(stlcand, trace, 0)
        except ValueError:
            quantscore = -10000 #proxy for -inf, putting -inf makes optimizers angry
        score = min(score, quantscore) 
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
    i = 0
    pvalue = {}
    for prm in prmlist:
        pvalue[prm.name] = x_out[i]
        i = i + 1
    return (pvalue, mvalue, clock()-start)






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
    return (x_out, mvalue, clock()-start)


def stretchsearch(prm, lbound, ubound, costfunc, pvalue_mut, decinc):
    #pvalue_mut is dictionary and hence, mutable, so create copy before doing anything with it
    pvalue = pvalue_mut.copy()
    
    c = costfunc(pvalue)
    if c> 0: 
        return pvalue[prm.name]
    epsilon = 0.01
    while c <= 0 and ubound - lbound > epsilon:
        pvalue[prm.name] = (ubound + lbound)/2
        c = costfunc(pvalue)
        print(c, pvalue)
        if decinc == "dec":
            if c >= 0:
                return pvalue[prm.name]
            else:
                ubound = pvalue[prm.name]
        elif decinc == "inc":
            if c >= 0:
                return pvalue[prm.name]
            else:
                lbound = pvalue[prm.name]
        else: 
            raise ValueError("Strech is incorrect for {}".format(prm.name))

    raise ValueError("No value possible for {}".format(prm.name))

def pbinsearch(prm, lbound, ubound, costfunc, pvalue_mut, decinc):
    #pvalue_mut is dictionary and hence, mutable, so create copy before doing anything with it
    pvalue = pvalue_mut.copy()

    epsilon = 0.01
    while ubound - lbound >= epsilon:
        pvalue[prm.name] = (ubound + lbound)/2
        c = costfunc(pvalue)
 #       print decinc, ubound, lbound, pvalue[prm.name], c
        if decinc == "dec":
            if c >= 0:
                ubound = pvalue[prm.name]
            else:
                lbound = pvalue[prm.name]
        elif decinc == "inc":
            if c >= 0:
                lbound = pvalue[prm.name]
            else:
                ubound = pvalue[prm.name]
        else: 
            raise ValueError("Roundupdown is incorrect for {}".format(prm.name))

    if decinc == "dec":
        return ubound 
    elif decinc == "inc":
        return lbound
    else: 
        raise ValueError("Roundupdown is incorrect for {}".format(prm.name))

    

def postProcess(stlex, pvalue, dirparams, tracelist):
    prmlist = parametrizer.getParams(stlex)
    prmcount = len(prmlist)
    boundlist = []
    for prm in prmlist:
        boundlist.append((float(prm.left),float(prm.right)))

    costfunc = lambda pvalue : minscoretracelist(stlex,pvalue,tracelist,scorer.quantitativescore)

    
    # expand to ensure all traces satisfy the stl property
    prmvalue = {}
    i = 0
    for prm in prmlist:
        #binary search between pvalue[prm.name] and lower/upper from boundlist
        lbound, ubound = boundlist[i]
        i = i + 1
        if (prm.name,1) in dirparams: #decrease will try to satisfy 
            prmvalue[prm.name] = stretchsearch(prm, lbound, pvalue[prm.name], costfunc, pvalue, "dec")
        elif (prm.name,-1) in dirparams: #increase will try to satisfy
            prmvalue[prm.name] = stretchsearch(prm, pvalue[prm.name], ubound, costfunc, pvalue, "inc")
        else:
            raise ValueError("Can't synthesize equality parameter: {}".format(prm.name))

    
   
    #prmvalue  = pvalue

    # contract till all traces still satisfy the stl property
    paramvalue = {}
    i = 0
    for prm in prmlist:
        #binary search between pvalue[prm.name] and lower/upper from boundlist
        lbound, ubound = boundlist[i]
        i = i + 1
        if (prm.name,1) in dirparams: #increase till possible 
            paramvalue[prm.name] = pbinsearch(prm, prmvalue[prm.name], ubound, costfunc, prmvalue, "inc")
        elif (prm.name,-1) in dirparams: #decrease till possible 
            paramvalue[prm.name] = pbinsearch(prm, lbound, prmvalue[prm.name], costfunc, prmvalue, "dec")
        else:
            paramvalue[prm.name] = prmvalue[prm.name]

    return paramvalue
    


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

    pvalue, value, dur = simoptimize(stlex, tracelist, optmethod = optmethod)
    dirparams = parametrizer.getParamsDir(stlex, 0)
    #print(dirparams)
    ppvalue = postProcess(stlex, pvalue, dirparams, tracelist) 
    #print(pvalue, ppvalue)
    stlsyn = parametrizer.setParams(stlex, ppvalue)

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
