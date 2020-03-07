#!/usr/bin/python3
import sys
sys.path.append('../util/')
import book_names
import os

def load_book(bible_name, book_name_short):
    file_path = '../markdown/'+bible_name+'/files/'+book_name_short+'.md'
    if os.path.exists(file_path):
        book = []
        chapter = []
        f = open(file_path, 'rt')
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if len(line) > 0:
                if line.startswith('## '): # a chapter starts
                    if len(chapter) > 0:
                        book.append(chapter)
                        chapter = []
                elif line.startswith('# '): # book title
                    continue
                elif line.startswith('__'): # TODO: story title
                    continue
                else: #verse
                    split_line = line.split(". ")
                    chapter.append(split_line[1])
        if len(chapter) > 0:
            book.append(chapter)
        return book
    else:
        return None
    

def load_bible(bible_name):
    bible = dict()
    for testament in book_names.book_names:
        for book_name in testament:
            _, book_name_short = book_name
            book = load_book(bible_name, book_name_short)
            if book != None:
                bible[book_name_short] = book
    return bible

    
if __name__ == '__main__':
    bible = load_bible("KJV")
    print(bible["Gen"][0][0])

    
