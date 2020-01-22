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

from tests import TestCase, patch

from pysword.modules import SwordModules
from pysword.bible import BlockType, CompressType

TEST_RESOURCE_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), u'resources')


class TestSwordModules(TestCase):
    def test_parse_modules_folder(self):
        """
        Test that conf file from a folder can be parsed.
        """
        # GIVEN: A SwordModules object using a folder for input
        modules = SwordModules(TEST_RESOURCE_FOLDER)

        # WHEN: parsing the modules conf files
        mods_metadata = modules.parse_modules()

        # THEN: Modules should be detectable and information extractable
        module_list = [u'ChiPinyin', u'FinPR', u'BSV', u'ASV', u'AraNAV', u'SpaRV1909']
        self.assertTrue(all(x in module_list for x in mods_metadata.keys()),
                        u'Some expected bibles were not detected')
        # Depending on the operating system, the handling of non-utf8 encoded conf-files is different
        self.assertEqual(mods_metadata[u'FinPR'][u'description'], u'Finnish Pyhä Raamattu (1933/1938)',
                         u'Could not extract "description" for "FinPR"')
        self.assertEqual(mods_metadata[u'BSV'][u'description'], u'The Bond Slave Version Bible',
                         u'Could not extract "description" for "BSV"')
        self.assertEqual(mods_metadata[u'ASV'][u'description'], u'American Standard Version (1901)',
                         u'Could not extract "description" for "ASV"')
        self.assertEqual(mods_metadata[u'AraNAV'][u'description'], u'New Arabic Version (Ketab El Hayat)',
                         u'Could not extract "description" for "AraNAV"')

    def test_parse_modules_zip(self):
        """
        Test that conf file from a zip can be parsed.
        """
        # GIVEN: A SwordModules object using a folder for input
        modules = SwordModules(os.path.join(TEST_RESOURCE_FOLDER, u'FinPR.zip'))

        # WHEN: parsing the modules conf files
        mods_metadata = modules.parse_modules()

        # THEN: Modules should be detectable and information extractable
        self.assertEqual(1, len(mods_metadata.keys()), u'There should be only 1  module in a zip.')
        self.assertIn(u'FinPR', mods_metadata.keys(), u'FinPR should be available')
        self.assertEqual(mods_metadata['FinPR']['description'], u'Finnish Pyhä Raamattu (1933/1938)',
                         u'Could not extract "description" for "FinPR"')

    @patch(u'pysword.modules.SwordBible')
    def test_get_bible_from_module(self, mocked_sword_bible):
        """
        Test that the assigning of default values works.
        """
        # GIVEN: A SwordModules object
        modules = SwordModules(u'test_sword_path')
        modules._modules = {u'test_key': {u'datapath': u'test_path', u'moddrv': u'test_mod_type'}}

        # WHEN: Requesting a bible from a module
        bible = modules.get_bible_from_module(u'test_key')

        # THEN: It should succeed
        # Check that the returned mock bible has created with default values
        self.assertIsNotNone(bible, u'Returned bible should not be None')
        mocked_sword_bible.assert_called_with(os.path.join(u'test_sword_path', u'test_path'),
                                              u'test_mod_type', u'kjv', None, None, BlockType.BOOK, CompressType.ZIP,
                                              None)
