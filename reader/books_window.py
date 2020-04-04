import os
import curses
from window import Window
from log import *
import loader

class BooksWindow(Window):

    VIEW_INDEX_VERSION = 0
    VIEW_INDEX_BOOK    = 1
    VIEW_INDEX_CHAPTER = 2
    
    def __init__ (self, main_window, y, x, h, w, title="UNTITLED"):
        self.ready = False
        super(BooksWindow, self).__init__(main_window, y, x, h, w, title)
        log("books window height = {}".format(self.height))
        self.grid_columns = 3
        self.grid_cell_width = self.columns // self.grid_columns
        last_location = self.read_last_location()
        if last_location == None:
            self.grid_view_index = self.VIEW_INDEX_VERSION
            self.grid_view_data = [self.load_versions(),
                                {},
                                {}]
        else:
            self.grid_view_data = [self.load_versions(last_location[0]),
                                   self.load_books(last_location[0], last_location[1]),
                                   self.load_chapters(last_location[0], last_location[1], last_location[2])]
            self.grid_view_index = self.VIEW_INDEX_CHAPTER
            #self.chapters_callback()
        self.ready = True
        
        
    def refresh(self):
        if self.ready == False:
            return

        # flush blank screen
        for i in range(self.height):
            self.win.addstr(i+1, 0, " " * self.columns)
            
        data = self.grid_view_data[self.grid_view_index]
        for i in range(len(data["list"])):
            text = data["list"][i]
            s = ' ' * ((self.grid_cell_width - len(text)) // 2)
            s += text
            s += ' ' * (self.grid_cell_width - len(s))
            display_row = (i // self.grid_columns) + 1
            display_col = (i % self.grid_columns) * self.grid_cell_width
            log("row = {}, height = {}, col = {}, width = {}, s = {}".format(display_row, self.height, display_col, self.grid_cell_width, s))
            if display_row > self.height:
                break
            if i == data["selected"]:
                self.win.addstr( display_row, display_col, s, curses.color_pair(3))
            else:
                self.win.addstr( display_row, display_col, s)
            
        super(BooksWindow, self).refresh()

        
    def handle_key(self, char):
        data = self.grid_view_data[self.grid_view_index]
        list_len = len(data["list"])
        loc = data["selected"]
        if char == "n": # move one line down
            loc += self.grid_columns
            if loc > list_len-1:
                return
            else:
                data["selected"] = loc
        elif char == "p": # move one line up
            loc -= self.grid_columns
            if loc < 0:
                return
            else:
                data["selected"] = loc
        elif char == "f": # move to next word
            loc += 1
            if loc > list_len-1:
                return
            else:
                data["selected"] = loc
        elif char == "b": # move to previsous word
            loc -= 1
            if loc < 0:
                return
            else:
                data["selected"] = loc
        elif char == "e":
            data["callback"]()
        else:
            return

        self.refresh()
        

    def load_versions(self, selected="NIV"):
        versions = os.listdir("../markdown/")
        return {"name": "Versions",
                "list": versions,
                "callback": self.versions_callback,
                "selected": versions.index(selected)}

    def versions_callback(self):
        version_data = self.grid_view_data[self.VIEW_INDEX_VERSION]
        version = version_data["list"][version_data["selected"]]
        books = self.load_books(version)
        self.grid_view_data[self.VIEW_INDEX_BOOK] = books
        self.grid_view_index = self.VIEW_INDEX_BOOK
        self.set_title("Books: " + version)
        #self.refresh()

    def load_books(self, version, selected="Gen"):
        books = os.listdir("../markdown/" + version + "/files/")
        books = list(map(lambda x: x[:-3] , books))
        xbooks = ["-return-"]
        for book in books:
            xbooks.append(book)
        return {"name": version,
                "list": xbooks,
                "callback": self.books_callback,
                "selected": xbooks.index(selected)}

    def books_callback(self):
        version_data = self.grid_view_data[self.VIEW_INDEX_VERSION]
        version = version_data["list"][version_data["selected"]]
        book_data = self.grid_view_data[self.VIEW_INDEX_BOOK]
        book = book_data["list"][book_data["selected"]]
        if book == "-return-":
            self.grid_view_index = self.VIEW_INDEX_VERSION
            self.set_title("Books: " + version)
        else:
            chapters = self.load_chapters(version, book)
            self.grid_view_data[self.VIEW_INDEX_CHAPTER] = chapters
            self.grid_view_index = self.VIEW_INDEX_CHAPTER
            self.set_title("Books: " + version + "/" + book)
        #self.refresh()

    def load_chapters(self, version, book, selected=0):
        book_content = open("../markdown/" + version + "/files/" + book + ".md", "rt").read().split('\n')
        book_name = book
        if len(book_content) > 0:
            book_name = book_content[0][2:]
        chapter_list = list(range(len(list(filter(lambda x: x.startswith("## "), book_content)))))
        chapter_list = ['-return-'] + list(map(lambda x: str(x+1), chapter_list))
        return {"name": book_name,
                "shortname": book,
                "list": chapter_list,
                "callback": self.chapters_callback,
                "selected": selected}

    def chapters_callback(self):
        version_data = self.grid_view_data[self.VIEW_INDEX_VERSION]
        version = version_data["list"][version_data["selected"]]
        book_data = self.grid_view_data[self.VIEW_INDEX_BOOK]
        book = book_data["list"][book_data["selected"]]
        chapter_data = self.grid_view_data[self.VIEW_INDEX_CHAPTER]
        chapter = chapter_data["list"][chapter_data["selected"]]
        if chapter == "-return-":
            self.grid_view_index = self.VIEW_INDEX_BOOK
            self.set_title("Books: " + version)
            #self.refresh()
        else:
            bible = loader.load_bible(version)
            # long name, short name, chapter, text.
            self.notify("load_text", (chapter_data["name"], chapter_data["shortname"], chapter, bible[book][int(chapter)-1]))
            self.set_title("Books: " + version + "/" + book)
            self.write_last_location(version, book, chapter)


    def write_last_location(self, version, book, chapter):
        open(".last_location.txt", "wt").write(version + " " + book + " " + str(chapter))
        
    def read_last_location(self):
        if os.path.exists(".last_location.txt"):
            l = open(".last_location.txt", "rt").read().split()
            return (l[0], l[1], int(l[2]))
        else:
            return None
    
    def text_window_ready(self):
        if self.grid_view_index == self.VIEW_INDEX_CHAPTER:
            self.chapters_callback()
