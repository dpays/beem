# This Python file uses the following encoding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
import json
import io
import collections
import hashlib
from binascii import hexlify, unhexlify
import requests
from .instance import shared_dpay_instance
from dpaygo.account import Account
from dpaygographenebase.py23 import integer_types, string_types, text_type, py23_bytes
from dpaygographenebase.account import PrivateKey
from dpaygographenebase.ecdsasig import sign_message, verify_message


class ImageUploader(object):
    def __init__(
        self,
        base_url="https://dsiteimages.com",
        challenge="ImageSigningChallenge",
        dpay_instance=None,
    ):
        self.challenge = challenge
        self.base_url = base_url
        self.dpay = dpay_instance or shared_dpay_instance()

    def upload(self, image, account, image_name=None):
        """ Uploads an image

            :param str/bytes image: path to the image or image in bytes representation which should be uploaded
            :param str account: Account which is used to upload. A posting key must be provided.
            :param str image_name: optional

            .. code-block:: python

                from dpaygo import DPay
                from dpaygo.imageuploader import ImageUploader
                stm = DPay(keys=["5xxx"]) # private posting key
                iu = ImageUploader(dpay_instance=stm)
                iu.upload("path/to/image.png", "account_name") # "private posting key belongs to account_name

        """
        account = Account(account, dpay_instance=self.dpay)
        if "posting" not in account:
            account.refresh()
        if "posting" not in account:
            raise AssertionError("Could not access posting permission")
        for authority in account["posting"]["key_auths"]:
            posting_wif = self.dpay.wallet.getPrivateKeyForPublicKey(authority[0])

        if isinstance(image, string_types):
            image_data = open(image, 'rb').read()
        elif isinstance(image, io.BytesIO):
            image_data = image.read()
        else:
            image_data = image

        message = py23_bytes(self.challenge, "ascii") + image_data
        signature = sign_message(message, posting_wif)
        signature_in_hex = hexlify(signature).decode("ascii")

        files = {image_name or 'image': image_data}
        url = "%s/%s/%s" % (
            self.base_url,
            account["name"],
            signature_in_hex
        )
        r = requests.post(url, files=files)
        return r.json()
