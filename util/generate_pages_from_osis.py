#!/usr/bin/python3
import os
import sys
import book_names
import osis_to_markdown as osis2md
import bible_versions as bibver
from pathlib import Path
import shutil

def generate_readme_books_table(book_list):
    books_per_row = 4
    num_books_added = 0
    buf = []
    buf.append('<table>')
    row_buf = []
    for book in book_list:
        short_name, num_of_chapters = book
        long_name = book_names.get_long_name(short_name)
        num_books_added += 1
        row_buf.append('<td>')
        link = 'files/' + short_name + '.md'
        row_buf.append('<b>' + '<a href=\'' + link + '\'>' + long_name + '</a>' + '</b><br/>')
        chapter_list = []

        # show 9 chapter-links for the most
        max_num_chapter_links = 9
        chapter_numbers = list(range(1, num_of_chapters + 1))
        selected_chapter_numbers = chapter_numbers
        if num_of_chapters > max_num_chapter_links:
            number_in_group = num_of_chapters / max_num_chapter_links
            selected_chapter_numbers = list(map(lambda x: chapter_numbers[int(x * number_in_group)], list(range(max_num_chapter_links))))
                
        for i in selected_chapter_numbers:
            link = 'files/' + short_name + '.md#' + (long_name + ' ' + str(i)).replace(' ', '-').lower()
            chapter_list.append('<a href=\'' + link + '\'>' + str(i) + '</a>')
                
        row_buf.append(', '.join(chapter_list))
        row_buf.append('</td>')

        if num_books_added % books_per_row == 0:
            buf.append('<tr>\n' + '\n'.join(row_buf) + '</tr>')
            row_buf = []

    if len(row_buf) > 0:
        buf.append('<tr>\n' + '\n'.join(row_buf) + '</tr>')

    buf.append('</table>')
    return '\n'.join(buf)
    

def generate_readme_buffer(version_name, book_list):
    readme_title, readme_description = bibver.get_info(version_name)
    buf = []
    buf.append('# ' + readme_title)
    if len(readme_description) > 0:
        buf.append(readme_description)

    ot_names_set = set(book_names.get_ot_short_names())
    nt_names_set = set(book_names.get_nt_short_names())
    book_names_set = set([x[0] for x in book_list])

    buf.append('')
    
    # handle Old Testament
    if ot_names_set & book_names_set:
        buf.append('## Old Testament')
        ot_book_list = []
        for ot_book_name in book_names.get_ot_short_names():
            for book_candidate in book_list:
                if book_candidate[0] == ot_book_name:
                    ot_book_list.append(book_candidate)
        buf.append(generate_readme_books_table(ot_book_list))
    
    # handle New Testament
    if nt_names_set & book_names_set:
        buf.append('## New Testament')
        nt_book_list = []
        for nt_book_name in book_names.get_nt_short_names():
            for book_candidate in book_list:
                if book_candidate[0] == nt_book_name:
                    nt_book_list.append(book_candidate)
        buf.append(generate_readme_books_table(nt_book_list))

    return '\n\n'.join(buf)


def generate_pages_from_osis(version_name, xml_path):
    xml_file = open(xml_path, 'rt')
    xml_text = xml_file.read()
    xml_file.close()
    markdown_buffers = osis2md.osis_to_markdown(xml_text)

    # generate book files
    dir_osis = '../source/osis/'
    dir_markdown = '../markdown/'
    dir_cwd = os.getcwd()
    dirpath = Path(dir_cwd + '/' + dir_markdown, version_name)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)
    dir_path = str(dirpath)
    os.mkdir(dir_path)
    dir_files_path = dir_path + "/files"
    os.mkdir(dir_files_path)

    book_list = []
    for book in markdown_buffers:
        short_name, num_chapters, buff = book
        book_list.append((short_name, num_chapters))
        book_filename = dir_files_path + '/' + short_name + '.md'
        book_file = open(book_filename, "wt")
        book_file.write(buff)
        book_file.close()
    
    # generate README.md
    readme_buf = generate_readme_buffer(version_name, book_list)
    # create readme file
    readme_file = open(dir_path + '/' + 'README.md', "wt")
    readme_file.write(readme_buf)
    readme_file.close()

if __name__ == '__main__':
    args = sys.argv
    if len(args) == 3:
        print("converting", args[2])
        generate_pages_from_osis(args[1], args[2])
    else:
        print("Usage: generate_pages_from_osis.py KJV ./tmp/kjv.xml")

