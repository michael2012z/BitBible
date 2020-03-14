from log import *

class Messenger(object):
    def __init__ (self):
        self.b_win = None
        self.t_win = None
        self.d_win = None
        self.c_win = None
        

    def register_windows(self, books_win, text_win, dict_win, comments_win):
        self.b_win = books_win
        self.t_win = text_win
        self.d_win = dict_win
        self.c_win = comments_win

    def notify(self, msg, data):
        if msg == "translate":
            self.d_win.translate(data)
        elif msg == "show_comment":
            self.c_win.comment(data)
        else:
            log("unkown message type: {}".format(msg))
            
