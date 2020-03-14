import curses
from log import *

class Window(object):
    def __init__ (self, main_window, y, x, h, w, title="UNTITLED"):
        self.win = curses.newwin(h, w, y, x)
        # self.win.border()
        self.win.hline(0, 0, '-', w)
        self.columns = w
        self.height = h - 1
        self.title = title
        self.focused = False
        self.set_title(title)
        
    def set_title(self, title):
        self.title = title
        if self.focused:
            self.set_focus()
        else:
            self.set_nonfocus()

    def set_focus(self):
        self.focused = True
        self.win.addstr(0, 2, '> ' + self.title + ' <', curses.color_pair(2))
        self.refresh()
        
    def set_nonfocus(self):
        self.focused = False
        self.win.addstr(0, 2, '> ' + self.title + ' <', curses.color_pair(1))
        self.refresh()

    def refresh(self):
        self.win.refresh()


    def break_text(self, text, width):
        words = text.split()
        lines = []
        line = ""
        for word in words:
            if len(line) + 1 + len(word) > width:
                line = " ".join([line, ' ' * (width - len(line))])
                lines.append(line)
                line = ""
            line = " ".join([line, word])
            line = line.strip()
        if len(line) > 0:
            lines.append(line)

        return lines

    def load(self, title, text_lines):
        pass

    def handle_key(self, char):
        pass
