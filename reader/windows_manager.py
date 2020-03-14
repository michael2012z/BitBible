from log import *

'''
Windows Manager controls the order in loop when the user switch between
windows by typing ctl + o.
'''
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

    def get_current_window(self):
        return self.windows_list[self.current_window]

    def switch_window(self):
        log("current window = {}".format(self.current_window))
        self.windows_list[self.current_window].set_nonfocus()
        self.current_window += 1
        if self.current_window == len(self.windows_list):
            self.current_window = 0
        log("next window = {}".format(self.current_window))
        self.windows_list[self.current_window].set_focus()

    def handle_key(self, char):
        if char == "o": # switch window
            self.switch_window()
        else:
            self.get_current_window().handle_key(char)
