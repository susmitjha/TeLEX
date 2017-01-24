

import pytest
import telex.synth
import pandas
import numpy
import sys, getopt


#templogicdata =  'G[0,6] F[b? 1;6,  a? 4;6](x1 > 2)'
templogicdata =  [
    'G[0,1](x <= a? 0;12 & x >= b? -12;0 )',
    '(  G[0,1](x <= a? 0;12 & x >= b? -12;0 )  &  G[1,2](x <= c? 0;12 & x >= d? -12;0 ) )',
    '( (  G[0,1](x <= a? 0;12 & x >= b? -12;0 )  &  G[1,2](x <= c? 0;12 & x >= d? -12;0 ) )  &  G[2,3](x <= e? 0;12 & x >= f? -12;0 )  ) ',
    '( ( (  G[0,1](x <= a? 0;12 & x >= b? -12;0)  &  G[1,2](x <= c? 0;12 & x >= d? -12;0) )  &  G[2,3](x <= e? 0;12 & x >= f? -12;0)  ) & G[3,4](x <= g? 0;12 & x >= h? -12;0) )',
    '( ( ( (  G[0,1](x <= a? 0;12 & x >= b? -12;0)  &  G[1,2](x <= c? 0;12 & x >= d? -12;0) )  &  G[2,3](x <= e? 0;12 & x >= f? -12;0)  ) & G[3,4](x <= g? 0;12 & x >= h? -12;0) ) & G[4,5](x <= i? 0;12 & x >= j? -12;0) )',
    '( ( ( ( (  G[0,1](x <= a? 0;12 & x >= b? -12;0)  &  G[1,2](x <= c? 0;12 & x >= d? -12;0) )  &  G[2,3](x <= e? 0;12 & x >= f? -12;0)  ) & G[3,4](x <= g? 0;12 & x >= h? -12;0) ) & G[4,5](x <= i? 0;12 & x >= j? -12;0) ) & G[5,6](x <= k? 0;12 & x >= l? -12;0) )',
    '( ( ( ( ( (  G[0,1](x <= a? 0;12 & x >= b? -12;0)  &  G[1,2](x <= c? 0;12 & x >= d? -12;0) )  &  G[2,3](x <= e? 0;12 & x >= f? -12;0)  ) & G[3,4](x <= g? 0;12 & x >= h? -12;0) ) & G[4,5](x <= i? 0;12 & x >= j? -12;0) ) & G[5,6](x <= k? 0;12 & x >= l? -12;0) ) & G[6,7](x <= m? 0;12 & x >= n? -12;0) )',
    '( ( ( ( ( ( (  G[0,1](x <= a? 0;12 & x >= b? -12;0)  &  G[1,2](x <= c? 0;12 & x >= d? -12;0) )  &  G[2,3](x <= e? 0;12 & x >= f? -12;0)  ) & G[3,4](x <= g? 0;12 & x >= h? -12;0) ) & G[4,5](x <= i? 0;12 & x >= j? -12;0) ) & G[5,6](x <= k? 0;12 & x >= l? -12;0) ) & G[6,7](x <= m? 0;12 & x >= n? -12;0) ) & G[7,8](x <= o? 0;12 & x >= p? -12;0) )',
    '( ( ( ( ( ( ( (  G[0,1](x <= a? 0;12 & x >= b? -12;0)  &  G[1,2](x <= c? 0;12 & x >= d? -12;0) )  &  G[2,3](x <= e? 0;12 & x >= f? -12;0)  ) & G[3,4](x <= g? 0;12 & x >= h? -12;0) ) & G[4,5](x <= i? 0;12 & x >= j? -12;0) ) & G[5,6](x <= k? 0;12 & x >= l? -12;0) ) & G[6,7](x <= m? 0;12 & x >= n? -12;0) ) & G[7,8](x <= o? 0;12 & x >= p? -12;0) ) & G[8,9](x <= q? 0;12 & x >= r? -12;0) )',
    '( ( ( ( ( ( ( ( (  G[0,1](x <= a? 0;12 & x >= b? -12;0)  &  G[1,2](x <= c? 0;12 & x >= d? -12;0) )  &  G[2,3](x <= e? 0;12 & x >= f? -12;0)  ) & G[3,4](x <= g? 0;12 & x >= h? -12;0) ) & G[4,5](x <= i? 0;12 & x >= j? -12;0) ) & G[5,6](x <= k? 0;12 & x >= l? -12;0) ) & G[6,7](x <= m? 0;12 & x >= n? -12;0) ) & G[7,8](x <= o? 0;12 & x >= p? -12;0) ) & G[8,9](x <= q? 0;12 & x >= r? -12;0) ) & G[9,10](x <= s? 0;12 & x >= t? -12;0) )',
    '( ( ( ( ( ( ( ( ( (  G[0,1](x <= a? 0;12 & x >= b? -12;0)  &  G[1,2](x <= c? 0;12 & x >= d? -12;0) )  &  G[2,3](x <= e? 0;12 & x >= f? -12;0)  ) & G[3,4](x <= g? 0;12 & x >= h? -12;0) ) & G[4,5](x <= i? 0;12 & x >= j? -12;0) ) & G[5,6](x <= k? 0;12 & x >= l? -12;0) ) & G[6,7](x <= m? 0;12 & x >= n? -12;0) ) & G[7,8](x <= o? 0;12 & x >= p? -12;0) ) & G[8,9](x <= q? 0;12 & x >= r? -12;0) ) & G[9,10](x <= s? 0;12 & x >= t? -12;0) ) & G[10,11](x <= u? 0;12 & x >= v? -12;0) )',
    '( ( ( ( ( ( ( ( ( ( (  G[0,1](x <= a? 0;12 & x >= b? -12;0)  &  G[1,2](x <= c? 0;12 & x >= d? -12;0) )  &  G[2,3](x <= e? 0;12 & x >= f? -12;0)  ) & G[3,4](x <= g? 0;12 & x >= h? -12;0) ) & G[4,5](x <= i? 0;12 & x >= j? -12;0) ) & G[5,6](x <= k? 0;12 & x >= l? -12;0) ) & G[6,7](x <= m? 0;12 & x >= n? -12;0) ) & G[7,8](x <= o? 0;12 & x >= p? -12;0) ) & G[8,9](x <= q? 0;12 & x >= r? -12;0) ) & G[9,10](x <= s? 0;12 & x >= t? -12;0) ) & G[10,11](x <= u? 0;12 & x >= v? -12;0) ) & G[11,12](x <= w? 0;12 & x >= y? -12;0) )',
]

