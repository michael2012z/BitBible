#!/usr/bin/python3
import os
import sys
from xml.etree.ElementTree import Element, SubElement, Comment
import xml.etree.ElementTree as ET
from extract_word_explanation import extract_word_explanation
from extract_word_frequency import build_word_list

xml_head = '<?xml version="1.0"?>\n<data>\n'

xml_tail = '\n</data>'

def make_xml_text(meta_data):
    word_data = Element('word_data')

    word = SubElement(word_data, 'word')
    word.text = str(meta_data[0])
    
    freq = SubElement(word_data, 'freq')
    freq.text = str(meta_data[1][0])
    
    pron = SubElement(word_data, 'pron')
    pron.text = meta_data[1][1]
    
    defi = SubElement(word_data, 'def')
    defi.text = meta_data[2][0]

    ety = SubElement(word_data, 'ety')
    ety.text = meta_data[2][1]

    family = SubElement(word_data, 'family')
    family.text = ";".join(meta_data[2][2])

    examples = SubElement(word_data, 'examples')
    for example in meta_data[2][3]:
        e = SubElement(examples, 'example')
        e.text = example

    hints = SubElement(word_data, 'hints')
    for hint in meta_data[2][4]:
        h = SubElement(hints, 'hint')
        p = SubElement(h, 'property')
        p.text = hint[0]
        m = SubElement(h, 'meaning')
        m.text = hint[1]

    return ET.tostring(word_data).decode("utf-8") 
    

def convert_vocabulary_into_xmls(dict_file, collins, support_combination = False):
    alpha = ''
    words = []
    buf = []
    output = None
    with open(dict_file, "rt") as dict_file:
        for line in dict_file:
            if line == '</>\n':
                word = buf[0][:-1]
                if support_combination == False and word.find(" ") > 0:
                    buf = []
                    continue
                explanation = extract_word_explanation("".join(buf))
                collins_data = (0, "")
                if word in collins:
                    collins_data = collins[word]
                xml_text = make_xml_text((word, collins_data, explanation))
                if output != None:
                    output.write(xml_text)
                buf = []
                if word[0].isalpha() and word[0].upper() != alpha:
                    alpha = word[0].upper()
                    if output != None:
                        output.write(xml_tail)
                    output = open("dictionary/" + alpha + ".xml", "wt")
                    output.write(xml_head)
                    print("handling {} words".format(alpha))
            else:
                buf.append(line)
        if output != None:
            output.write(xml_tail)

            
def convert_vocabulary_into_separate_xmls(dict_file, collins):
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for letter in letters:
        if not os.path.exists("dictionary/" + letter):
            os.makedirs("dictionary/" + letter)
    alpha = ''
    words = []
    buf = []
    output = None
    with open(dict_file, "rt") as dict_file:
        for line in dict_file:
            if line == '</>\n':
                word = buf[0][:-1]
                if word.find(" ") > 0:
                    buf = []
                    continue
                explanation = extract_word_explanation("".join(buf))
                buf = []
                collins_data = (0, "")
                if word in collins:
                    collins_data = collins[word]
                xml_text = make_xml_text((word, collins_data, explanation))

                # write to a seperate xml
                if word[0].isalpha():
                    if alpha != word[0].upper():
                        alpha = word[0].upper()
                        print("generating dictionary files for {} words".format(alpha))
                else:
                    continue

                try:
                    output_fn = "dictionary/" + alpha  + "/" + word.lower() + ".xml"
                    if os.path.exists(output_fn):
                        print("multiple items exist for {}, overwriting".format(word))
                    output = open(output_fn, "wt")
                    output.write(xml_head)
                    output.write(xml_text)
                    output.write(xml_tail)
                    output.close()
                except:
                    print("error happens when creating dictionary for {}".format(word))
            else:
                buf.append(line)



if __name__ == '__main__':
    # collins contains pron and freq
    print("building word frequency list")
    _, collins = build_word_list("Collins.xml")
    # collins = dict()
    # convert Vocabulary dictionary into XML files, adding pron and freq
    print("building dictionary files")
    # dict_file = "example.xml"
    dict_file = "Vocabulary.xml"
    convert_vocabulary_into_separate_xmls(dict_file, collins)

