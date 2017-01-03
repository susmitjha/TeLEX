import pytest
import telex.stl as stl
import telex.parametrizer as parametrizer
import telex.synth as synth
import telex.scorer as scorer
import telex.inputreader as inputreader
import pandas

#templogicdata =  'G[0,6] F[b? 1;6,  a? 4;6](x1 > 2)'
templogicdata =  [
    'G[b? 1;6,  a? 1;9](x1 > 2)',
    'G[0,5] F[a? 0;3, b? 0;5] (x1 > 2)',
    'G[0,5] F[1, b? 0;5] (x1 > 2)',
    'G[0,5] F[a? 0;2 , 2] (x1 > 2)',
    'G[0,5] F[a? 1;2 , 3] (x1 > 2)',
    'G[0,9] ({ x2 - x1 } < a? 0;5 )',
]

@pytest.mark.parametrize("tlStr", templogicdata)
def test_stl(tlStr):
    stlex = stl.parse(tlStr)
    param = parametrizer.getParams(stlex)
    #print(param, len(param))
    print("\nSTL Template: {}".format(stlex))
   
    x = inputreader.readtracefile("traces/trace1.csv")
    x1 = inputreader.readtracefile("traces/trace2.csv")

    '''
    valmap = synth.explore(param) 
    stlex1 = parametrizer.setParams(stlex, valmap)
    print("Testing parameter setter: ", stlex1)
    try:
        boolscore = scorer.qualitativescore(stlex1, x, 0)
        quantscore = scorer.quantitativescore(stlex1, x, 0)
    except ValueError:
        boolscore = False
        quantscore = -float('inf')

    print("Testing scorer: ", boolscore, quantscore)
    '''
    
    #stlsyn = synth.bayesoptimize(stlex, [x,x1], 50, 1, 2, "discrete", steps = 10)
    stlsyn, value, dur = synth.bayesoptimize(stlex, [x,x1], 50, 1, 2, "continuous")
    print("Synthesized STL: {}".format(stlsyn))
    print("Synthesis: Cost is {}, Time taken is {}".format(value, dur))
    try:
        boolscore = scorer.qualitativescore(stlsyn, x, 0)
        quantscore = scorer.quantitativescore(stlsyn, x, 0)
    except ValueError:
        boolscore = False
        quantscore = -float('inf')

    print("Testing synthesized STL on one trace: ", boolscore, quantscore)
    
#test_stl(templogicdata)
