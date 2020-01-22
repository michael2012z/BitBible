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

from tests import MagicMock, TestCase

from pysword.books import BibleStructure


class TestBibleStructure(TestCase):
    def test_init_invalid_versification(self):
        """
        Test that BibleStructure raises an exception on invalid versification
        """
        # GIVEN: An invalid versification
        versification = u'does_not_exists'

        # WHEN: Creating a new BibleStructure
        # THEN: An ValueError exception should be raised
        self.assertRaises(ValueError, BibleStructure,  versification)

    def test_ref_to_indicies(self):
        """
        Test that ref_to_indicies can handle unicode and non-unicode input, only makes sense for python2
        """
        # GIVEN: A bible structure with mocked find_book
        bible_structure = BibleStructure(u'kjv')
        mocked_find_book = MagicMock()
        mocked_find_book.return_value = ('mocked_testament', MagicMock())
        bible_structure.find_book = mocked_find_book
        bible_structure._book_offset = MagicMock()

        # WHEN: Calling ref_to_indicies with both str and unicode input
        bible_structure.ref_to_indicies('test')
        bible_structure.ref_to_indicies(u'test')

        # THEN: The mocked find_book should have been called twice
        self.assertEqual(mocked_find_book.call_count, 2, u'The mocked find_book should have been called twice')
