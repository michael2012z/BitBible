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
        self.selected_word = ""
        self.displaying_book_short_name = ""
        self.displaying_chapter = ""
        # cursor location in current line, it's always the postion of
        # some word's first letter.
        # Valid value should be >= 5
        self.current_cursor = 0
        super(TextWindow, self).__init__(main_window, y, x, h, w, title, show_highlight=True)

        
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
        for i in range(self.height):
            if (i + self.buffer_upper_line) < self.buffer_lower_line:
                self.print_line(i+1, self.display_buffer[self.buffer_upper_line + i], i == self.current_line)
            else:
                # flush blank screen
                self.print_line(i+1, " " * self.columns)

        self.win.refresh()
    
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
        
    def load(self, data):
        '''
        This function breaks the text lines into display lines according to display columns and show the text.
        text_lines: List of a tuple, each tuple contains a tag (usually index) and a line of text.
        data:             # long name, short name, chapter, text.
        '''
        title = data[0]
        self.displaying_book_short_name = data[1]
        self.displaying_chapter = data[2]
        verses = data[3]
        self.set_title(title + " " + self.displaying_chapter)

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

        super(TextWindow, self).load(display_buffer)

        highlighted_verse = self.get_current_verse()
        self.notify("show_comment", (self.displaying_book_short_name, self.displaying_chapter, str(highlighted_verse)))

            
    def get_current_verse(self):
        lines = 0
        verse_index = 0
        for verse_meta_data in self.chapter_meta_data:
            verse_index += 1
            lines += len(verse_meta_data[1])
            if self.current_line + self.buffer_upper_line < lines:
                return verse_index
        return 0
            
    def move_to_next_word(self):
        if self.current_cursor == 0:
            self.current_cursor = 4
        else:
            self.current_cursor += 1 + len(self.selected_word)
            if self.current_cursor >= self.columns:
                self.current_cursor = self.columns - 1
                return
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
        old_verse = self.get_current_verse()
        super(TextWindow, self).handle_key(char)
        if char == "f": # move to next word
            self.move_to_next_word()
        elif char == "b": # move to previsous word
            self.move_to_prev_word()
        elif char == "[": # page up
            pass
        elif char == "]": # page down
            pass
        new_verse = self.get_current_verse()
        if new_verse != old_verse:
            self.notify("show_comment", (self.displaying_book_short_name, self.displaying_chapter, str(new_verse)))
        self.notify("translate", self.selected_word)
    
