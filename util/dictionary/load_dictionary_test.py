#!/usr/bin/python3
import os
import sys
import xml.etree.ElementTree as ET


words = dict() # {"word": (pron, freq, def, ety, family, examples, hints)}

tree = ET.parse('dictionary/G.xml')
root = tree.getroot()

for word_data in root:
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
                if hint.tag == 'property':
                    p = hint.text
                else:
                    m = hint.text
                hints.append((p, m))
        words[word] = (pron, freq, defi, ety, family, examples, hints)
    print(words)
