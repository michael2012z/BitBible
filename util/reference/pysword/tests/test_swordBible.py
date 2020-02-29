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

from tests import MagicMock, TestCase, call, patch

from pysword.bible import RawTextModule, RawTextModule4, SwordModuleType, SwordBible, Testament, ZTextModule, \
    ZTextModule4

TEST_RESOURCE_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), u'resources')


class TestBookStructure(TestCase):
    @patch('pysword.bible.Testament')
    def test_init_only_one_testament(self, mocked_testament):
        """
        Test that when loading a bible with only one testament, only that testament is available
        """
        # GIVEN: A mocked _get_ztext_files method in SwordBible
        mocked_testament.side_effect = [True, IOError('Not good')]

        # WHEN: Creating a SwordBible
        bible = SwordBible(u'test_path', SwordModuleType.ZTEXT, u'kjv', 'utf-8', u'OSIS')

        # THEN: Only 'nt' should have been loaded
        testaments = list(bible._testaments.keys())
        self.assertListEqual(testaments, [u'ot'],  u'Only "ot" files should be available')

    @patch('pysword.bible.SwordBible._setup')
    def test_init(self, patched_sword_bible_setup):
        """
        Test that the init loading of bible works
        """
        # GIVEN: A bible
        path = os.path.join(TEST_RESOURCE_FOLDER, u'modules', u'texts', u'ztext', u'finpr')

        # WHEN: Loading the bible
        bible = SwordBible(path)

        # THEN: It should load
        self.assertIsNotNone(bible, u'The bible should have loaded')


class TestSwordBible(TestCase):
    """
    Test the :class:`pysword.bible.SwordBible` class.
    """
    def setUp(self):
        setup_patcher = patch('pysword.bible.SwordBible._setup')
        self.addCleanup(setup_patcher.stop)
        setup_patcher.start()

    def test_instantiation_default(self):
        """
        Test that the instance returned is an instance of the correct class.
        """
        # GIVEN: The SwordBible class
        # WHEN: Creating an instance without any module_type specified
        instance = SwordBible('path')

        # THEN: The instance should be an instance of the :class:`pysword.bible.RawTextModule`
        self.assertIsInstance(instance, ZTextModule)
        self.assertFalse(isinstance(instance, ZTextModule4))

    def test_instantiation_raw_text(self):
        """
        Test that the instance returned is an instance of the correct class.
        """
        # GIVEN: The SwordBible class
        # WHEN: Creating an instance with a module_type of raw text
        instance = SwordBible('path', SwordModuleType.RAWTEXT)

        # THEN: The instance should be an instance of the :class:`pysword.bible.RawTextModule`
        self.assertIsInstance(instance, RawTextModule)
        self.assertFalse(isinstance(instance, RawTextModule4))

    def test_instantiation_raw_text_keyword(self):
        """
        Test that the instance returned is an instance of the correct class.
        """
        # GIVEN: The SwordBible class
        # WHEN: Creating an instance with a module_type of raw text as specified by a keyword argument
        instance = SwordBible('path', module_type=SwordModuleType.RAWTEXT)

        # THEN: The instance should be an instance of the :class:`pysword.bible.RawTextModule`
        self.assertIsInstance(instance, RawTextModule)
        self.assertFalse(isinstance(instance, RawTextModule4))

    def test_instantiation_raw_text_4(self):
        """
        Test that the instance returned is an instance of the correct class.
        """
        # GIVEN: The SwordBible class
        # WHEN: Creating an instance with a module_type of raw text 4
        instance = SwordBible('path', SwordModuleType.RAWTEXT4)

        # THEN: The instance should be an instance of the :class:`pysword.bible.RawTextModule4`
        self.assertIsInstance(instance, RawTextModule4)

    def test_instantiation_z_text(self):
        """
        Test that the instance returned is an instance of the correct class.
        """
        # GIVEN: The SwordBible class
        # WHEN: Creating an instance with a module_type of z text
        instance = SwordBible('path', SwordModuleType.ZTEXT)

        # THEN: The instance should be an instance of the :class:`pysword.bible.ZTextModule`
        self.assertIsInstance(instance, ZTextModule)
        self.assertFalse(isinstance(instance, ZTextModule4))

    def test_instantiation_z_text_4(self):
        """
        Test that the instance returned is an instance of the correct class.
        """
        # GIVEN: The SwordBible class
        # WHEN: Creating an instance with a module_type of z text 4
        instance = SwordBible('path', SwordModuleType.ZTEXT4)

        # THEN: The instance should be an instance of the :class:`pysword.bible.ZTextModule4`
        self.assertIsInstance(instance, ZTextModule4)

    def test_instantiation_invalid_type(self):
        """
        Test that the instance returned is an instance of the correct class.
        """
        # GIVEN: The SwordBible class
        # WHEN: Creating an instance with a module_type of zLD
        # THEN: A ValueError should be raised
        self.assertRaises(ValueError, SwordBible,  'path', 'zLD')

    def test_direct_instantiation_raw_text(self):
        """
        Test that the instance returned is an instance of the correct class.
        """
        # GIVEN: The :class:`pysword.bible.RawTextModule`
        # WHEN: Creating an instance of it
        instance = RawTextModule('path')

        # THEN: The instance should be an instance of the :class:`pysword.bible.RawTextModule`
        self.assertIsInstance(instance, RawTextModule)

    def test_direct_instantiation_raw_text_34(self):
        """
        Test that the instance returned is an instance of the correct class.
        """
        # GIVEN: The :class:`pysword.bible.RawTextModule4`
        # WHEN: Creating an instance of it
        instance = RawTextModule4('path')

        # THEN: The instance should be an instance of the :class:`pysword.bible.RawTextModule4`
        self.assertIsInstance(instance, RawTextModule4)

    def test_direct_instantiation_z_text(self):
        """
        Test that the instance returned is an instance of the correct class.
        """
        # GIVEN: The :class:`pysword.bible.ZTextModule`
        # WHEN: Creating an instance of it
        instance = ZTextModule('path')

        # THEN: The instance should be an instance of the :class:`pysword.bible.ZTextModule`
        self.assertIsInstance(instance, ZTextModule)

    def test_direct_instantiation_z_text_4(self):
        """
        Test that the instance returned is an instance of the correct class.
        """
        # GIVEN: The :class:`pysword.bible.ZTextModule4`
        # WHEN: Creating an instance of it
        instance = ZTextModule4('path')

        # THEN: The instance should be an instance of the :class:`pysword.bible.ZTextModule4`
        self.assertIsInstance(instance, ZTextModule4)


