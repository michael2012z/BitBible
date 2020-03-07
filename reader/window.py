import curses

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
        
