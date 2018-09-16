Quickstart
==========

dPay
-----
The dpay object is the connection to the dPay blockchain.
By creating this object different options can be set.

.. note:: All init methods of dpaygo classes can be given
          the ``dpay_instance=`` parameter to assure that
          all objects use the same dpay object. When the
          ``dpay_instance=`` parameter is not used, the
          dpay object is taken from get_shared_dpay_instance().

          ``get_shared_dpay_instance()`` returns a global instance of dpay.
          It can be set by ``set_shared_dpay_instance`` otherwise it is created
          on the first call.

.. code-block:: python

   from dpaygo import DPay
   from dpaygo.account import Account
   stm = DPay()
   account = Account("test", dpay_instance=stm)

.. code-block:: python

   from dpaygo import DPay
   from dpaygo.account import Account
   from dpaygo.instance import set_shared_dpay_instance
   stm = DPay()
   set_shared_dpay_instance(stm)
   account = Account("test")

Wallet and Keys
---------------
Each account has the following keys:

* Posting key (allows accounts to post, vote, edit, repost and follow/mute)
* Active key (allows accounts to transfer, power up/down, voting for witness, ...)
* Memo key (Can be used to encrypt/decrypt memos)
* Owner key (The most important key, should not be used with dPayGo)

Outgoing operation, which will be stored in the dPay blockchain, have to be
signed by a private key. E.g. Comment or Vote operation need to be signed by the posting key
of the author or upvoter. Private keys can be provided to dpaygo temporary or can be
stored encrypted in a sql-database (wallet).

.. note:: Before using the wallet the first time, it has to be created and a password has
          to set. The wallet content is available to dpay and all python scripts, which have
          access to the sql database file.

Creating a wallet
~~~~~~~~~~~~~~~~~
``dpay.wallet.wipe(True)`` is only necessary when there was already an wallet created.

.. code-block:: python

   from dpaygo import DPay
   dpay = DPay()
   dpay.wallet.wipe(True)
   dpay.wallet.unlock("wallet-passphrase")

Adding keys to the wallet
~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

   from dpaygo import DPay
   dpay = DPay()
   dpay.wallet.unlock("wallet-passphrase")
   dpay.wallet.addPrivateKey("xxxxxxx")
   dpay.wallet.addPrivateKey("xxxxxxx")

Using the keys in the wallet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from dpaygo import DPay
   dpay = DPay()
   dpay.wallet.unlock("wallet-passphrase")
   account = Account("test", dpay_instance=dpay)
   account.transfer("<to>", "<amount>", "<asset>", "<memo>")

Private keys can also set temporary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from dpaygo import DPay
   dpay = DPay(keys=["xxxxxxxxx"])
   account = Account("test", dpay_instance=dpay)
   account.transfer("<to>", "<amount>", "<asset>", "<memo>")

Receiving information about blocks, accounts, votes, comments, market and witness
---------------------------------------------------------------------------------

Receive all Blocks from the Blockchain

.. code-block:: python

   from dpaygo.blockchain import Blockchain
   blockchain = Blockchain()
   for op in blockchain.stream():
       print(op)

Access one Block

.. code-block:: python

   from dpaygo.block import Block
   print(Block(1))

Access an account

.. code-block:: python

   from dpaygo.account import Account
   account = Account("test")
   print(account.balances)
   for h in account.history():
       print(h)

A single vote

.. code-block:: python

   from dpaygo.vote import Vote
   vote = Vote(u"@gtg/ffdhu-gtg-witness-log|gandalf")
   print(vote.json())

All votes from an account

.. code-block:: python

   from dpaygo.vote import AccountVotes
   allVotes = AccountVotes("gtg")

Access a post

.. code-block:: python

   from dpaygo.comment import Comment
   comment = Comment("@gtg/ffdhu-gtg-witness-log")
   print(comment["active_votes"])

Access the market

.. code-block:: python

   from dpaygo.market import Market
   market = Market("BBD:BEX")
   print(market.ticker())

Access a witness

.. code-block:: python

   from dpaygo.witness import Witness
   witness = Witness("gtg")
   print(witness.is_active)

Sending transaction to the blockchain
-------------------------------------

Sending a Transfer

.. code-block:: python

   from dpaygo import DPay
   dpay = DPay()
   dpay.wallet.unlock("wallet-passphrase")
   account = Account("test", dpay_instance=dpay)
   account.transfer("null", 1, "BBD", "test")

Upvote a post

.. code-block:: python

   from dpaygo.comment import Comment
   from dpaygo import DPay
   dpay = DPay()
   dpay.wallet.unlock("wallet-passphrase")
   comment = Comment("@gtg/ffdhu-gtg-witness-log", dpay_instance=dpay)
   comment.upvote(weight=10, voter="test")

Publish a post to the blockchain

.. code-block:: python

   from dpaygo import DPay
   dpay = DPay()
   dpay.wallet.unlock("wallet-passphrase")
   dpay.post("title", "body", author="test", tags=["a", "b", "c", "d", "e"], self_vote=True)

Sell BEX on the market

.. code-block:: python

   from dpaygo.market import Market
   from dpaygo import DPay
   dpay.wallet.unlock("wallet-passphrase")
   market = Market("BBD:BEX", dpay_instance=dpay)
   print(market.ticker())
   market.dpay.wallet.unlock("wallet-passphrase")
   print(market.sell(300, 100))  # sell 100 BEX for 300 BEX/BBD
