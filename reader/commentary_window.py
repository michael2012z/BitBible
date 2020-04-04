import curses
from window import Window
from log import *
import os

class CommentaryWindow(Window):
    def __init__ (self, main_window, y, x, h, w, title="UNTITLED"):
        super(CommentaryWindow, self).__init__(main_window, y, x, h, w, title)
        text = [
                "...... " * 24, 
                "Commentary display is not yet ready.",
                "Commentary in OSIS format will be loaded, and update when the focus of the Text window changes.",
                "...... " * 24, 
                ]
        text_lines = []
        for t in text:
            text_lines += self.break_text(t, self.columns-1)
        self.load("Commentary", text_lines)


    def load(self, title, text_lines):
        for i in range(len(text_lines)):
            if i == self.height-2:
                return
            self.win.addstr(i+1, 0, text_lines[i])
            self.win.addstr(i+1, len(text_lines[i]), " " * (self.columns-1 - len(text_lines[i])))
        for i in range(len(text_lines), self.height - 1):
            self.win.addstr(i+1, 0, " " * (self.columns-1))

    def comment(self, verse_id):
        # verse_id in format (book_short_name, chapter, verse)
        text = "Commentary not found."
        book_short_name, chapter, verse = verse_id
        filename = "../commentary/MHCC/markdown/" + book_short_name + ".md"
        if os.path.exists(filename):
            buff = open(filename, "rt").read().split('\n')
            for line in buff:
                if line.startswith(chapter + "." + verse + " "):
                    text = line[line.find(" ")+1:]
                    text = self.break_text(text, self.columns-1)
        self.load("xxxxxxxx", text)
        self.refresh()

    def handle_key(self, char):
        pass
    
