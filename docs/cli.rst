dPay CLI
~~~~~~~~~~
`dpay` is a convenient CLI utility that enables you to manage your wallet, transfer funds, check
balances and more.

Using the Wallet
----------------
`dpay` lets you leverage your BIP38 encrypted wallet to perform various actions on your accounts.

The first time you use `dpay`, you will be prompted to enter a password. This password will be used to encrypt
the `dpay` wallet, which contains your private keys.

You can change the password via `changewalletpassphrase` command.

::

    dpay changewalletpassphrase


From this point on, every time an action requires your private keys, you will be prompted ot enter
this password (from CLI as well as while using `dPay` library).

To bypass password entry, you can set an environment variable ``UNLOCK``.

::

    UNLOCK=mysecretpassword dpay transfer <recipient_name> 100 BEX

Common Commands
---------------
First, you may like to import your dPay account:

::

    dpay importaccount


You can also import individual private keys:

::

   dpay addkey <private_key>

Listing accounts:

::

   dpay listaccounts

Show balances:

::

   dpay balance account_name1 account_name2

Sending funds:

::

   dpay transfer --account <account_name> <recipient_name> 100 BEX memo

Upvoting a post:

::

   dpay upvote --account <account_name> https://dsite.io/funny/@mynameisbrian/the-content-stand-a-comic


Setting Defaults
----------------
For a more convenient use of ``dpay`` as well as the ``dPayGo`` library, you can set some defaults.
This is especially useful if you have a single dPay account.

::

   dpay set default_account test
   dpay set default_vote_weight 100

   dpay config
    +---------------------+--------+
    | Key                 | Value  |
    +---------------------+--------+
    | default_account     | test   |
    | default_vote_weight | 100    |
    +---------------------+--------+

If you've set up your `default_account`, you can now send funds by omitting this field:

::

    dpay transfer <recipient_name> 100 BEX memo

Commands
--------

.. click:: dpaygo.cli:cli
    :prog: dpay
    :show-nested:

dpay --help
-------------
You can see all available commands with ``dpay --help``

::

    ~ % dpay --help
   Usage: cli.py [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

   Options:
     -n, --node TEXT        URL for public dPay API (e.g.
                            https://dpayapi.com)
     -o, --offline          Prevent connecting to network
     -d, --no-broadcast     Do not broadcast
     -p, --no-wallet        Do not load the wallet
     -x, --unsigned         Nothing will be signed
     -e, --expires INTEGER  Delay in seconds until transactions are supposed to
                            expire(defaults to 60)
     -v, --verbose INTEGER  Verbosity
     --version              Show the version and exit.
     --help                 Show this message and exit.

   Commands:
     addkey                  Add key to wallet When no [OPTION] is given,...
     allow                   Allow an account/key to interact with your...
     approvewitness          Approve a witnesses
     balance                 Shows balance
     broadcast               broadcast a signed transaction
     buy                     Buy BEX or BBD from the internal market...
     cancel                  Cancel order in the internal market
     changewalletpassphrase  Change wallet password
     claimreward             Claim reward balances By default, this will...
     config                  Shows local configuration
     convert                 Convert BEX Dollars to BEX (takes a week...
     createwallet            Create new wallet with a new password
     currentnode             Sets the currently working node at the first...
     delkey                  Delete key from the wallet PUB is the public...
     delprofile              Delete a variable in an account's profile
     disallow                Remove allowance an account/key to interact...
     disapprovewitness       Disapprove a witnesses
     downvote                Downvote a post/comment POST is...
     follow                  Follow another account
     follower                Get information about followers
     following               Get information about following
     importaccount           Import an account using a passphrase
     info                    Show basic blockchain info General...
     interest                Get information about interest payment
     listaccounts            Show stored accounts
     listkeys                Show stored keys
     mute                    Mute another account
     muter                   Get information about muter
     muting                  Get information about muting
     newaccount              Create a new account
     nextnode                Uses the next node in list
     openorders              Show open orders
     orderbook               Obtain orderbook of the internal market
     parsewif                Parse a WIF private key without importing
     permissions             Show permissions of an account
     pingnode                Returns the answer time in milliseconds
     power                   Shows vote power and bandwidth
     powerdown               Power down (start withdrawing VESTS from...
     powerdownroute          Setup a powerdown route
     powerup                 Power up (vest BEX as BEX POWER)
     pricehistory            Show price history
     repost                 Repost an existing post
     sell                    Sell BEX or BBD from the internal market...
     set                     Set default_account, default_vote_weight or...
     setprofile              Set a variable in an account's profile
     sign                    Sign a provided transaction with available...
     ticker                  Show ticker
     tradehistory            Show price history
     transfer                Transfer BBD/BEX
     unfollow                Unfollow/Unmute another account
     updatememokey           Update an account's memo key
     upvote                  Upvote a post/comment POST is...
     votes                   List outgoing/incoming account votes
     walletinfo              Show info about wallet
     witnesscreate           Create a witness
     witnesses               List witnesses
     witnessupdate           Change witness properties
