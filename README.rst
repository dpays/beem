dPayGo - Official Python Library for dPay
===============================================

dPayGo is an unofficial python library for dPay, which is created new from scratch from `python-bitshares`.


Support & Documentation
=======================
You may find help in the  `dpay-telegram-channel`_. The discord channel can also be used to discuss things about dpaygo.

A complete library documentation is available at  `libraries.dpays.io/dpaygo`_.

Advantages over the official dpay-python library
=================================================

* High unit test coverage
* Support for websocket nodes
* Native support for new Appbase calls
* Node error handling and automatic node switching
* Usage of pycryptodomex instead of the outdated pycrypto
* Complete documentation of dpay and all classes including all functions
* dpayid integration
* Works on read-only systems
* Own BlockchainObject class with cache
* Contains all broadcast operations
* Estimation of virtual account operation index from date or block number
* the command line tool dpay uses click and has more commands
* DPayNodeRPC can be used to execute even not implemented RPC-Calls
* More complete implemention

Installation
============
The minimal working python version is 2.7.x. or 3.4.x

dPayGo can be installed parallel to dpay-python.

For Debian and Ubuntu, please ensure that the following packages are installed:

.. code:: bash

    sudo apt-get install build-essential libssl-dev python-dev

For Fedora and RHEL-derivatives, please ensure that the following packages are installed:

.. code:: bash

    sudo yum install gcc openssl-devel python-devel

For OSX, please do the following::

    brew install openssl
    export CFLAGS="-I$(brew --prefix openssl)/include $CFLAGS"
    export LDFLAGS="-L$(brew --prefix openssl)/lib $LDFLAGS"

For Termux on Android, please install the following packages:

.. code:: bash

    pkg install clang openssl-dev python-dev

Signing and Verify can be fasten (200 %) by installing cryptography:

.. code:: bash

    pip install -U cryptography

Install dPayGo by pip::

    pip install -U dpaygo

You can install dPayGo from this repository if you want the latest
but possibly non-compiling version::

    git clone https://github.com/dpays/dpaygo.git
    cd dpaygo
    python setup.py build

    python setup.py install --user

Run tests after install::

    pytest


Installing dpaygo with conda-forge
--------------------------------

Installing dpaygo from the conda-forge channel can be achieved by adding conda-forge to your channels with::

    conda config --add channels conda-forge

Once the conda-forge channel has been enabled, dpaygo can be installed with::

    conda install dpaygo

Signing and Verify can be fasten (200 %) by installing cryptography::

    conda install cryptography


CLI tool dpay
---------------
A command line tool is available. The help output shows the available commands:

    dpay --help

Stand alone version of CLI tool dpay
--------------------------------------
With the help of pyinstaller, a stand alone version of dpay was created for Windows, OSX and linux.
Each version has just to be unpacked and can be used in any terminal. The packed directories
can be found under release. Each release has a hash sum, which is created directly in the build-server
before transmitting the packed file. Please check the hash-sum after downloading.

Changelog
=========
0.01.06
-------
* Added all new seed nodes for dPay's live network

0.01.05
-------
* Removed old nodes

0.01.04
-------
* Added dPay Node Running On Appbase (0.20.0) {Moved from Dev network} [d.dpays.io]
* Fixed "invalid reward fund" bug
* Cleaned up typos and typos in docs

0.01.03
-------
* Updated for the dPay network

License
=======
This library is licensed under the MIT License.

Acknowledgements
================
`python-bitshares`_ and `python-graphenelib`_ were created by Fabian Schuh (xeroc).

.. _python-graphenelib: https://github.com/xeroc/python-graphenelib
.. _python-bitshares: https://github.com/xeroc/python-bitshares
.. _Python: http://python.org
.. _Anaconda: https://www.continuum.io
.. _dpaygo.readthedocs.io: http://dpaygo.readthedocs.io/en/latest/
.. _dpaygo-discord-channel: https://discord.gg/4HM592V
