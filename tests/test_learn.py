import pytest
import telex.stl as stl
import telex.parametrizer as parametrizer
import telex.synth as synth
import telex.scorer as scorer
import telex.inputreader as inputreader
import pandas

#templogicdata =  'G[0,6] F[b? 1;6,  a? 4;6](x1 > 2)'
templogicdata =  [
    'G[b? 1;6,  a? 4;6](x1 > 2)'
]

@pytest.mark.parametrize("tlStr", templogicdata)
def test_stl(tlStr):
    stlex = stl.parse(tlStr)
    param = parametrizer.getParams(stlex)
    print(param, len(param))
    valmap = synth.explore(param) 
    stlex1 = parametrizer.setParams(stlex, valmap)
    print("Testing parser: ", stlex)
    print("Testing parameter setter: ", stlex1)
    x = inputreader.readtracefile("traces/trace1.csv")
    x1 = inputreader.readtracefile("traces/trace2.csv")
    try:
        boolscore = scorer.qualitativescore(stlex1, x, 0)
        quantscore = scorer.quantitativescore(stlex1, x, 0)
    except ValueError:
        boolscore = False
        quantscore = -float('inf')

    print("Testing scorer: ", boolscore, quantscore)
    
    paramval = {}
    i = 0
    print(param)
    for p in param:
        paramval[i] = 5
        print(p, p.left)
        i = i+1
    print(paramval)
    #stlexscore = synth.quantscoretracelist(stlex, [x, x1], paramval)
    stlsyn = synth.bayesoptimize(stlex, [x,x1], 50, 1, 2, "discrete", steps = 10)
    #stlsyn = synth.bayesoptimize(stlex, [x,x1], 50, 1, 2, "continuous")
    print("Testing bayesopt synthesizer: {}".format(stlsyn))

    try:
        boolscore = scorer.qualitativescore(stlsyn, x, 0)
        quantscore = scorer.quantitativescore(stlsyn, x, 0)
    except ValueError:
        boolscore = False
        quantscore = -float('inf')

    print("Testing scorer: ", boolscore, quantscore)
    
#test_stl(templogicdata)
