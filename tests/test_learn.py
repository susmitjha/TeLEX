import pytest
import telex.synth
import pandas

#templogicdata =  'G[0,6] F[b? 1;6,  a? 4;6](x1 > 2)'
templogicdata =  [
    'G[b? 1;6,  a? 1;9](x1 > 2)',
    'G[0,5] F[a? 0;3, b? 0;5] (x1 > 2)',
    'G[0,5] F[1, b? 0;5] (x1 > 2)',
    'G[0,5] F[a? 0;2 , 2] (x1 > 2)',
    'G[0,5] F[a? 1;2 , 3] (x1 > 2)',
    'G[0,9] ({ x1 - x2 } < a? -2;8 )',
    'G[0,9] ({ x2 - x1 } < a? -2;8 )',
    'U[0,a? 0;2] (x1 <= 10, x2<=5)',
    'U[0,2] (x1 > b? 0;5, x2 > 1)',
]

@pytest.mark.parametrize("tlStr", templogicdata)
def test_stl(tlStr):
    print(tlStr)
    try:
        (stlsyn, value, dur) = telex.synth.synthSTLParam(tlStr, "traces")
    except ValueError:
        (stlsyn, value, dur) = telex.synth.synthSTLParam(tlStr, "traces", "nogradient")
    print(" Synthesized STL formula: {}\n Theta Optimal Value: {}\n Optimization time: {}\n".format(stlsyn, value, dur))
    (bres, qres) = telex.synth.verifySTL(stlsyn, "traces")
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

