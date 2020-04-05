import os
import curses
from window import Window
from log import *
import xml.etree.ElementTree as ET
import nltk
from nltk.stem import WordNetLemmatizer
import threading

class DictionaryWindow(Window):
    def __init__ (self, main_window, y, x, h, w, title="UNTITLED"):
        self.word = ""
        self.wordnet_lemmatizer = WordNetLemmatizer()
        # nltk.pos_tag(["early"])
        # self.wordnet_lemmatizer.lemmatize("early", 'v')
        super(DictionaryWindow, self).__init__(main_window, y, x, h, w, title)
        self.help_text = [
                          " Key settings:"
                          "   Ctl + o: switch window",
                          "   Ctl + i: switch window (inversely)",
                          "   Ctl + n: to next line",
                          "   Ctl + p: to preview line",
                          "   Ctl + f: to next word",
                          "   Ctl + b: to preview word",
                          "   Ctl + e: enter",
                          ]
        self.translate(self.word)

    def load(self, text_lines):
        super(DictionaryWindow, self).load(text_lines)
            
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


    def format_explanation(self, explanation):
        # explanation format: (word, pron, freq, defi, ety, family, examples, hints)
        text = []
        if explanation == None:
            return text
        # definition
        if explanation[3] != None and len(explanation[3]) > 0:
            text.append(explanation[3])
        # hints
        if explanation[7] != None and len(explanation[7]) > 0:
            text.append("[Definition]")
            for hint in explanation[7]:
                text.append(" - " + hint[0] + ": " + hint[1])
        # family
        if explanation[5] != None and len(explanation[5]) > 0:
            text.append("[Family]")
            text.append(explanation[5])
        # examples
        if explanation[6] != None and len(explanation[6]) > 0:
            text.append("[Examples]")
            for example in explanation[6]:
                text.append(" - " + example)
        # etymology
        if explanation[4] != None and len(explanation[4]) > 0:
            text.append("[Etymology]")
            text.append(explanation[4])
        return text
        
    def translate(self, word):
        text_lines = []
        word = word.strip()
        if len(word) == 0:
            self.word = ""
            self.load(self.help_text)
            self.set_title("Help")
            #self.refresh()
            return
            
        self.word = self.get_alpha(word)
        #if self.word.istitle() and self.is_name(self.word) != True:
        #    self.word = self.word.lower()
        self.word = self.word.lower()
        if nltk.pos_tag([self.word])[0][1][0] == 'V':
            self.word = self.wordnet_lemmatizer.lemmatize(self.word, 'v')
        else:
            self.word = self.wordnet_lemmatizer.lemmatize(self.word)
        # load explanation
        explanation = self.load_word(self.word)
        defi_block = []
        freq = 0
        if explanation != None:
            expla_text = self.format_explanation(explanation)
            freq = int(explanation[2])
            if len(expla_text) > 0:
                for line in expla_text:
                    defi_block += self.break_text(line, self.columns-1)

        # first line: #######wrod####...###***###### (# stands for space, * is frequency)
        first_line_head = " " * 6 + self.word
        first_line_tail = "*" * freq +  " " * 6
        paddings = (self.columns - 1 - len(first_line_head) - len(first_line_tail))
        first_line = first_line_head + " " * paddings + first_line_tail
        text_lines = [first_line] + defi_block
        self.load(text_lines)
        self.set_title("Dictionary")
        #self.refresh()


    def load_word(self, word):
        file_name = "../dictionary/dictionary/" + word[0].upper() + "/" + word + ".xml"
        if word[0].isalpha()== False or not os.path.exists(file_name):
            return None
        
        tree = ET.parse(file_name)
        word_data = tree.getroot()[0]
        word = ""
        pron = ""
        freq = 0
        defi = ""
        ety = ""
        family = ""
        examples = []
        hints = []
        for attr in word_data:
            if attr.tag == 'word':
                word = attr.text
            elif attr.tag == 'pron':
                pron = attr.text
            elif attr.tag == 'freq':
                freq = attr.text
            elif attr.tag == 'def':
                defi = attr.text
            elif attr.tag == 'family':
                family = attr.text
            elif attr.tag == 'examples':
                for example in attr:
                    examples.append(example.text)
            elif attr.tag == 'hints':
                for hint in attr:
                    p = ""
                    m = ""
                    for i in hint:
                        if i.tag == 'property':
                            p = i.text
                        else:
                            m = i.text
                    hints.append((p, m))
        word_item = (word, pron, freq, defi, ety, family, examples, hints)
        return word_item

        
    def handle_key(self, char):
        super(DictionaryWindow, self).handle_key(char)
    

    def is_name(self, word):
        name_list = ["God", "He"]
        if word in name_list:
            return True
        else:
            return False
        
