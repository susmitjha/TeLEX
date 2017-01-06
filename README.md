# TeLEX
Temporal Logic Extractor


Installation Instructions
--------------------------

1) Prerequisite: Python and python-dev packages (Can use apt-get install on Ubuntu).

2) Python packages: numpy, pandas, parsimonious, singledispatch(python 2)/functools(python 3) (Can use pip install for these).

3) Install BayesOpt tool with Python API wrapper ( http://rmcantin.bitbucket.org/html/install.html )
- git clone https://github.com/rmcantin/bayesopt
- sudo apt-get install libboost-dev cmake cmake-curses-gui g++
- sudo apt-get install python-dev python-numpy
- cmake -DBAYESOPT_PYTHON_INTERFACE=ON .
- make
- sudo make install 

4) Use setup.py for installation or add TeLEX home to PYTHONPATH.

5) Run test scripts in tests to verify installation and modify these scripts as needed.

Troubleshooting: 
a) complain about six module :
sudo pip  install --upgrade six (six version might need upgrade, parsimonious depends on six)
b) linblopt import issue :
installation of bayesopt puts libnlopt.so in /usr/local/lib (or similar relative path if using prefix). You might have to do sudo ldconfig to rehash libraries.

