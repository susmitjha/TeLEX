import pytest
import telex.synth
import telex.scorer
import pandas

import telex.inputreader as inputreader


#templogicdata =  'G[0,6] F[b? 1;6,  a? 4;6](x1 > 2)'
templogicdata =  [
#   'G[0, 220046461440] ( ((angle > 0.2) | (angle < -0.2)) -> (speed < a? 15;25) )',
#   'G[0, 220046461440] ( ((torque > 1.6) | (torque < -1.6)) -> (speed < a? 15;25) )',
#    'G[0, 220046461440] ( (angle > -0.06)  ->  (torque > b? -2;-0.5)  )',
#    'G[0, 220046461440] ( (angle < 0.06)  ->  (torque < b? 0.5;2)  )',
#     'G[0, 2200464614] ( (torque < 0)  ->  F[0, 220000000](angle < a? -1;2)  )',
#    'G[1,999] ( (e6 <= 0)  |  (G[0, 5] (e6 >= 1))  )',
#    'G[1,999] ( ( ( ( ( ( ( ( te1 <= a? 0;100) & (te2 <= a? 0;100) ) & (te3 <= a? 0;100) ) & (te4 <= a? 0;100) ) & (te5 <= a? 0;100) ) & (te6 <= a? 0;100) ) & (te7 <= a? 0;100) ) & (te8 <= a? 0;100) )',
    'G[1,999] (y1 > a? -1;50)'
]

@pytest.mark.parametrize("tlStr", templogicdata)
def test_stl(tlStr):
    print(tlStr)

    #x = inputreader.readtracefile("surv/trace1.csv")
    #stl1 = telex.stl.parse(tlStr)
    #sc = telex.scorer.smartscore(stl1, x, 0)
    #print(sc)

    #exit()

    try:
        (stlsyn, value, dur) = telex.synth.synthSTLParam(tlStr, "surv")
    except ValueError:
        print('Error: Check bounds')
        (stlsyn, value, dur) = telex.synth.synthSTLParam(tlStr, "surv", "nogradient")
    print(" Synthesized STL formula: {}\n Theta Optimal Value: {}\n Optimization time: {}\n".format(stlsyn, value, dur))
    (bres, qres) = telex.synth.verifySTL(stlsyn, "surv")
    print(" Test result of synthesized STL on each trace: {}\n Robustness Metric Value: {}\n".format(bres, qres))
#    print(tlStr)
#    (stlsyn, value, dur) = telex.synth.synthSTLParam(tlStr, "traces")
#    print(stlsyn, value, dur)
#    (bres, qres) = telex.synth.verifySTL(stlsyn, "traces")
#    print(bres, qres)


def main():
    for templ in templogicdata:
        test_stl(templ)

if __name__ == "__main__":
    main()


'''
(telex) jha@sjlinux1:~/projects/TeLEX/tests$ python test_surv.py 
G[1,999] ( ( ( ( ( ( ( ( te1 <= a? 0;100) & (te2 <= a? 0;100) ) & (te3 <= a? 0;100) ) & (te4 <= a? 0;100) ) & (te5 <= a? 0;100) ) & (te6 <= a? 0;100) ) & (te7 <= a? 0;100) ) & (te8 <= a? 0;100) )
 Synthesized STL formula: G[1.0,999.0]((((((((te1 <= 39.0014648438) & (te2 <= 39.0014648438)) & (te3 <= 39.0014648438)) & (te4 <= 39.0014648438)) & (te5 <= 39.0014648438)) & (te6 <= 39.0014648438)) & (te7 <= 39.0014648438)) & (te8 <= 39.0014648438))
 Theta Optimal Value: 0.0199990829179
 Optimization time: 0.442027

 Test result of synthesized STL on each trace: [True]
 Robustness Metric Value: [0.00146484375]


===============

(telex) jha@sjlinux1:~/projects/TeLEX/tests$ python test_surv.py 
G[1,99] ( (e6 >= 1)  ->  (F[0, 20] (e6 <= 0))  )
-0.0
(telex) jha@sjlinux1:~/projects/TeLEX/tests$ python test_surv.py 
G[1,99] ( (e6 >= 1)  &  (G[0, 20] (e6 >= 1))  )
-3.44099815531


'''
