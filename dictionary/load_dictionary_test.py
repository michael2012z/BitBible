#!/usr/bin/python3
import os
import sys
import xml.etree.ElementTree as ET


tree = ET.parse('dictionary/A/adventure.xml')
word_data = tree.getroot()[0]

word = ""
pron = ""
freq = 0
defi = ""
ety = ""
family = ""
examples = []
hints = []
for attr in word_data:
    if attr.tag == 'word':
        word = attr.text
    elif attr.tag == 'pron':
        pron = attr.text
    elif attr.tag == 'freq':
        freq = attr.text
    elif attr.tag == 'def':
        defi = attr.text
    elif attr.tag == 'family':
        family = attr.text
    elif attr.tag == 'examples':
        for example in attr:
            examples.append(example.text)
    elif attr.tag == 'hints':
        for hint in attr:
            p = ""
            m = ""
            for i in hint:
                if i.tag == 'property':
                    p = i.text
                else:
                    m = i.text
            hints.append((p, m))
word_item = (word, pron, freq, defi, ety, family, examples, hints)
print(word_item)

