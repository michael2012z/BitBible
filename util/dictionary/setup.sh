#!/bin/bash

cd raw_data

cat Vocab*.zip > whole.zip
zip -FF whole.zip --out Vocabulary.zip
unzip Vocabulary.zip
cat Vocabulary/x* > Vocabulary.xml
rm -f whole.zip
rm -f Vocabulary.zip
rm -rf Vocabulary

cat Collin*.zip > whole.zip
zip -FF whole.zip --out Collins.zip
unzip Collins.zip
cat Collins/x* > Collins.xml
rm -f whole.zip
rm -f Collins.zip
rm -rf Collins

cd ..

rm -rf dictionary
python3 build_dictionary.py
