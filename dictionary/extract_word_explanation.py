#!/usr/bin/python3
import os
import sys
from bs4 import BeautifulSoup

html_head = '''
<!DOCTYPE html>
<html itemscope="" itemtype="http://schema.org/WebPage" lang="en-IN">
<head></head>
<body>
'''

html_tail = '''
</body>
</html>
'''

def extract_word_explanation(html_text):
    # print(html_text)
    family = []
    definition = ""
    etymology = ""
    examples = []
    hints = []
    html_doc = html_head + html_text + html_tail
    soup = BeautifulSoup(html_doc, 'html.parser')

    # definition
    for tag in soup.find_all("div"):
        if tag.has_attr("class") and tag.attrs['class'] == ['i', 't', 's']:
            definition = tag.get_text()

    # etymology
    for tag in soup.find_all("div"):
        if tag.has_attr("class") and tag.attrs['class'] == ['a', 'i']:
            etymology = tag.get_text()
    
    # word family
    tags = soup.find_all("span")
    for tag in tags:
        if tag.has_attr("class") and tag.attrs['class'] == ['b', 'c'] and tag.get_text() == "WORD FAMILY":
            family_list = tag.find_next("div").get_text()
            family = family_list.split("/")

    # examples
    tags = soup.find_all("span")
    for tag in tags:
        if tag.has_attr("class") and tag.attrs['class'] == ['b', 'c'] and tag.get_text() == "USAGE EXAMPLES":
            examples_tag = tag.find_next("div")
            if examples_tag.has_attr("id") and examples_tag.attrs['id'] == "vUi":
                for example_tag in examples_tag.find_all("div"):
                    if example_tag.has_attr("class") and example_tag.attrs['class'] == ['n']:
                        examples.append(example_tag.get_text())

    # hints
    tmp_kind = []
    tmp_meaning = []
    for tag in soup.find_all("div"):
        if tag.has_attr("class") and tag.attrs['class'] == ['a', 'm']:
            # a,v,n,...
            for p_tag in tag.find_all("a"):
                if p_tag.has_attr("class") and len(p_tag.attrs) == 2:
                    tmp_kind.append(p_tag.get_text())
            # meaning
            for meaning_tag in tag.find_all("span"):
                if meaning_tag.has_attr("class") and meaning_tag.attrs["class"] == ['t']:
                    tmp_meaning.append(meaning_tag.get_text())
            # combine
            for i in range(len(tmp_kind)):
                hints.append((tmp_kind[i], tmp_meaning[i]))
                        
    return (definition, etymology, family, examples, hints)


def build_word_list(dict_file):
    alpha = ''
    words = []
    buf = []
    with open(dict_file, "rt") as dict_file:
        for line in dict_file:
            if line == '</>\n':
                word = buf[0][:-1]
                explanation = extract_word_explanation("".join(buf))
                buf = []
                words.append((word, explanation))
                if word[0].isalpha() and word[0].upper() != alpha:
                    alpha = word[0].upper()
                    print("handling {} words".format(alpha))
            else:
                buf.append(line)
    return words



if __name__ == '__main__':
    #word_list = build_word_list("Collins.xml")
    word_list = build_word_list("Vocabulary.xml")
#    for word in word_list:
#        print(word)

