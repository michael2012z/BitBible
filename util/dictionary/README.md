## How were the raw files created (Vocabulary.xml as example)
- cd raw_data
- split --bytes=1M Vocabulary.xml 
- mkdir Vocabulary
- mv x* Vocabulary
- zip -r Vocabulary.zip Vocabulary
- zipsplit -n 512000 Vocabulary.zip
- rm Vocabulary.zip 
- rm Vocabulary/x*
- mv Vocab*.zip Vocabulary/

## How to recover the dictionary file from split files
- cd raw_data
- cat Vocab*.zip > whole.zip
- zip -FF whole.zip --out Vocabulary.zip
- rm -f Vocab???.zip
- rm whole.zip
- unzip Vocabulary.zip
- cat Vocabulary/x* > Vocabulary.xml
- rm Vocabulary.zip
- rm -rf Vocabulary
