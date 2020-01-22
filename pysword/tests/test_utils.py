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

from tests import TestCase, skipUnless

try:
    import pathlib
except ImportError:
    pass

from pysword.utils import path_like_to_str


class TestPathLikeToStr(TestCase):
    @skipUnless(sys.version_info >= (3, 6), u'Only Python 3.6 and above has the os.PathLike object')
    def test_path_like_object(self):
        # GIVEN: An object that implements the `os.PathLike` `__fspath__` method
        path_like_object = pathlib.Path(u'test', u'path')

        # WHEN: Calling with path_like_to_str with an `os.PathLike` object
        result = path_like_to_str(path_like_object)

        # Then a string of the Path should have been returned
        self.assertIsInstance(result, str)
        self.assertEqual(result, os.path.join(u'test', u'path'))

    @skipUnless(sys.version_info >= (3, 4) and sys.version_info < (3, 6),
                u'Only Python 3.4 and 3.5 has a `pathlib.Path` object that is not also a `os.PathLike` object.')
    def test_path_object(self):
        # GIVEN: A `pathlib.Path` object
        path_object = pathlib.Path(u'test', u'path')

        # WHEN: Calling with path_like_to_str with an `pathlib.Path` object
        result = path_like_to_str(path_object)

        # Then a string of the Path should have been returned
        self.assertIsInstance(result, str)
        self.assertEqual(result, os.path.join(u'test', u'path'))

    @skipUnless(sys.version_info >= (3,), u'Use the str object in py3')
    def test_str_object(self):
        # GIVEN: A `str` object
        str_object = os.path.join(u'test', u'path')

        # WHEN: Calling with path_like_to_str with an `pathlib.Path` object
        result = path_like_to_str(str_object)

        # THEN: The returned valus should be a str and equal to the object passed in
        self.assertIsInstance(result, str)
        self.assertEqual(result, str_object)

    @skipUnless(sys.version_info < (3,), u'Use the unicode object in py2')
    def test_unicode_object(self):
        # GIVEN: A `unicode` object
        unicode_object = os.path.join(u'test', u'path')

        # WHEN: Calling with path_like_to_str with an `unicode` object
        result = path_like_to_str(unicode_object)

        # THEN: The returned valus should be a unicode and equal to the object passed in
        self.assertIsInstance(result, unicode)
        self.assertEqual(result, unicode_object)

    def test_invalid_type(self):
        # GIVEN: A list of unsupported types
        unsupported_types = [None, False, True, 0, 1, 3, list(), dict(), tuple()]

        for unsupported_object in unsupported_types:
            # WHEN: Calling path_like_to_str with an invalid object
            self.assertRaises(TypeError, path_like_to_str, unsupported_types)
