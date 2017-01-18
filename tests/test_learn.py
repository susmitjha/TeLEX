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
]

@pytest.mark.parametrize("tlStr", templogicdata)
def test_stl(tlStr):
    print(tlStr)
    (stlsyn, value, dur) = telex.synth.synthSTLParam(tlStr, "traces")
    print(stlsyn, value, dur)
    (bres, qres) = telex.synth.verifySTL(stlsyn, "traces")
    print(bres, qres)


def main():
    for templ in templogicdata:
        test_stl(templ)

if __name__ == "__main__":
    main()

