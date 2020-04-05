import curses
from window import Window
from log import *
import os

class CommentaryWindow(Window):
    def __init__ (self, main_window, y, x, h, w, title="UNTITLED"):
        super(CommentaryWindow, self).__init__(main_window, y, x, h, w, title)


    def Xload(self, text_lines):
        for i in range(len(text_lines)):
            if i == self.height-2:
                return
            self.win.addstr(i+1, 0, text_lines[i])
            self.win.addstr(i+1, len(text_lines[i]), " " * (self.columns-1 - len(text_lines[i])))
        for i in range(len(text_lines), self.height - 1):
            self.win.addstr(i+1, 0, " " * (self.columns-1))

    def comment(self, verse_id):
        # verse_id in format (book_short_name, chapter, verse)
        text = ["Commentary not found."]
        book_short_name, chapter, verse = verse_id
        filename = "../commentary/MHCC/markdown/" + book_short_name + ".md"
        if os.path.exists(filename):
            buff = open(filename, "rt").read().split('\n')
            for line in buff:
                if line.startswith(chapter + "." + verse + " "):
                    text = line[line.find(" ")+1:]
                    text = self.break_text(text, self.columns-1)
        self.load(text)
        self.refresh()

    def handle_key(self, char):
        super(CommentaryWindow, self).handle_key(char)


    
