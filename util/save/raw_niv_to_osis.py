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

def look_for_book_short_name(book_long_name):
    for book in book_abbrev:
        long_name, short_name = book
        if book_long_name == long_name:
            return short_name
    return ''

dir_osis = '../source/osis/'
dir_markdown = '../markdown/'
dir_niv = '../source/raw/niv/'

tmp_xml_head = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<tmp>\n'
tmp_xml_tail = '\n</tmp>\n'

osis_file_head = '''<?xml version='1.0' encoding='UTF-8'?>
<osis xsi:schemaLocation='http://www.bibletechnologies.net/2003/OSIS/namespace http://www.bibletechnologies.net/osisCore.2.1.1.xsd' xmlns='http://www.bibletechnologies.net/2003/OSIS/namespace' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'>
  <osisText osisIDWork='niv' xml:lang='en' osisRefWork='Bible'>
    <header>
      <revisionDesc>
        <date>2010-02-26</date>
        <p>initial OSIS 2.1.1 version</p>
      </revisionDesc>
      <work osisWork='niv'>
        <title>New International Version</title>
        <subject>The Holy Bible</subject>
        <description>New International Version</description>
        <type type='OSIS'>Bible</type>
        <identifier type='OSIS'>niv</identifier>
        <language type='IETF'>en</language>
        <refSystem>Bible</refSystem>
      </work>
    </header>

'''

osis_file_tail = '''

  </osisText>
</osis>

'''

osis_file = open("../source/osis/niv.xml", "wt")
osis_file.write(osis_file_head)

for raw_filename in os.listdir(dir_niv):
    print("converting", raw_filename)
    raw_file = open(dir_niv + raw_filename)
    tmp_xml = tmp_xml_head + raw_file.read() + tmp_xml_tail
    root = ET.fromstring(tmp_xml)
    book_xml_lines = []
    book_name_long = ''
    book_name_short = ''
    chapter_name = ''
    title = ''
    chapter_index = 0
    line_index = 0
    line_text = ''
    
    for item in root:
        if item.tag == 'book':
            book_name_long = item.text
            # find short name
            book_name_short = look_for_book_short_name(book_name_long)
            if len(book_name_short) == 0:
                print("cannot find book name ", book_name_long)
                exit()
            book_xml_lines.append('<div type=\'book\' osisID=\'' + book_name_short + '\'>')
        elif item.tag == 'c': # chapter
            chapter_index += 1
            chapter_name = book_name_short + '.' + str(chapter_index)
            if chapter_index > 1:
                book_xml_lines.append('</chapter>')
            book_xml_lines.append('<chapter osisID=\'' + chapter_name + '\'>')
        elif item.tag == 's': # title
            title = item.text
            book_xml_lines.append('<title>' + title + '</title>')
        elif item.tag == 'i': # line index
            line_index = item.text
        elif item.tag == 't': # text
            line_text = item.text
            book_xml_lines.append('<verse osisID=\'' + chapter_name + '.' + str(line_index) + '\'>' + line_text + '</verse>')
        else:
            print("unknown tag at ", raw_filename, book_name_log, chapter_name)
            exit()
            
    raw_file.close()
    book_xml_lines.append('</chapter>')
    book_xml_lines.append('</div>')
    osis_file.write('\n'.join(book_xml_lines))


osis_file.write(osis_file_tail)
osis_file.close()

