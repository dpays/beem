from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import sys
from datetime import datetime, timedelta
import time
import io
import logging

from dpaygo.blockchain import Blockchain
from dpaygo.block import Block
from dpaygo.account import Account
from dpaygo.amount import Amount
from dpaygographenebase.account import PasswordKey, PrivateKey, PublicKey
from dpaygo.dpay import DPay
from dpaygo.utils import parse_time, formatTimedelta
from dpaygoapi.exceptions import NumRetriesReached
from dpaygo.nodelist import NodeList
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

password = "secretPassword"
username = "dpaygo"
useWallet = False

if __name__ == "__main__":
    nodelist = NodeList()
    stm = DPay(node=nodelist.get_nodes(normal=False, appbase=False, testnet=True))
    prefix = stm.prefix
    # curl --data "username=username&password=secretPassword" https://testnet.dpay.vc/create
    stm.wallet.wipe(True)
    if useWallet:
        stm.wallet.create("123")
        stm.wallet.unlock("123")
    active_key = PasswordKey(username, password, role="active", prefix=prefix)
    owner_key = PasswordKey(username, password, role="owner", prefix=prefix)
    posting_key = PasswordKey(username, password, role="posting", prefix=prefix)
    memo_key = PasswordKey(username, password, role="memo", prefix=prefix)
    active_pubkey = active_key.get_public_key()
    owner_pubkey = owner_key.get_public_key()
    posting_pubkey = posting_key.get_public_key()
    memo_pubkey = memo_key.get_public_key()
    active_privkey = active_key.get_private_key()
    posting_privkey = posting_key.get_private_key()
    owner_privkey = owner_key.get_private_key()
    memo_privkey = memo_key.get_private_key()
    if useWallet:
        stm.wallet.addPrivateKey(owner_privkey)
        stm.wallet.addPrivateKey(active_privkey)
        stm.wallet.addPrivateKey(memo_privkey)
        stm.wallet.addPrivateKey(posting_privkey)
    else:
        stm = DPay(node=nodelist.get_nodes(normal=False, appbase=False, testnet=True),
                    wif={'active': str(active_privkey),
                         'posting': str(posting_privkey),
                         'memo': str(memo_privkey)})
    account = Account(username, dpay_instance=stm)
    account.disallow("dpaygo1", permission='posting')
    account.allow('dpaygo1', weight=1, permission='posting', account=None)
    if useWallet:
        stm.wallet.getAccountFromPrivateKey(str(active_privkey))

    # stm.create_account("dpaygo1", creator=account, password=password1)

    account1 = Account("dpaygo1", dpay_instance=stm)
    b = Blockchain(dpay_instance=stm)
    blocknum = b.get_current_block().identifier

    account.transfer("dpaygo1", 1, "BBD", "test")
    b1 = Block(blocknum, dpay_instance=stm)