#G[4,5](x <= i? 0;10 & x >= j? -10;0)

@pytest.mark.parametrize("tlStr", templogicdata)
def test_stl(tlStr, optmethod = "gradient"):
    print(tlStr)
    (stlsyn, value, dur) = telex.synth.synthSTLParam(tlStr, "scale", optmethod)
    print(" Synthesized STL formula: {}\n Theta Optimal Value: {}\n Optimization time: {}\n".format(stlsyn, value, dur))
    (bres, qres) = telex.synth.verifySTL(stlsyn, "scale")
    print(" Test result of synthesized STL on each trace: {}\n Robustness Metric Value: {}\n".format(bres, qres))
    return stlsyn,value,dur
 

def main(argv):
    itercount = 2
    optmethod = "gradient"
    
    
    try: 
        opts,args = getopt.getopt(argv, "hi:o:",["itercount=","optmethod="])
    except getopt.GetoptError:
        print 'python test_scale.py -i <number of times to iterate each synthesis task to compute mean runtime> -o <opt-method>' 
        sys.exit(2)
    for opt,arg in opts:
        if opt == '-h':
            print 'python test_scale.py -i <number of times to iterate each synthesis task to compute mean runtime> -o <opt-method>'
            print 'Valid opt-methods: \"gradient\", \"nogradient\"'
            sys.exit()
        elif opt in ("-i", "--itercount"):
            itercount = int(arg)
        elif opt in ("-o", "--optmethod"):
            optmethod = arg

    logfile = "scale_" + optmethod + "_" + str(itercount) + ".log"
    print("Writing to logfile: {}".format(logfile))


    runtime = {}
    rhovalues = {}
    doneflag = {}

    for templ in templogicdata:
        runtime[templ] = []
        rhovalues[templ] = []
        doneflag[templ] = False

    for templ in templogicdata:
        for i in range(0,itercount):
            stlsyn, value, dur = test_stl(templ, optmethod)
            runtime[templ].append(dur)
            rhovalues[templ].append(value)
            f1=open(logfile, 'a')
            f1.write("Finished {} (Iter: {}) in {} seconds with value {} and result {}\n".format(templ, i, dur , value, stlsyn))
            f1.close()
            f1=open(logfile, 'a')
        doneflag[templ] = True
        f1.write("========================SO-FAR========================================\n")
        f1.write("               Optmethod {}\n".format(optmethod))
        f1.write("======================================================================\n")
        f1.write("                Averaging over {} Iterations\n".format(itercount))
        f1.write("======================================================================\n")
        template = "{0:5}|{1:10}|{2:25}|{3:25}|{4:20}|{5:20}\n" 
        f1.write(template.format("ID", " #Params", "     Mean Runtime", "     Variance in Runtime", "  Rho Mean ", " Rho Var ") )
        j = 1
        for templ1 in filter(lambda x: doneflag[x], templogicdata):
            f1.write("----------------------------------------------------------------------\n")
            f1.write(template.format(j, 2*j, numpy.mean(runtime[templ1]), numpy.var(runtime[templ1]), numpy.mean(rhovalues[templ1]), numpy.var(rhovalues[templ1]) ))
            j = j+1
        f1.write("======================================================================\n")
        f1.close()


    f1=open(logfile, 'a')
    f1.write("========================FINAL=========================================\n")
    f1.write("               Optmethod {}\n".format(optmethod))
    f1.write("======================================================================\n")
    f1.write("                Averaging over {} Iterations\n".format(itercount))
    f1.write("======================================================================\n")
    template = "{0:5}|{1:10}|{2:25}|{3:25}|{4:20}|{5:20}\n" 
    f1.write(template.format("ID", " #Params", "     Mean Runtime", "     Variance in Runtime", "  Rho Mean ", " Rho Var ") )
    i = 1
    for templ in templogicdata:
        f1.write("----------------------------------------------------------------------\n")
        f1.write(template.format(i, 2*i, numpy.mean(runtime[templ]), numpy.var(runtime[templ]), numpy.mean(rhovalues[templ]), numpy.var(rhovalues[templ]) ))
        i = i+1
    f1.write("======================================================================\n")
    f1.close()

    #print("Mean Robustness Value: {}, Variance: {}".format(numpy.mean(rhovalues), numpy.var(rhovalues) ) )


if __name__ == "__main__":
    main(sys.argv[1:])

