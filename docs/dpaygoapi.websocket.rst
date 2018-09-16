dpaygoapi\.websocket
==================

This class allows subscribe to push notifications from the DPay
node.

.. code-block:: python

    from pprint import pprint
    from dpaygoapi.websocket import DPayWebsocket

    ws = DPayWebsocket(
        "wss://jefferson.dpays.io",
        accounts=["test"],
        on_block=print,
    )

    ws.run_forever()


.. autoclass:: dpaygoapi.websocket.DPayWebsocket
    :members:
    :undoc-members:
    :private-members:
    :special-members:
