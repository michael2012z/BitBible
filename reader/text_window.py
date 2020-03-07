from window import Window
from log import *

class TextWindow(Window):
    '''
    Layout:
    |001. xxxxxxxxxxxxxxxxxxxxxx| -
    |     xxxxxxxxxxxxxxxxxxxxxx| verse buffer height
    |     xxxxxxxxxxxx          | -
    |002. xxxxxxxxxxxxxxxxxxxxxx|
    |     xxxxxxxxxxxx          |
    |    |<--  verses block  -->|
    |<--- verse buffer width -->|

    Meta data format:
    [ <- all verses in the chapter
        ( <- one verse
            "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  <- verse raw text
            [ <- block of verse text, broken into lines (align to text area width)
                "xxxxxxxxxxxxxxx",
                "xxxxxxxxxxxxxxx",
                "xxxxxxx"
            ],
            [ <- split words data collection, for all words
                ( "a-word", row_in_block, column_in_block), <- data of a word
                ...
            ]
        ),
        ... <- other versers
    ]
    '''
    def __init__ (self, main_window, y, x, h, w, title="UNTITLED"):
        super(TextWindow, self).__init__(main_window, y, x, h, w, title)
        self.meta_data = []

    def make_verse_meta_data(self, raw_text):
        verse_block = self.break_text(raw_text, self.columns-5)
        padded_raw_text = "".join(verse_block)
        words = raw_text.split()
        words_meta_data = []
        pos = 0
        for word in words:
           offset = pos + padded_raw_text[pos:].find(word)
           pos = offset + len(word)
           words_meta_data.append((word, offset//(self.columns-5), offset%(self.columns-5)))
        return (raw_text, verse_block, words_meta_data)
           

    def make_verse_display_buffer(self, index, verse_meta_data):
        display_buffer = []
        head = "{:0>3d}. ".format(index)
        for line in verse_meta_data[1]:
            display_line = "{}{}".format(head, line)
            display_buffer.append(display_line)
            head = "     "
        return display_buffer
        
    def load(self, title, verses):
        '''
        This function breaks the text lines into display lines according to display columns and show the text.
        text_lines: List of a tuple, each tuple contains a tag (usually index) and a line of text.
        '''
        self.set_title(title)

        # make meta data for all verses
        self.chapter_meta_data = []
        for verse in verses:
            self.chapter_meta_data.append(self.make_verse_meta_data(verse))

        # build display buffer,
        display_buffer = []
        index = 0
        for verse_meta_data in self.chapter_meta_data:
            index += 1
            verse_buffer = self.make_verse_display_buffer(index, verse_meta_data)
            for buffer_line in verse_buffer:
                display_buffer.append(buffer_line)
        
        # render the display area
        start_index = 0
        for i in range(self.lines-1):
            if (start_index + i) >= len(display_buffer):
                break
            self.win.addstr(i+1, 0, display_buffer[start_index + i])


    # ------------------------- code below not finished -------------------
    def display_buffer_line_screen_line(self, buffer_line):
        return 0
        
    def verse_index_to_display_buffer_line(self, verse_index):
        return 0

    def word_index_to_verse_buffer_position(self, word_index):
        return (0, 0)
    
    def print_selected(self, text, screen_line, column):
        pass
            
    def set_selected(self, verse_index, word_index):
        buffer_line = self.verse_index_to_display_buffer_line(verse_index)
        screen_line = self.display_buffer_line_screen_line(buffer_line)
        if index == -1: # select the index
            self.print_selected("{:0>3d}. ".format(verse_index), screen_line, 0)
        else:
            word_text, row_in_block, column_in_block = self.meta_data[verse_index][2]
            self.print_selected(word_text, screen_line + row_in_block + 5 + column_in_block)
        
    def handle_key(char):
        pass
    
