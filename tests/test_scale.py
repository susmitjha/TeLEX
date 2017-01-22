import pytest
import telex.synth
import pandas
import numpy

#templogicdata =  'G[0,6] F[b? 1;6,  a? 4;6](x1 > 2)'
templogicdata =  [
    'G[0,1](x <= a? 0;12 & x >= b? -12;0 )',
    '(  G[0,1](x <= a? 0;12 & x >= b? -12;0 )  &  G[1,2](x <= c? 0;12 & x >= d? -12;0 ) )',
#    '( (  G[0,1](x <= a? 0;12 & x >= b? -12;0 )  &  G[1,2](x <= c? 0;12 & x >= d? -12;0 ) )  &  G[2,3](x <= e? 0;12 & x >= f? -12;0 )  ) ',
#    '( ( (  G[0,1](x <= a? 0;12 & x >= b? -12;0)  &  G[1,2](x <= c? 0;12 & x >= d? -12;0) )  &  G[2,3](x <= e? 0;12 & x >= f? -12;0)  ) & G[3,4](x <= g? 0;12 & x >= h? -12;0) )',
#    '( ( ( (  G[0,1](x <= a? 0;12 & x >= b? -12;0)  &  G[1,2](x <= c? 0;12 & x >= d? -12;0) )  &  G[2,3](x <= e? 0;12 & x >= f? -12;0)  ) & G[3,4](x <= g? 0;12 & x >= h? -12;0) ) & G[4,5](x <= i? 0;12 & x >= j? -12;0) )',
#    '( ( ( ( (  G[0,1](x <= a? 0;12 & x >= b? -12;0)  &  G[1,2](x <= c? 0;12 & x >= d? -12;0) )  &  G[2,3](x <= e? 0;12 & x >= f? -12;0)  ) & G[3,4](x <= g? 0;12 & x >= h? -12;0) ) & G[4,5](x <= i? 0;12 & x >= j? -12;0) ) & G[5,6](x <= k? 0;12 & x >= l? -12;0) )',
#    '( ( ( ( ( (  G[0,1](x <= a? 0;12 & x >= b? -12;0)  &  G[1,2](x <= c? 0;12 & x >= d? -12;0) )  &  G[2,3](x <= e? 0;12 & x >= f? -12;0)  ) & G[3,4](x <= g? 0;12 & x >= h? -12;0) ) & G[4,5](x <= i? 0;12 & x >= j? -12;0) ) & G[5,6](x <= k? 0;12 & x >= l? -12;0) ) & G[6,7](x <= m? 0;12 & x >= n? -12;0) )',
#    '( ( ( ( ( ( (  G[0,1](x <= a? 0;12 & x >= b? -12;0)  &  G[1,2](x <= c? 0;12 & x >= d? -12;0) )  &  G[2,3](x <= e? 0;12 & x >= f? -12;0)  ) & G[3,4](x <= g? 0;12 & x >= h? -12;0) ) & G[4,5](x <= i? 0;12 & x >= j? -12;0) ) & G[5,6](x <= k? 0;12 & x >= l? -12;0) ) & G[6,7](x <= m? 0;12 & x >= n? -12;0) ) & G[7,8](x <= o? 0;12 & x >= p? -12;0) )',
#    '( ( ( ( ( ( ( (  G[0,1](x <= a? 0;12 & x >= b? -12;0)  &  G[1,2](x <= c? 0;12 & x >= d? -12;0) )  &  G[2,3](x <= e? 0;12 & x >= f? -12;0)  ) & G[3,4](x <= g? 0;12 & x >= h? -12;0) ) & G[4,5](x <= i? 0;12 & x >= j? -12;0) ) & G[5,6](x <= k? 0;12 & x >= l? -12;0) ) & G[6,7](x <= m? 0;12 & x >= n? -12;0) ) & G[7,8](x <= o? 0;12 & x >= p? -12;0) ) & G[8,9](x <= q? 0;12 & x >= r? -12;0) )',
#    '( ( ( ( ( ( ( ( (  G[0,1](x <= a? 0;12 & x >= b? -12;0)  &  G[1,2](x <= c? 0;12 & x >= d? -12;0) )  &  G[2,3](x <= e? 0;12 & x >= f? -12;0)  ) & G[3,4](x <= g? 0;12 & x >= h? -12;0) ) & G[4,5](x <= i? 0;12 & x >= j? -12;0) ) & G[5,6](x <= k? 0;12 & x >= l? -12;0) ) & G[6,7](x <= m? 0;12 & x >= n? -12;0) ) & G[7,8](x <= o? 0;12 & x >= p? -12;0) ) & G[8,9](x <= q? 0;12 & x >= r? -12;0) ) & G[9,10](x <= s? 0;12 & x >= t? -12;0) )',
#    '( ( ( ( ( ( ( ( ( (  G[0,1](x <= a? 0;12 & x >= b? -12;0)  &  G[1,2](x <= c? 0;12 & x >= d? -12;0) )  &  G[2,3](x <= e? 0;12 & x >= f? -12;0)  ) & G[3,4](x <= g? 0;12 & x >= h? -12;0) ) & G[4,5](x <= i? 0;12 & x >= j? -12;0) ) & G[5,6](x <= k? 0;12 & x >= l? -12;0) ) & G[6,7](x <= m? 0;12 & x >= n? -12;0) ) & G[7,8](x <= o? 0;12 & x >= p? -12;0) ) & G[8,9](x <= q? 0;12 & x >= r? -12;0) ) & G[9,10](x <= s? 0;12 & x >= t? -12;0) ) & G[10,11](x <= i? 0;12 & x >= j? -12;0) )',
#    '( ( ( ( ( ( ( ( ( ( (  G[0,1](x <= a? 0;12 & x >= b? -12;0)  &  G[1,2](x <= c? 0;12 & x >= d? -12;0) )  &  G[2,3](x <= e? 0;12 & x >= f? -12;0)  ) & G[3,4](x <= g? 0;12 & x >= h? -12;0) ) & G[4,5](x <= i? 0;12 & x >= j? -12;0) ) & G[5,6](x <= k? 0;12 & x >= l? -12;0) ) & G[6,7](x <= m? 0;12 & x >= n? -12;0) ) & G[7,8](x <= o? 0;12 & x >= p? -12;0) ) & G[8,9](x <= q? 0;12 & x >= r? -12;0) ) & G[9,10](x <= s? 0;12 & x >= t? -12;0) ) & G[10,11](x <= i? 0;12 & x >= j? -12;0) ) & G[11,12](x <= i? 0;12 & x >= j? -12;0) )',
]

