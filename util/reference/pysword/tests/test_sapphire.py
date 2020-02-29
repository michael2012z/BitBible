# -*- coding: utf-8 -*-
###############################################################################
# PySword - A native Python reader of the SWORD Project Bible Modules         #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2019 Various PySword developers:                         #
# Kenneth Arnold, Joshua Gross, Tomas Groth, Ryan Hiebert, Philip Ridout,     #
# Matthew Wardrop                                                             #
# --------------------------------------------------------------------------- #
# Permission is hereby granted, free of charge, to any person obtaining a     #
# copy of this software and associated documentation files (the "Software"),  #
# to deal in the Software without restriction, including without limitation   #
# the rights to use, copy, modify, merge, publish, distribute, sublicense,    #
# and/or sell copies of the Software, and to permit persons to whom the       #
# Software is furnished to do so, subject to the following conditions:        #
#                                                                             #
# The above copyright notice and this permission notice shall be included     #
# in all copies or substantial portions of the Software.                      #
#                                                                             #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER      #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING     #
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER         #
# DEALINGS IN THE SOFTWARE.                                                   #
###############################################################################

import os
import sys

from tests import TestCase

from pysword.sapphire import Sapphire


class TestSapphire(TestCase):

    def test_sapphire_encrypt_and_decrypt(self):
        """
        Test that sapphire can encrypt and decrypt
        """
        # GIVEN: A cipherkey, a text and the Sapphire stream class
        cipherkey = 'qwerty'
        text = 'pysword'
        sap = Sapphire(cipherkey)

        # WHEN: Encrypting the text
        encrypted = []
        for b in bytearray(text, 'utf-8'):
            encrypted.append(sap.encrypt(b))

        # THEN: The output should be encrypted as expected
        assert encrypted == [95, 56, 27, 126, 46, 13, 112]

        # GIVEN: A reset Sapphire stream class
        sap.reset()

        # WHEN: Decrypting the encrypted data
        decrypted = []
        for b in bytearray(encrypted):
            decrypted.append(sap.decrypt(b))
        decrypted_data = bytes(bytearray(decrypted))

        # THEN: Then decrypted data should match the original data
        assert decrypted_data.decode() == text
