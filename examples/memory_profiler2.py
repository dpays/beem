from __future__ import print_function
from memory_profiler import profile
import sys
from dpaygo.dpay import DPay
from dpaygo.account import Account
from dpaygo.blockchain import Blockchain
from dpaygo.instance import set_shared_dpay_instance, clear_cache
from dpaygo.storage import configStorage as config
from dpaygoapi.graphenerpc import GrapheneRPC
import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@profile
def profiling(node, name_list, shared_instance=True, clear_acc_cache=False, clear_all_cache=True):
    print("shared_instance %d clear_acc_cache %d clear_all_cache %d" %
          (shared_instance, clear_acc_cache, clear_all_cache))
    if not shared_instance:
        stm = DPay(node=node)
        print(str(stm))
    else:
        stm = None
    acc_dict = {}
    for name in name_list:
        acc = Account(name, dpay_instance=stm)
        acc_dict[name] = acc
        if clear_acc_cache:
            acc.clear_cache()
        acc_dict = {}
    if clear_all_cache:
        clear_cache()
    if not shared_instance:
        del stm.rpc


if __name__ == "__main__":
    stm = DPay()
    print("Shared instance: " + str(stm))
    set_shared_dpay_instance(stm)
    b = Blockchain()
    account_list = []
    for a in b.get_all_accounts(limit=500):
        account_list.append(a)
    shared_instance = False
    clear_acc_cache = False
    clear_all_cache = False
    node = "wss://dpayd.dpays.io"
    n = 3
    for i in range(1, n + 1):
        print("%d of %d" % (i, n))
        profiling(node, account_list, shared_instance=shared_instance, clear_acc_cache=clear_acc_cache, clear_all_cache=clear_all_cache)
