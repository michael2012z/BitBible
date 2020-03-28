#!/usr/bin/python3

import curses
from curses.textpad import Textbox, rectangle
from window import Window
from text_window import TextWindow
from books_window import BooksWindow
from windows_manager import WindowsManager
from dictionary_window import DictionaryWindow
from log import *
from messenger import Messenger

class Reader():

    def create_title(self, main_window, title):
        title_len = len(title) + 4
        screen_height, screen_width = main_window.getmaxyx()
        bar_length = (screen_width - title_len) // 2
        main_window.hline(0, 0, curses.ACS_HLINE, bar_length)
        main_window.addstr(0, bar_length + 2, title , curses.A_REVERSE)
        main_window.hline(0, bar_length + title_len, curses.ACS_HLINE, screen_width - bar_length - title_len)
        main_window.refresh()

    def setup_frames(self, main_window):
        '''
        Divide the display region into 4 areas:
        tl | tr
        +++++++
        bl | br
        '''
        screen_height, screen_width = main_window.getmaxyx()
        display_area = (1, 0, screen_height-1, screen_width)
        da = display_area
        tl_width = da[3] // 4
        tl_height = da[2] * 2 // 3
        bl_width = da[3] // 3

        main_window.hline(da[0] + tl_height - 1, da[1], 0, da[3])
        main_window.vline(da[0], tl_width - 1, 0, tl_height-1)
        main_window.vline(tl_height+1, bl_width - 1, 0, da[2] - tl_height)

        tl = BooksWindow(main_window, da[0], da[1], tl_height, tl_width, "Books")
        tl.refresh()
        tr = TextWindow(main_window, da[0], da[1] + tl_width, tl_height, da[3] - tl_width, "Text")
        tr.refresh()
        bl = DictionaryWindow(main_window, da[0] + tl_height, da[1], da[2] - tl_height, bl_width, "Dictionary")
        bl.refresh()
        br = Window(main_window, da[0] + tl_height, da[1] + bl_width, da[2] - tl_height, da[3] - bl_width, "Comments")
        br.refresh()

        return tl, tr, bl, br
    
    
    def main(self, main_window):
        curses.curs_set(0)
    
        # Clear screen
        main_window.clear()
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLUE)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_GREEN)
        
        self.create_title(main_window, "BitBible")

        tl, tr, bl, br = self.setup_frames(main_window)

        msgr = Messenger()
        tl.set_messenger(msgr)
        tr.set_messenger(msgr)
        bl.set_messenger(msgr)
        br.set_messenger(msgr)
        msgr.register_windows(tl, tr, bl, br)
        
        wm = WindowsManager()
        wm.append_window(tl)
        wm.append_window(tr, True)
        wm.append_window(bl)
        wm.append_window(br)
        tr.notify("text_window_ready", 0)

        main_window.refresh()

        while True:
            ch = main_window.getch()
            if ch in range(1, 27):
                char = chr(ch+96)
                log("control + {}".format(char))
                if char == "x": # exit
                    return
                else:
                    wm.handle_key(char)
            else:
                char = chr(ch)
                if char  == "q": # q also works to exit
                    return
                else:
                    continue
            

if __name__ == '__main__':
    log("============= BitBible reader started ==============", True)
    reader = Reader()
    curses.wrapper(reader.main)


