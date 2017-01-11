
# TeLEX
Temporal Logic Extractor


Recommended Installation Instructions
--------------------------------------

1) Get hold of Conda: 
https://www.continuum.io/downloads#linux
http://conda.pydata.org/docs/install/full.html
> bash Anaconda-latest-Linux-x86_64.sh

2) Use the yml file in repository to setup environment for TeLEX
> conda env create -f telex.yml

3) Add TeLEX home to PYTHONPATH

4) Go to tests folder and run "python test_learn.py" to check if all tests pass and TeLEX is installed.


Direct Installation Notes Without Conda
----------------------------------------

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
