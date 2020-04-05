#!/usr/bin/python3
import sys
import xml.etree.ElementTree as ET
import book_names

'''
    Parse input XML text into Markdown files, through internal structure:
    [ # collection of book blocks
        ('Gen', # book name
            [ # collection of chapters
                [ # collection of verses
                    "In the begining...",
                    "And the earth...",
                    ......
                ]
            ]
        )
    ]
'''

def report_unknown(node):
    print("unknow node:", node.attrib)
    exit()

def osis_to_markdown(xml_text):
    '''
    Input: Text of a XML file
    Output: A list of books. Each book is in form of a tuple of (short_name, number_of_chapters, markdown_text)
    '''
    book_blocks = osis_to_structure(xml_text)
    markdown_buffers = []
    for book_block in book_blocks:
        #print(book_block[0])
        num_of_chapters, text = book_block_to_markdown(book_block)
        markdown_buffers.append((book_block[0], num_of_chapters, text))
    return markdown_buffers

def book_block_to_markdown(book_block):
    '''
    Input: Block of a book
    Output: The number of chapters and Markdown text of a book
    '''
    book_short_name, chapters = book_block
    file_name = book_short_name.lower() + ".md"
    buff = []
    book_long_name = book_names.get_long_name(book_short_name)
    buff.append("# " + book_long_name)
    chapter_index = 0
    for chapter in chapters:
        chapter_index += 1
        chapter_title = book_long_name + ' ' + str(chapter_index)
        buff.append("## " + chapter_title)
        verse_index = 0
        for verse in chapter:
            verse_index += 1
            buff.append(str(verse_index) + ". " + verse)
    return chapter_index, "\n\n".join(buff)
    
def osis_to_structure(xml_text):
    root = ET.fromstring(xml_text)
    ns = '{http://www.bibletechnologies.net/2003/OSIS/namespace}'
    tag_osis_header = ns + "header"
    tag_osis_div = ns + "div"
    tag_osis_title = ns + "title"
    tag_osis_verse = ns + "verse"
    tag_osis_chapter = ns + "chapter"
    tag_osis_w = ns + "w"
    tag_osis_note = ns + "note"

    book_blocks = []
    
    osis_text = root[0]
    osis_header = osis_text[0]
    if osis_header.tag != tag_osis_header :
        print("OSIS header missing. Exit.")
        exit()

    if len(osis_text) < 2:
        print("OSIS testaments missing. Exit.")
        exit()
        
    osis_testaments = osis_text[1:]
    for osis_testament in osis_testaments:
        # testament +
        if osis_testament.attrib['type'] == 'x-testament':
            for osis_book in osis_testament:
                # book +
                if osis_book.attrib['type'] == 'book':
                    book_short_name = osis_book.attrib['osisID']
                    chapter_blocks = []
                    for osis_chapter in osis_book:
                        # chapter +
                        if osis_chapter.tag == tag_osis_chapter:
                            chapter_id = osis_chapter.attrib['osisID']
                            chapter_block = []
                            #print(chapter_id)
                            for osis_verse in osis_chapter:
                                # verse +
                                if osis_verse.tag == tag_osis_verse:
                                    # remove notes at first
                                    has_note = True
                                    while (has_note):
                                        has_note = False
                                        for i in osis_verse.iter():
                                            if i.tag == tag_osis_note:
                                                osis_verse.remove(i)
                                                has_note = True
                                    verse_text = []
                                    for t in osis_verse.itertext():
                                        verse_text.append(t)
                                    verse_text = "".join(verse_text)
                                    #print(verse_text)
                                    chapter_block.append(verse_text)
                                # verse -
                                else:
                                    report_unknown(osis_verse)
                            chapter_blocks.append(chapter_block)
                        # chapter -
                        else:
                            report_unknown(osis_chapter)
                    book_block = (book_short_name, chapter_blocks)
                    book_blocks.append(book_block)
                # book -
                else:
                    report_unknown(osis_book)
        # testament -
        else:
            report_unknown(osis_testament)
            exit()
                
    return book_blocks

if __name__ == '__main__':
    args = sys.argv
    xml_file = open(args[1], 'rt')
    xml_text = xml_file.read()
    xml_file.close()
    markdown_buffers = osis_to_markdown(xml_text)
    print(markdown_buffers[0][0], markdown_buffers[0][1])