#G[4,5](x <= i? 0;10 & x >= j? -10;0)

@pytest.mark.parametrize("tlStr", templogicdata)
def test_stl(tlStr):
    print(tlStr)
    (stlsyn, value, dur) = telex.synth.synthSTLParam(tlStr, "scale","L-BFGS-B")
    print(" Synthesized STL formula: {}\n Theta Optimal Value: {}\n Optimization time: {}\n".format(stlsyn, value, dur))
    (bres, qres) = telex.synth.verifySTL(stlsyn, "scale")
    print(" Test result of synthesized STL on each trace: {}\n Robustness Metric Value: {}\n".format(bres, qres))
    return value,dur


def main():
    runtime = {}
    rhovalues = []

    for templ in templogicdata:
        runtime[templ] = []

    for i in range(0,2):
        for templ in templogicdata:
            value, dur = test_stl(templ)
            runtime[templ].append(dur)
            rhovalues.append(value)


    print("======================================================================")
    template = "{0:5}|{1:10}|{2:25}|{3:25}" 
    print template.format("ID", " #Params", "     Mean Runtime", "     Variance in Runtime")
    print("----------------------------------------------------------------------")
    i = 1
    for templ in templogicdata:
        print(template.format(i, 2*i, numpy.mean(runtime[templ]), numpy.var(runtime[templ])))
        i = i+1
        print("----------------------------------------------------------------------")
    print("======================================================================")
    print("Mean Robustness Value: {}, Variance: {}".format(numpy.mean(rhovalues), numpy.var(rhovalues) ) )


if __name__ == "__main__":
    main()

