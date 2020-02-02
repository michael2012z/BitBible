import curses
from curses.textpad import Textbox, rectangle

class Window(object):
    def __init__ (self, main_window, y, x, h, w, title):
        self.win = curses.newwin(h, w, y, x)
        # self.win.border()
        self.win.hline(0, 0, '-', w)
        self.win.addstr(0, 2, '> ' + title + ' <', curses.color_pair(1))

        
    def refresh(self):
        self.win.refresh()
        

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
    bl = Window(main_window, da[0] + tl_height, da[1], da[2] - tl_height, bl_width, "Translate")
    bl.refresh()
    br = Window(main_window, da[0] + tl_height, da[1] + bl_width, da[2] - tl_height, da[3] - bl_width, "Comments")
    br.refresh()
    return tl, tr, bl, br
    
    
def main(main_window):
    # Clear screen
    main_window.clear()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_WHITE)

    create_title(main_window, "BitBible")
    setup_frames(main_window)

    main_window.refresh()
    main_window.getkey()

    
curses.wrapper(main)
