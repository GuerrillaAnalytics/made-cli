# made
A command line tool for analysing data efficiently

# Configuration
This code was developed using the Anaconda distribution of Python. This seemed to confuse tox and virtualenv. The resolution is:

* make sure Python 2.7.9 is available by running `conda install python=2.7.9`
* install pip with `easy_install pip`
* install tox with `easy_install tox`
* install pipsi with `easy_install pipsi`

# Installation
Force installation into Python3 environment (in case you have Python2 as default environment).
* `pipsi install -e . --python python3`

# Removal
* `pipsi uninstall made`
