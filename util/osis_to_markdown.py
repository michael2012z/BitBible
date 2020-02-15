#!/usr/bin/python3

import xml.etree.ElementTree as ET
from pathlib import Path
import shutil
import os



def generate_bible(bible_name, bible_file):
    dir_osis = '../osis/'
    dir_markdown = '../markdown/'
    tree = ET.parse(dir_osis + bible_file)
    root = tree.getroot()
    ns = '{http://www.bibletechnologies.net/2003/OSIS/namespace}'
    osis_text = root[0]
    #print(osis_text.tag)
    # clear the dir
    dir_cwd = os.getcwd()
    dirpath = Path(dir_cwd + '/' + dir_markdown, bible_name)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)
    dir_path = str(dirpath)
    os.mkdir(dir_path)

    tag_osis_header = ns + "header"
    tag_osis_div = ns + "div"
    tag_osis_title = ns + "title"
    tag_osis_verse = ns + "verse"
    
    osis_header = osis_text[0]
    if osis_header.tag != tag_osis_header :
        print("OSIS header missing. Exit.")
        exit()

    for book in osis_text[1:]:
        if book.tag != tag_osis_div or book.attrib['type'] != 'book':
            print("OSIS body error. Exit.")
            exit()
        book_id = book.attrib['osisID']
        book_filename = dir_path + '/' + book_id + '.md'
        book_file = open(book_filename, "wt")
        print("writing " + book_filename)
        
        for chapter in book:
            chapter_id = chapter.attrib['osisID']
            for verse in chapter:
                line = ""
                if verse.tag == tag_osis_title:
                    line = verse.text
                elif verse.tag == tag_osis_verse:
                    verse_id = verse.attrib['osisID']
                    verse_text = verse.text
                    line = " ".join([verse_id, verse_text])
                else:
                    print("unknown tag at " + book_id + " : " + chapter_id)
                book_file.write(line)
                book_file.write('\n\n')

        book_file.close()

        
if __name__ == '__main__':
    bibles = [
        ('kjv', 'kjv.xml')
        ]

    for bible in bibles:
        generate_bible(bible[0], bible[1])

        
