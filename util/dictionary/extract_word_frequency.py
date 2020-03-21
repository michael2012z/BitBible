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

def extract_word_frequency(html_text):
    # print(html_text)
    freq = 0
    pron = ""
    definition = ""
    example = ""
    html_doc = html_head + html_text + html_tail
    soup = BeautifulSoup(html_doc, 'html.parser')
    # frequency
    for div in soup.body.find_all("div"):
        if 'data-band' in div.attrs.keys():
            freq = int(div.attrs['data-band'])
    # pron
    tags = soup.find_all("span")
    for tag in tags:
        if tag.has_attr("class") and tag.attrs['class'][0] == "pron":
            pron = tag.get_text().replace("\n", "").replace(" )", ")").strip()
            if pron[0] == "(" and pron[-1] == ")":
                pron = pron[1:-1]
            else:
                pron = ""
            break
            
    # def
    tags = soup.find_all("span")
    for tag in tags:
        if tag.has_attr("class") and tag.attrs['class'][0] == "def":
            definition = tag.get_text().strip()
            break

    # example
    tags = soup.find_all("span")
    for tag in tags:
        if tag.has_attr("class") and tag.attrs['class'][0] == "orth":
            example = tag.get_text().strip()[2:]
            break

    #print("{} : {} : {} : {}".format(freq, pron, definition, example))
    return freq

def build_word_list(dict_file):
    alpha = ''
    words = [
             [],# 0 - no frequency
             [],# 1
             [],# 2
             [],# 3
             [],# 4
             [] # 5
             ]
    buf = []
    l = 0
    with open(dict_file, "rt") as collins:
        for line in collins:
            l += 1
            if line == '</>\n':
                word = buf[0][:-1]
                if word.find(" ") > 0: # skip words combination
                    buf = []
                    continue
                frequency = extract_word_frequency("".join(buf))
                buf = []
                words[frequency].append(word)
                if word[0].isalpha() and word[0].upper() != alpha:
                    alpha = word[0].upper()
                    print("handling {} words".format(alpha))
            else:
                buf.append(line)
    return words


def write_frequency_files(word_list):
    freq = 0
    for freq_words in words:
        with open("words-" + str(freq) + ".txt", "wt") as f:
            for word in freq_words:
                f.write(word+"\n")
            freq += 1
            

if __name__ == '__main__':
    word_list = build_word_list("Collins.xml")
    #word_list = build_word_list("example.xml")
    #write_frequency_files(word_list)