class TestDecodeBytesPy2(TestCase):
    def setUp(self):
        self.setup_patcher = patch.object(SwordBible, '_setup')
        self.addCleanup(self.setup_patcher.stop)
        self.setup_patcher.start()

    def test_decode_bytes_utf8(self):
        """
        Test SwordBible._decode_bytes when called with a Py2 str / Py3 bytes object encoded with utf-8
        """
        # GIVEN: A Py2 str / Py3 bytes object which has been encoded from utf-8
        bible_instance = SwordBible('module_path')
        unicode_data = u'Finnish Pyhä Raamattu (1933/1938)'
        byte_data = unicode_data.encode('utf-8')

        # WHEN: Calling `_decode_bytes`
        result = bible_instance._decode_bytes(byte_data)

        # THEN: The result should be equal to the original unicode data. `_encoding` should still be None, as it was
        #       successfully decoded in the try statment block
        self.assertEqual(unicode_data, result)
        self.assertEqual(bible_instance._encoding, None)

    def test_decode_bytes_iso_8859_1(self):
        """
        Test SwordBible._decode_bytes when called with a Py2 str / Py3 bytes object encoded with iso-8859-1
        """
        # GIVEN: A Py2 str / Py3 bytes object which has been encoded from iso-8859-1
        bible_instance = SwordBible('module_path')
        unicode_data = u'Finnish Pyhä Raamattu (1933/1938)'
        byte_data = unicode_data.encode(u'iso-8859-1')

        # WHEN: Calling `_decode_bytes`
        result = bible_instance._decode_bytes(byte_data)

        # THEN: The result should be equal to the original unicode data. `_encoding` should be set to `iso-8859-1` as
        #       the statment block failed.
        self.assertEqual(unicode_data, result)
        self.assertEqual(bible_instance._encoding, u'cp1252')

    def test_decode_bytes_specified_encoding(self):
        """
        Test SwordBible._decode_bytes when called with a Py2 str / Py3 bytes object encoded by the encoding specified in
        the initialisation of the SwordBible object
        """
        # GIVEN: A Py2 str / Py3 bytes object which has been encoded from utf-16, and when the encoding has
        #       been specified.
        bible_instance = SwordBible('module_path', encoding='utf-16')
        unicode_data = u'Finnish Pyhä Raamattu (1933/1938)'
        byte_data = unicode_data.encode('utf-16')

        # WHEN: Calling `_decode_bytes`
        result = bible_instance._decode_bytes(byte_data)

        # THEN: The result should be equal to the original unicode data. `_encoding` should be set to encoding specified
        self.assertEqual(unicode_data, result)
        self.assertEqual(bible_instance._encoding, 'utf-16')


class TestTestamentClass(TestCase):
    """
    Tests to test the :class:`pysword.bible.Testament` class.
    """
    @patch(u'pysword.bible.io')
    def test_instantiation(self, mocked_io):
        """
        Test the instantation of the :class:`pysword.bible.Testament` class
        """
        # GIVEN: The Testament class
        # WHEN: Instantiating it.
        instance = Testament(u'nt', test_file_1=u'test_1.ext', test_file_2=u'test_2.ext', test_file_3=u'test_3.ext')

        # THEN: An attribute should have been created for each file handler that was opened. io.open should have been
        #       called with each file.
        self.assertTrue(hasattr(instance, u'test_file_1'))
        self.assertTrue(hasattr(instance, u'test_file_2'))
        self.assertTrue(hasattr(instance, u'test_file_3'))
        # Prior to Py3.6 the order of keyword arguments was not guaranteed.
        mocked_io.open.assert_has_calls(
            [call(u'test_1.ext', u'rb'), call(u'test_2.ext', u'rb'), call(u'test_3.ext', u'rb')],
            any_order=True)
        self.assertEqual(mocked_io.open.call_count, 3)

    @patch(u'pysword.bible.io')
    def test_deletion(self, mocked_io):
        """
        Test the deletion of and instance of the :class:`pysword.bible.Testament` class
        """
        file_handle_1_mock = MagicMock()
        file_handle_2_mock = MagicMock()
        file_handle_3_mock = MagicMock()
        mocked_io.open.side_effect = [file_handle_1_mock, file_handle_2_mock, file_handle_3_mock]

        # GIVEN: An instance of the Testament class
        instance = Testament('nt', test_file_1=u'test_1.ext', test_file_2=u'test_2.ext', test_file_3=u'test_3.ext')

        # WHEN: Deleting the instance
        del instance

        # THEN: Each file should have been closed
        file_handle_1_mock.close.assert_called_once_with()
        file_handle_2_mock.close.assert_called_once_with()
        file_handle_3_mock.close.assert_called_once_with()
