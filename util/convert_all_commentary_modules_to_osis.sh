#!/bin/bash
export SWORD_PATH=$(pwd)/tmp
mkdir tmp

unzip ../commentary/Geneva.zip -d tmp/ && mod2osis Geneva > tmp/Geneva.xml
unzip ../commentary/MHCC.zip -d tmp/ && mod2osis MHCC > tmp/MHCC.xml
unzip ../commentary/MHC.zip -d tmp/ && mod2osis MHC > tmp/MHC.xml
