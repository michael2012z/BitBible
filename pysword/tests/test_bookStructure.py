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

from tests import TestCase

from pysword.books import BookStructure


class TestBookStructure(TestCase):
    def test_get_indicies_invalid_chapter(self):
        """
        Test that get_indicies() throws exception on invalid chapter
        """
        # GIVEN: A test BookStructure with 4 chapters
        structure = BookStructure(u'test name', u'test osis name', u'test abbr', [31, 25, 24, 26])

        # WHEN: Calling get_indicies() with an invalid chapter parameter
        # THEN: An ValueError exception should be thrown
        self.assertRaises(ValueError, structure.get_indicies,  5, 1)

    def test_get_indicies_invalid_verse(self):
        """
        Test that get_indicies() throws exception on invalid verse
        """
        # GIVEN: A test BookStructure with 4 chapters
        structure = BookStructure(u'test name', u'test osis name', u'test abbr', [31, 25, 24, 26])

        # WHEN: Calling get_indicies() with an invalid verse parameter
        # THEN: An ValueError exception should be thrown
        self.assertRaises(ValueError, structure.get_indicies,  3, 25)
