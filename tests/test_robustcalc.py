import pytest
from telex.stl import parse
from telex.parametrizer import getParams, setParams
from telex.synth import explore
from telex.scorer import qualitativescore, quantitativescore, smartscore
import telex.inputreader as inputreader
import pandas

#x1 range(1,10)
#x2 range(1,10)
#x3 bool
#t [1-10]

templogicdata = [
    'x1 > 2',
    'x1 > a? 1;10',
    '!x3',
    '!(x1 > 4)',
    '!(x1 > asa? 2;10)',
    '((x1 > 2) | ((x2 > 2) | (x2 <= 5)))',
    '((x1 > 2) | ((x2 < 4) & (x1 < 5)))',
    '((x1 > 2) | ((x1 > 2) & !(x1 > 2)))',
    'F[0,1](x1 > 2)',
    'G[2,3] F[0,1] (x1 > 2)',
    'F[0,1]((x1 > 2) | ((x1 < 6) | !(x2 > 2)))',
    'G[0, b? 3;6](x1 > a? 2.5;9.2)',
    'F[0,1](x3)',
    '(({x1 + x2} > 2) | ((x1 > 4) & !(x2 > 2)))',
    'F[0,1]({x1 - x2} > 2)',
    'G[2,3]F[0,1]({x1 * x2} > 2)',
    'F[0,2](({x1 / x2} > ab? 0;0.5) | (({{x1 * x2} + x1} > 2) | !(x1 > 2)))',
    'G[0, b? 3;10]({x1 + x2} > a? 2.1;2.2)',
    ' ( (x1 > 6)-> x3 ) ',
    'F[0,2](({x1 / x2} > ab? 0.1;0.9) -> (({{x1 * x2} + x1} > 2) -> !(x1 > 2)))',
    'U[0,1.33] (x1 <= 10, x2<=5)',
    'U[0,2] (x1 >= 4, x2 >= 1)'
]



@pytest.mark.parametrize("tlStr", templogicdata)
def test_stl(tlStr):
    stl = parse(tlStr)
    param = getParams(stl)
    valmap = explore(param)
    stl1 = setParams(stl, valmap)
    #print(stl)
    print(stl1)
    #x = pandas.DataFrame([[1,2, True], [1,4, True], [4,2, False], [1,2, True], [1,4, True], [4,2, False], [1,2, True], [1,4, True], [4,2, False], [4,2, False]], index=[0,1,2,3,4,5,6,7,8,9], columns=["x1", "x2", "x3"])
    x = inputreader.readtracefile("traces/trace2.csv")
    try:
        boolscore = qualitativescore(stl1, x, 0)
        print(boolscore)
    except ValueError:
        print("Value error")
    try:
        quantscore = quantitativescore(stl1, x, 0)
        print(quantscore)
    except ValueError:
        print("Value error in quant")
    try:
        sscore = smartscore(stl1, x, 0)
        print(sscore)
    except ValueError:
        print("Value error in smart")        
  
def main():
    for templ in templogicdata:
        test_stl(templ)

if __name__ == "__main__":
    main()

