#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# PySword - A native Python reader of the SWORD Project Bible Modules         #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2019 Various developers:                                 #
# Kenneth Arnold, Joshua Gross, Tomas Groth, Ryan Hiebert, Philip Ridout,     #
# Matthew Wardrop                                                             #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 51  #
# Franklin St, Fifth Floor, Boston, MA 02110-1301 USA                         #
###############################################################################

import zipfile
import os

try:
    import urllib.request as urllib
except:
    import urllib


def get_and_extract(url, filename):
    """
    Downloads and extract bibles for testing
    """
    target_folder = os.path.dirname(os.path.realpath(__file__))
    target_file = os.path.join(target_folder, filename)
    print(u'Downloading from %s...' % url)
    urllib.urlretrieve(url, target_file)
    print('Extracting %s...' % filename)
    with zipfile.ZipFile(target_file, u'r') as z:
        z.extractall(target_folder)


bibles = [(u'ftp://ftp.xiphos.org/zip/chipinyin.zip', u'chipinyin.zip'),
          (u'ftp://ftp.xiphos.org/zip/bsv.zip', u'bsv.zip'),
          (u'http://www.crosswire.org/ftpmirror/pub/sword/packages/rawzip/FinPR.zip', u'FinPR.zip'),
          (u'http://www.crosswire.org/ftpmirror/pub/sword/packages/rawzip/ASV.zip', u'ASV.zip'),
          (u'http://www.crosswire.org/ftpmirror/pub/sword/packages/rawzip/AraNAV.zip', u'AraNAV.zip'),
          (u'http://www.crosswire.org/ftpmirror/pub/sword/packages/rawzip/SpaRV1909.zip', u'SpaRV1909.zip'),
          ]


for bible in bibles:
    get_and_extract(bible[0], bible[1])
