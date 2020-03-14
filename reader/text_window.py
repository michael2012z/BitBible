import curses
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
        self.meta_data = []
        # display buffer's upper boundary in window
        self.buffer_upper_line = 0
        # display buffer's lower boundary in window
        # note: it is the next line to the last
        #       displayed line
        self.buffer_lower_line = 0
        # highlighted line of the window
        # note: this is not a line in display buffer
        self.current_line = 0
        # cursor location in current line, it's always the postion of
        # some word's first letter.
        # Valid value should be >= 5
        self.current_cursor = 0
        self.selected_word = ""
        self.display_buffer = []
        super(TextWindow, self).__init__(main_window, y, x, h, w, title)
        log("text window height = {}".format(self.height))

    def print_line(self, line_num, text, highlighted = False):
        if highlighted == False:
            self.win.addstr(line_num, 0, text)
            if self.columns > len(text):
                self.win.addstr(line_num, len(text), ' ' * (self.columns - len(text)))
            return
        
        pure_text = text[4:].strip()
        self.win.addstr(line_num, 0, text[:4], curses.color_pair(3))
        words = pure_text.split(" ")
        pos = 4
        for word in words:
            if self.current_cursor in range(pos, pos + 1 + len(word)):
                self.current_cursor = pos
                self.selected_word = word
                color_index = 4
            else:
                color_index = 3
            self.win.addstr(line_num, pos, ' ', curses.color_pair(3))
            self.win.addstr(line_num, pos+1, word, curses.color_pair(color_index))
            pos += 1 + len(word)

        if self.columns > len(text):
            padding = self.columns - len(text)
            self.win.addstr(line_num, pos, ' ' * padding, curses.color_pair(3))
            
    def refresh(self):
        self.selected_word = ""
        for i in range(self.height-1):
            if (i + self.buffer_upper_line) < self.buffer_lower_line:
                self.print_line(i+1, self.display_buffer[self.buffer_upper_line + i], i == self.current_line)

        super(TextWindow, self).refresh()
        
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
        self.display_buffer = []
        index = 0
        for verse_meta_data in self.chapter_meta_data:
            index += 1
            verse_buffer = self.make_verse_display_buffer(index, verse_meta_data)
            for buffer_line in verse_buffer:
                self.display_buffer.append(buffer_line)

        # set the display boundaries
        self.buffer_upper_line = 0
        self.buffer_lower_line = self.height - 1
        if self.buffer_lower_line > len(self.display_buffer):
           self.buffer_lower_line = len(self.display_buffer)
           


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

    def move_to_next_line(self):
        if self.current_line + self.buffer_upper_line < self.buffer_lower_line - 1:
            # normal case
            self.current_line += 1
        else:
            if self.buffer_lower_line - self.buffer_upper_line < self.height:
                # lower boundary is in the middle of screen, no move
                return
            else:
                # move page one line down
                self.buffer_upper_line += 1
                self.buffer_lower_line += 1
        self.refresh()
                
    def move_to_prev_line(self):
        if self.current_line == 0:
            if self.buffer_upper_line == 0:
                return
            else:
                self.buffer_upper_line -= 1
                self.buffer_lower_line -= 1
        else:
            self.current_line -= 1
        self.refresh()

    def move_to_next_word(self):
        log("1 current_cursor = {}, selected = ".format(self.current_cursor, self.selected_word))
        if self.current_cursor == 0:
            self.current_cursor = 4
        else:
            self.current_cursor += 1 + len(self.selected_word)
            if self.current_cursor >= self.columns:
                self.current_cursor = self.columns - 1
                return
        log("2 current_cursor = {}".format(self.current_cursor))
        self.refresh()

    def move_to_prev_word(self):
        if self.current_cursor == 0:
            return
        else:
            self.current_cursor -= 1
            if self.current_cursor < 0:
                self.current_cursor = 0
            self.refresh()


    def handle_key(self, char):
        if char == "n": # move one line down
            self.move_to_next_line()
        elif char == "p": # move one line up
            self.move_to_prev_line()
        elif char == "f": # move to next word
            self.move_to_next_word()
        elif char == "b": # move to previsous word
            self.move_to_prev_word()
        elif char == "[": # page up
            return
        elif char == "]": # page down
            return

    
