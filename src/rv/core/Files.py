from __future__ import annotations
from typing import List, Set
from pathlib import Path
from pygments import highlight
from pygments.lexers import get_lexer_for_filename, TextLexer
from pygments.formatters import Terminal256Formatter
from pygments.token import Token
from difflib import SequenceMatcher

from rv.core.utils import get_number_of_digits, get_indentation, is_blank_line

class File:
    def __init__(self, input_name : str):
        self.buffer = ""
        self.filename = None
        self.lexer = None
        self.highlighted_buffer = ""
        self.lines = None
        self.highlighted_lines = None
        self.number_of_highlighted_lines = 0
        self.number_of_lines = 0
        self.max_number_of_digits = 0
        self.line_breaks = None


        if not self.load(input_name):      
            paths = Path(".").rglob("*")
            max_similarity = 0
            target_file = None
            for path in paths:
                if path.is_file():
                    similarity = SequenceMatcher(None,input_name,path.name).ratio()
                    if similarity > max_similarity:
                        max_similarity = similarity 
                        target_file = path

            self.load(target_file)

    def load(self,filename : str) -> bool:
        if Path(filename).is_file():
            self.filename = filename
            try:
                self.lexer = get_lexer_for_filename(filename)
            except:
                self.lexer = TextLexer()
            with open(filename,"r") as f:
                self.buffer = f.read()

            self.highlighted_buffer = highlight(self.buffer,self.lexer,Terminal256Formatter(style="gruvbox-dark"))
            self.lines = self.buffer.split("\n")
            self.highlighted_lines = self.highlighted_buffer.split("\n")
            self.number_of_lines = len(self.lines)
            self.number_of_highlighted_lines = len(self.highlighted_lines)
            self.max_number_of_digits = get_number_of_digits(self.number_of_highlighted_lines)

            for i in range(self.number_of_highlighted_lines):
                self.highlighted_lines[i] = f'{i+1}{" "*(self.max_number_of_digits-get_number_of_digits(i+1))} ~ {self.highlighted_lines[i]}'
                self.highlighted_buffer = "\n".join(self.highlighted_lines)

            self.line_breaks = [i for i, char in enumerate(self.buffer) if char == '\n']          
            return True
        else:
            return False

    def find_fragment(self, text : str, treshold : float = 0.10 ):
        # get_indentation()
        # max_similarity = 0
        target_line_index = None
        for i in range(len(self.lines)):
            if text in self.lines[i].lower():
                target_line_index = i
                break
            # similarity = SequenceMatcher(None,text,self.lines[i]).ratio()
            # if similarity > max_similarity:
            #     max_similarity = similarity
            #     target_line_index = i

        if target_line_index == None:
            return None

        return Fragment(self, target_line_index)

    def get_line_number_of_char_index(self,char_index : int):
        # Count how many newlines happened BEFORE this character index
        # Add 1 because line numbers are 1-indexed
        return sum(1 for break_pos in self.line_breaks if break_pos < char_index) 

    def get_functions(self) -> Set[str]:
       return set([(value,self.get_line_number_of_char_index(index)) for index, token_type, value in self.lexer.get_tokens_unprocessed(self.buffer) if token_type in Token.Name.Function])


class Fragment:
    def __init__(self, file, baseline : int):
        self.file = file
        self.baseline = baseline
        self._highlighted_buffer = None
        self._buffer = None
        self.firstline = baseline
        self.lastline = baseline
        self.expand()

    @property
    def buffer(self) -> str:
        if self._buffer == None:
            self._buffer = "\n".join(self.file.lines[self.firstline:self.lastline])

        return self._buffer

    @property
    def highlighted_buffer(self) -> str:
        if self._highlighted_buffer == None:
            self._highlighted_buffer = "\n".join(self.file.highlighted_lines[self.firstline:self.lastline])

        return self._highlighted_buffer

    def expand(self) -> None:
        base_indentation = get_indentation(self.file.lines[self.baseline])
        
        index = self.baseline-1
        stop = False
        while index >= 0 and not stop:
            self.firstline -= 1
            indentation = get_indentation(self.file.lines[index])

            if is_blank_line(self.file.lines[index]):
                if index-1 >= 0 and get_indentation(self.file.lines[index-1]) <= base_indentation:
                    stop = True
                
            stop = stop or indentation < base_indentation
            index -= 1

        index = self.baseline+1
        stop = False
        while index < self.file.number_of_lines and not stop:
            self.lastline += 1
            indentation = get_indentation(self.file.lines[index])

            if is_blank_line(self.file.lines[index]):
                if index+1 < self.file.number_of_lines and get_indentation(self.file.lines[index+1]) <= base_indentation:
                    stop = True
                
            stop = stop or indentation != 0 and indentation < base_indentation
            index += 1