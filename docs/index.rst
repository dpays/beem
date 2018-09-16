.. dpay-python documentation master file, created by
   sphinx-quickstart on Fri Jun  5 14:06:38 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. http://sphinx-doc.org/rest.html
   http://sphinx-doc.org/markup/index.html
   http://sphinx-doc.org/markup/para.html
   http://openalea.gforge.inria.fr/doc/openalea/doc/_build/html/source/sphinx/rest_syntax.html
   http://rest-sphinx-memo.readthedocs.org/en/latest/ReST.html

.. image:: _static/dpaygo-logo.svg
   :width: 300 px
   :alt: dpaygo
   :align: center

Welcome to dPayGo's documentation!
================================

dPay is a blockchain-based rewards platform for publishers to monetize
content and grow community.

It is based on *Graphene* (tm), a blockchain technology stack (i.e.
software) that allows for fast transactions and ascalable blockchain
solution. In case of DPay, it comes with decentralized publishing of
content.

The dPayGo library has been designed to allow developers to easily
access its routines and make use of the network without dealing with all
the related blockchain technology and cryptography. This library can be
used to do anything that is allowed according to the dPay
blockchain protocol.


About this Library
------------------

The purpose of *dPayGo* is to simplify development of products and
services that use the dPay blockchain. It comes with

* it's own (bip32-encrypted) wallet
* RPC interface for the Blockchain backend
* JSON-based blockchain objects (accounts, blocks, prices, markets, etc)
* a simple to use yet powerful API
* transaction construction and signing
* push notification API
* *and more*

Quickstart
----------

.. note:: All methods that construct and sign a transaction can be given
          the ``account=`` parameter to identify the user that is going
          to affected by this transaction, e.g.:

          * the source account in a transfer
          * the accout that buys/sells an asset in the exchange
          * the account whos collateral will be modified

         **Important**, If no ``account`` is given, then the
         ``default_account`` according to the settings in ``config`` is
         used instead.

.. code-block:: python

   from dpaygo import DPay
   dpay = DPay()
   dpay.wallet.unlock("wallet-passphrase")
   account = Account("test", dpay_instance=dpay)
   account.transfer("<to>", "<amount>", "<asset>", "<memo>")

.. code-block:: python

   from dpaygo.blockchain import Blockchain
   blockchain = Blockchain()
   for op in blockchain.stream():
       print(op)

.. code-block:: python

   from dpaygo.block import Block
   print(Block(1))

.. code-block:: python

   from dpaygo.account import Account
   account = Account("test")
   print(account.balances)
   for h in account.history():
       print(h)

.. code-block:: python

   from dpaygo.dpay import DPay
   stm = DPay()
   stm.wallet.wipe(True)
   stm.wallet.create("wallet-passphrase")
   stm.wallet.unlock("wallet-passphrase")
   stm.wallet.addPrivateKey("512345678")
   stm.wallet.lock()

.. code-block:: python

   from dpaygo.market import Market
   market = Market("BBD:BEX")
   print(market.ticker())
   market.dpay.wallet.unlock("wallet-passphrase")
   print(market.sell(300, 100)  # sell 100 BEX for 300 BEX/BBD


General
-------
.. toctree::
   :maxdepth: 1

   installation
   quickstart
   tutorials
   cli
   configuration
   apidefinitions
   modules
   contribute
   support
   indices



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
