
# TeLEX
Temporal Logic Extractor


Installation Instructions 
1. Conda (Recommended)
2. Virtualbox 
3. Plain old simple method

-----------------------------------------
1. Conda
-----------------------------------------

1) Get hold of Conda: 
https://www.continuum.io/downloads#linux
http://conda.pydata.org/docs/install/full.html
> bash Anaconda-latest-Linux-x86_64.sh

2) Use the yml file in repository to setup environment for TeLEX
> conda env create -f telex.yml

This will create an environment named "telex" in your conda. Verify this by running: 
> conda env list

You should see a list of environments with "telex" in it; illustrative example:
>\# conda environments:
>\#
>telex                    /home/jha/anaconda2/envs/telex
>root                  *  /home/jha/anaconda2

3) If the "telex" environment is present in your environment, you can activate it by:
> source activate telex

4) Add TeLEX home to your PYTHONPATH environment variable; illustrative example:
>(telex) jha@sjlinux1:~/projects/TeLEX$ export PYTHONPATH=$PWD

>(telex) jha@sjlinux1:~/projects/TeLEX$ echo $PYTHONPATH
>/home/jha/projects/TeLEX

4) Go to tests folder and run "python test_learn.py" to check if all tests pass and TeLEX is installed.

-----------------------------------------
2. Virtualbox
-----------------------------------------


-----------------------------------------
3. Direct Installation Notes 
-----------------------------------------

1) Prerequisite: Python and python-dev packages (Can use apt-get install on Ubuntu).

2) Python packages: numpy, scipy, pandas, parsimonious, singledispatch(python 2)/functools(python 3) (Can use pip install for these).

3) Use setup.py for installation or add TeLEX home to PYTHONPATH.

4) Run test scripts in tests to verify installation and modify these scripts as needed.

Troubleshooting: 
------------------

a) complain about six module :
sudo pip  install --upgrade six (six version might need upgrade, parsimonious depends on six)

b) linblopt import issue :
installation of bayesopt puts libnlopt.so in /usr/local/lib (or similar relative path if using prefix). You might have to do sudo ldconfig to rehash libraries.
Optional: Install BayesOpt tool with Python API wrapper

To fix:
--------

a) code assumes deterministic enumeration over lists in communicating with optimizer; this is probably not the case in python 3 or is likely to be removed soon for security issues. 
