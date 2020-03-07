#!/usr/bin/python3

import curses
from curses.textpad import Textbox, rectangle
import loader

log_file = None
def log(message):
    log_file.write(str(message))
    log_file.write('\n')

class WindowsManager(object):
    def __init__ (self, windows_list=[]):
        self.current_window = -1
        self.windows_list = []
        for window in windows_list:
            self.append_window()

    def append_window(self, window, default=False):
        self.windows_list.append(window)
        if len(self.windows_list) == 1:
            self.current_window = 0
            self.windows_list[self.current_window].set_focus()

        if default:
            self.windows_list[self.current_window].set_nonfocus()
            self.current_window = len(self.windows_list) - 1
            self.windows_list[self.current_window].set_focus()

    def current_window(self):
        return self.windows_list[self.current_window]

    def switch_window(self):
        log("current window = {}".format(self.current_window))
        self.windows_list[self.current_window].set_nonfocus()
        self.current_window += 1
        if self.current_window == len(self.windows_list):
            self.current_window = 0
        log("next window = {}".format(self.current_window))
        self.windows_list[self.current_window].set_focus()

    
class Window(object):
    def __init__ (self, main_window, y, x, h, w, title="UNTITLED"):
        self.win = curses.newwin(h, w, y, x)
        # self.win.border()
        self.win.hline(0, 0, '-', w)
        self.columns = w
        self.lines = h - 1
        self.title = title
        self.focused = False
        self.set_title(title)
        
    def set_title(self, title):
        self.title = title
        if self.focused:
            self.set_focus()
        else:
            self.set_nonfocus()
        self.refresh()

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


    def break_text(self, text, limit):
        text_list = []
        num_lines = (len(text) + limit - 1) // limit
        for i in range(0, num_lines):
            start = i * limit
            if (i+1)*limit > len(text):
                line = text[i*limit :]
            else:
                line = text[i*limit : (i+1)*limit]
            text_list.append(line)
        return text_list


    def display(self, title, text_lines):
        '''
        This function breaks the text lines into display lines according to display columns and show the text.
        text_lines: List of a tuple, each tuple contains a tag (usually index) and a line of text.
        '''
        self.set_title(title)

        # display_lines is a list of tuple, each tuple contains a tag and a list
        display_blocks = []
        tag = 0
        for text_line in text_lines:
            tag += 1
            display_blocks.append((tag, self.break_text(text_line, self.columns-5)))

        # build display buffer,
        display_buffer = []
        for block in display_blocks:
            head = "{:0>3d}. ".format(block[0])
            for line in block[1]:
                display_line = "{}{}".format(head, line)
                display_buffer.append(display_line)
                head = "     "

        # render the display area
        start_index = 0
        for i in range(self.lines-1):
            if (start_index + i) >= len(display_buffer):
                break
            self.win.addstr(i+1, 0, display_buffer[start_index + i])
        

def create_title(main_window, title):
    title_len = len(title) + 4
    screen_height, screen_width = main_window.getmaxyx()
    bar_length = (screen_width - title_len) // 2
    main_window.hline(0, 0, curses.ACS_HLINE, bar_length)
    main_window.addstr(0, bar_length + 2, title , curses.A_REVERSE)
    main_window.hline(0, bar_length + title_len, curses.ACS_HLINE, screen_width - bar_length - title_len)
    main_window.refresh()

def setup_frames(main_window):
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
    
    tl = Window(main_window, da[0], da[1], tl_height, tl_width, "Books")
    tl.refresh()
    tr = Window(main_window, da[0], da[1] + tl_width, tl_height, da[3] - tl_width, "Text")
    tr.refresh()
    bl = Window(main_window, da[0] + tl_height, da[1], da[2] - tl_height, bl_width, "Dictionary")
    bl.refresh()
    br = Window(main_window, da[0] + tl_height, da[1] + bl_width, da[2] - tl_height, da[3] - bl_width, "Comments")
    br.refresh()
    return tl, tr, bl, br


def main(main_window):
    curses.curs_set(0)
    # Load text
    bible = loader.load_bible("NIV")
    
    # Clear screen
    main_window.clear()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLUE)

    create_title(main_window, "BitBible")
    tl, tr, bl, br = setup_frames(main_window)

    wm = WindowsManager()
    wm.append_window(tl)
    wm.append_window(tr, True)
    wm.append_window(bl)
    wm.append_window(br)

    tr.display("Genesis 1", bible["Gen"][0])
    
    tr.refresh()

    main_window.refresh()

    while True:
        ch = main_window.getch()
        if ch in range(1, 27):
            char = chr(ch+96)
            log("control + {}".format(char))
            if char == "x": # exit
                return
            elif char == "o": # switch window
                wm.switch_window()
            else:
                continue
        else:
            char = chr(ch)
            if char  == "q": # q also works to exit
                return
            else:
                continue
            


log_file = open("debug.log", "wt")

curses.wrapper(main)

log_file.close()
