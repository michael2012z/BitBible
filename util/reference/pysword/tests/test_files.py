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

from tests.test_utils import TestCase

from pysword.modules import SwordModules

TEST_RESOURCE_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), u'resources')


class TestModules(TestCase):

    def test_load_finpr_zip(self):
        """
        Test that the FinPR.zip file is loaded correctly.
        """
        # GIVEN: The FinPR.zip file
        modules = SwordModules(os.path.join(TEST_RESOURCE_FOLDER, u'FinPR.zip'))

        # WHEN: Parsing the FinPR module and reading a passage.
        found_modules = modules.parse_modules()
        bible = modules.get_bible_from_module(u'FinPR')
        output = bible.get(books=[u'john'], chapters=[3], verses=[16])

        # THEN: The FinPR module should be the only one found. And the passage should be equal to the known text.
        assert u'FinPR' in found_modules
        assert len(found_modules) == 1
        assert output == u'Sillä niin on Jumala maailmaa rakastanut, että hän antoi ainokaisen Poikansa, ' \
                         u'ettei yksikään, joka häneen uskoo, hukkuisi, vaan hänellä olisi iankaikkinen elämä.'

    def test_load_chipinyin_zip(self):
        """
        Test that the chipinyin.zip file is loaded correctly.
        """
        # GIVEN: The chipinyin.zip file
        modules = SwordModules(os.path.join(TEST_RESOURCE_FOLDER, u'chipinyin.zip'))

        # WHEN: Parsing the chipinyin module and reading a passage.
        found_modules = modules.parse_modules()
        bible = modules.get_bible_from_module(u'ChiPinyin')
        output = bible.get(books=[u'john'], chapters=[3], verses=[16])

        # THEN: The ChiPinyin module should be the only one found. And the passage should be equal to the known text.
        assert u'ChiPinyin' in found_modules
        assert len(found_modules) == 1
        assert output == u' Shén aì shìrén , shènzhì jiāng tāde dú shēng zǐ cìgĕi tāmen , jiào yīqiè xìn tāde , bú ' \
                         u'zhì mièwáng , fǎn dé yǒngshēng . '

    def test_load_bsv_zip(self):
        """
        Test that the bsv.zip file is loaded correctly.
        """
        # GIVEN: The bsv.zip file
        modules = SwordModules(os.path.join(TEST_RESOURCE_FOLDER, u'bsv.zip'))

        # WHEN: Parsing the BSV module and reading a passage.
        found_modules = modules.parse_modules()
        bible = modules.get_bible_from_module(u'BSV')
        output = bible.get(books=[u'john'], chapters=[3], verses=[16])

        # THEN: The BSV module should be the only one found. And the passage should be equal to the known text.
        assert u'BSV' in found_modules
        assert len(found_modules) == 1
        assert output == u'For God so loved the world, that he gave his only begotten Son, that whoever believes in ' \
                         u'him should not perish, but have everlasting life.'

    def test_load_asv_zip(self):
        """
        Test that the ASV.zip file is loaded correctly.
        """
        # GIVEN: The ASV.zip file
        modules = SwordModules(os.path.join(TEST_RESOURCE_FOLDER, u'ASV.zip'))

        # WHEN: Parsing the ASV module and reading a passage.
        found_modules = modules.parse_modules()
        bible = modules.get_bible_from_module(u'ASV')
        output = bible.get(books=[u'gen'], chapters=[3], verses=[20])

        # THEN: The ASV module should be the only one found. And the passage should be equal to the known text.
        assert u'ASV' in found_modules
        assert len(found_modules) == 1
        assert output == u'And the man called his wife’s name Eve; because she was the mother of all living.'

    def test_load_aranav_zip(self):
        """
        Test that the AraNAV.zip file is loaded correctly.
        """
        # GIVEN: The AraNAV.zip file
        modules = SwordModules(os.path.join(TEST_RESOURCE_FOLDER, u'AraNAV.zip'))

        # WHEN: Parsing the AraNAV module and reading a passage.
        found_modules = modules.parse_modules()
        bible = modules.get_bible_from_module(u'AraNAV')
        output = bible.get(books=[u'rev'], chapters=[22], verses=[19])

        # THEN: The AraNAV module should be the only one found.
        assert u'AraNAV' in found_modules
        assert len(found_modules) == 1
        # The passage should be empty since that verse is not in this translation.
        assert output.strip() == u'  وَلْتَكُنْ نِعْمَةُ رَبِّنَا يَسُوعَ الْمَسِيحِ مَعَكُمْ جَمِيعاً.'.strip()

    def test_load_sparv1909_zip(self):
        """
        Test that the encrypted SpaRV1909.zip file is loaded correctly.
        """
        # GIVEN: The SpaRV1909.zip file
        modules = SwordModules(os.path.join(TEST_RESOURCE_FOLDER, u'SpaRV1909.zip'))

        # WHEN: Parsing the SpaRV1909 module and reading a passage.
        found_modules = modules.parse_modules()
        bible = modules.get_bible_from_module(u'SpaRV1909')
        output = bible.get(books=[u'gen'], chapters=[3], verses=[20])

        # THEN: The SpaRV1909 module should be the only one found. And the passage should be equal to the known text.
        assert u'SpaRV1909' in found_modules
        assert len(found_modules) == 1
        print(output)
        assert output == u'Y llamó el hombre el nombre de su mujer, Eva; por cuanto ella era madre de todos ' \
                         u'los vivientes.'

        # WHEN: Reading a second passage
        output = bible.get(books=[u'john'], chapters=[3], verses=[17])

        # THEN: The the passage should be equal to the expected text
        assert output == u'Porque no envió Dios á su Hijo al mundo para que condene al mundo, mas para ' \
                         u'que el mundo sea salvo por él.'
