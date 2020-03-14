import curses
from window import Window
from log import *

class DictionaryWindow(Window):
    def __init__ (self, main_window, y, x, h, w, title="UNTITLED"):
        self.word = ""
        super(DictionaryWindow, self).__init__(main_window, y, x, h, w, title)

    def get_alpha(self, word):
        s = -1
        e = len(word)
        for i in range(len(word)):
            c = word[i]
            if c.isalpha() and s == -1:
                s = i
            if (c.isalpha() == False) and (s != -1):
                e = i
                break
        return word[s:e]
                
    def translate(self, word):
        self.word = self.get_alpha(word)
        if self.word.istitle() and self.is_name(self.word) != True:
            self.word = self.word.lower()
        paddings = (self.columns - len(self.word)) // 2
        self.win.addstr(1, 0, " " * paddings)
        self.win.addstr(1, paddings, self.word, curses.color_pair(3))
        self.win.addstr(1, paddings + len(self.word), " " * (self.columns - paddings - len(self.word)))
        self.refresh()
        
    def handle_key(self, char):
        pass
    

    def is_name(self, word):
        name_list = ["God", "He"]
        if word in name_list:
            return True
        else:
            return False
        
