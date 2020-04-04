import curses
from log import *
from messenger import Messenger

class Window(object):
    def __init__ (self, main_window, y, x, h, w, title="UNTITLED", show_highlight=False):
        self.win = curses.newwin(h, w, y, x)
        # self.win.border()
        self.win.hline(0, 0, '-', w)
        self.columns = w - 1
        self.height = h - 2
        self.title = title
        self.focused = False
        self.msgr = None
        self.show_highlight = show_highlight
        self.display_buffer = []
        # display buffer's upper boundary in window
        self.buffer_upper_line = 0
        # display buffer's lower boundary in window
        # note: it is the next line to the last
        #       displayed line
        self.buffer_lower_line = 0
        # highlighted line of the window
        # note: this is not a line in display buffer
        self.current_line = 0

        self.set_title(title)
        

    def set_messenger(self, msgr):
        self.msgr = msgr

    def notify(self, msg, data):
        self.msgr.notify(msg, data)
        
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

        
    def print_line(self, line_num, text, highlighted = False):
        self.win.addstr(line_num, 0, text)
        if self.columns > len(text):
            self.win.addstr(line_num, len(text), ' ' * (self.columns - len(text)))
            
    def refresh(self):
        for i in range(self.height):
            if (i + self.buffer_upper_line) < self.buffer_lower_line:
                self.print_line(i+1, self.display_buffer[self.buffer_upper_line + i])
            else:
                self.print_line(i+1, " " * (self.columns-1))
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

    def load(self, text_lines):
        self.display_buffer = text_lines
        # set the display boundaries
        self.buffer_upper_line = 0
        self.buffer_lower_line = self.height
        if self.buffer_lower_line > len(self.display_buffer):
           self.buffer_lower_line = len(self.display_buffer)

        
    def move_to_next_line(self):
        # Simulate the senario that highlight is at the end of the screen
        log("move_to_next_line: 1 self.current_line = {}, self.buffer_lower_line = {}, self.buffer_upper_line".format(self.current_line, self.buffer_lower_line, self.buffer_upper_line))    
        if self.show_highlight == False:
            self.current_line = self.buffer_lower_line - 1 - self.buffer_upper_line

        if self.current_line + self.buffer_upper_line < self.buffer_lower_line - 1:
            # highlighted line in middle 
            self.current_line += 1
            log("move_to_next_line: 2 self.current_line = {}, self.buffer_lower_line = {}, self.buffer_upper_line".format(self.current_line, self.buffer_lower_line, self.buffer_upper_line))    
        else: # lighlighted line on lower boundary
            if self.buffer_lower_line == len(self.display_buffer):
                # lower boundary is in the middle of screen, no move
                log("move_to_next_line: 3 self.current_line = {}, self.buffer_lower_line = {}, self.buffer_upper_line".format(self.current_line, self.buffer_lower_line, self.buffer_upper_line))    

                return
            else:
                # move page one line down
                self.buffer_upper_line += 1
                self.buffer_lower_line += 1
                log("move_to_next_line: 4 self.current_line = {}, self.buffer_lower_line = {}, self.buffer_upper_line".format(self.current_line, self.buffer_lower_line, self.buffer_upper_line))    

        self.refresh()
                
    def move_to_prev_line(self):
        # Simulate the senario that highlight is at the end of the screen
        if self.show_highlight == False:
            self.current_line = 0
        
        if self.current_line == 0:
            if self.buffer_upper_line == 0:
                return
            else:
                self.buffer_upper_line -= 1
                self.buffer_lower_line -= 1
        else:
            self.current_line -= 1
        self.refresh()


    def handle_key(self, char):
        if char == "n": # move one line down
            self.move_to_next_line()
        elif char == "p": # move one line up
            self.move_to_prev_line()

