import pytest
import telex.synth
import pandas

#templogicdata =  'G[0,6] F[b? 1;6,  a? 4;6](x1 > 2)'
templogicdata =  [
     'G[0, 220046461440] ( ((angle > 0.2) | (angle < -0.2)) -> (speed < a? 15;25) )',
    'G[0, 220046461440] ( ((angle > 0.2) | (angle < -0.2)) -> ( (speed < a? 15;25) & (speed > b? -25;-15) ) )',
]

@pytest.mark.parametrize("tlStr", templogicdata)
def test_stl(tlStr):
    print(tlStr)
    try:
        (stlsyn, value, dur) = telex.synth.synthSTLParam(tlStr, "udacityData")
    except ValueError:
        (stlsyn, value, dur) = telex.synth.synthSTLParam(tlStr, "udacityData", "nogradient")
    print(" Synthesized STL formula: {}\n Theta Optimal Value: {}\n Optimization time: {}\n".format(stlsyn, value, dur))
    (bres, qres) = telex.synth.verifySTL(stlsyn, "udacityData")
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

