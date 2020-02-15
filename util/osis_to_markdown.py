#!/usr/bin/python3

import xml.etree.ElementTree as ET
from pathlib import Path
import shutil
import os

book_abbrev = [
    ("Genesis", "Gen"),
    ("Exodus", "Exod"),
    ("Leviticus", "Lev"),
    ("Numbers", "Num"),
    ("Deuteronomy", "Deut"),
    ("Joshua", "Josh"),
    ("Judges", "Judg"),
    ("Ruth", "Ruth"),
    ("1 Samuel", "1Sam"),
    ("2 Samuel", "2Sam"),
    ("1 Kings", "1Kgs"),
    ("2 Kings", "2Kgs"),
    ("1 Chronicles", "1Chr"),
    ("2 Chronicles", "2Chr"),
    ("Ezra", "Ezra"),
    ("Nehemiah", "Neh"),
    ("Tobit", "Tob"),
    ("Judith", "Jdt"),
    ("Esther", "Esth"),
    ("Maccabees", "1 Macc"),
    ("2 Maccabees", "2 Macc"),
    ("Job", "Job"),
    ("Psalms", "Ps"),
    ("Proverbs", "Prov"),
    ("Ecclesiastes", "Eccl"),
    ("Song of Songs", "Song"),
    ("Canticles", "Cant"),
    ("Wisdom", "Wis"),
    ("Sirach", "Sir"),
    ("Isaiah", "Isa"),
    ("Jeremiah", "Jer"),
    ("Lamentations", "Lam"),
    ("Baruch", "Bar"),
    ("Ezekiel", "Ezek"),
    ("Daniel", "Dan"),
    ("Hosea", "Hos"),
    ("Joel", "Joel"),
    ("Amos", "Amos"),
    ("Obadiah", "Obad"),
    ("Jonah", "Jonah"),
    ("Micah", "Mic"),
    ("Nahum", "Nah"),
    ("Habakkuk", "Hab"),
    ("Zephaniah", "Zeph"),
    ("Haggai", "Hag"),
    ("Zechariah", "Zech"),
    ("Malachi", "Mal"),
    ("Matthew", "Matt"),
    ("Mark", "Mark"),
    ("Luke", "Luke"),
    ("John", "John"),
    ("Acts", "Acts"),
    ("Romans", "Rom"),
    ("1 Corinthians", "1Cor"),
    ("2 Corinthians", "2Cor"),
    ("Galatians", "Gal"),
    ("Ephesians", "Eph"),
    ("Philippians", "Phil"),
    ("Colossians", "Col"),
    ("1 Thessalonians", "1Thess"),
    ("2 Thessalonians", "2Thess"),
    ("1 Timothy", "1Tim"),
    ("2 Timothy", "2Tim"),
    ("Titus", "Titus"),
    ("Philemon", "Phlm"),
    ("Hebrews", "Heb"),
    ("James", "Jas"),
    ("1 Peter", "1Pet"),
    ("2 Peter", "2Pet"),
    ("1 John", "1John"),
    ("2 John", "2John"),
    ("3 John", "3John"),
    ("Jude", "Jude"),
    ("Revelation", "Rev"),
]

def look_for_book_long_name(book_short_name):
    for book in book_abbrev:
        long_name, short_name = book
        if book_short_name == short_name:
            return long_name
    return ''


def generate_bible(bible_name, bible_file):
    dir_osis = '../source/osis/'
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

    # create readme file
    readme_file = open(dir_path + '/' + 'README.md', "wt")
    
    tag_osis_header = ns + "header"
    tag_osis_div = ns + "div"
    tag_osis_title = ns + "title"
    tag_osis_verse = ns + "verse"
    tag_osis_description = ns + "description"
    
    osis_header = osis_text[0]
    if osis_header.tag != tag_osis_header :
        print("OSIS header missing. Exit.")
        exit()

    osis_header_work = osis_header[1]
    for header_work_item in osis_header_work:
        if header_work_item.tag == tag_osis_title:
            readme_file.write('# ' + header_work_item.text + '\n\n')
        elif header_work_item.tag == tag_osis_description:
            readme_file.write(header_work_item.text + '\n\n')
        

    for book in osis_text[1:]:
        if book.tag != tag_osis_div or book.attrib['type'] != 'book':
            print("OSIS body error. Exit.")
            exit()
            
        book_id = book.attrib['osisID']
        book_long_name = look_for_book_long_name(book_id)
        if len(book_long_name) == 0:
            print("Book name not found:", book_id)
            exit()
            
        book_filename = dir_path + '/' + book_id + '.md'
        book_file = open(book_filename, "wt")
        print("writing " + book_filename)

        # book title
        book_file.write("# " + book_id + "\n\n")
        
        for chapter in book:
            if chapter.tag == tag_osis_title: # not a chapter, but a title, only occurs in Psalms
                line = "__" + chapter.text.strip() + "__"
                book_file.write(line)
                book_file.write('\n\n')
                continue
            
            chapter_id = chapter.attrib['osisID']
            # chapter title
            book_file.write("## " + chapter_id + "\n\n")

            for verse in chapter:
                line = ""
                if verse.tag == tag_osis_title:
                    line = "__" + verse.text.strip() + "__"
                elif verse.tag == tag_osis_verse:
                    verse_id = verse.attrib['osisID']
                    # ignore the chapter id in each line
                    verse_head = verse_id[(len(chapter_id)+1):]
                    verse_text = verse.text
                    line = ". ".join([verse_head, verse_text])
                else:
                    print("unknown tag at " + book_id + " : " + chapter_id)
                book_file.write(line)
                book_file.write('\n\n')

        book_file.close()

        
if __name__ == '__main__':
    bibles = [
        ('kjv', 'kjv.xml'),
        ('niv', 'niv.xml')
    ]

    for bible in bibles:
        generate_bible(bible[0], bible[1])

        
