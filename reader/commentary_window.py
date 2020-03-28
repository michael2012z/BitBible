import curses
from window import Window
from log import *


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
            self.win.addstr(i+1, 0, text_lines[i])
            self.win.addstr(i+1, len(text_lines[i]), " " * (self.columns-1 - len(text_lines[i])))
        for i in range(len(text_lines), self.height - 1):
            self.win.addstr(i+1, 0, " " * (self.columns-1))
            
    def handle_key(self, char):
        pass
    
