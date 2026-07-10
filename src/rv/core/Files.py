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

            self.highlighted_buffer = highlight(self.buffer,self.lexer,Terminal256Formatter(style="monokai"))
            self.lines = self.buffer.split("\n")
            self.highlighted_lines = self.highlighted_buffer.split("\n")
            self.number_of_lines = len(self.lines)
            self.max_number_of_digits = get_number_of_digits(self.number_of_lines)

            for i in range(self.number_of_lines):
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
            if text in self.lines[i]:
                target_line_index = i
                break
            # similarity = SequenceMatcher(None,text,self.lines[i]).ratio()
            # if similarity > max_similarity:
            #     max_similarity = similarity
            #     target_line_index = i

        if target_line_index == None:
            return ""
        fragment_buffer = self.highlighted_lines[target_line_index]

        target_indentation = get_indentation(self.lines[target_line_index])
        index = target_line_index-1
        stop = False
        while index >= 0 and not stop:
            fragment_buffer = f'{self.highlighted_lines[index]}\n{fragment_buffer}'
            indentation = get_indentation(self.lines[index])

            if is_blank_line(self.lines[index]):
                if index-1 >= 0 and get_indentation(self.lines[index-1]) <= target_indentation:
                    stop = True
                
            stop = stop or indentation < target_indentation
            index -= 1

        index = target_line_index+1
        stop = False
        while index < self.number_of_lines and not stop:
            fragment_buffer = f'{fragment_buffer}\n{self.highlighted_lines[index]}'
            indentation = get_indentation(self.lines[index])

            if is_blank_line(self.lines[index]):
                if index+1 < self.number_of_lines and get_indentation(self.lines[index+1]) <= target_indentation:
                    stop = True
                
            stop = stop or indentation != 0 and indentation < target_indentation
            index += 1

        return fragment_buffer

    def get_line_number_of_char_index(self,char_index : int):
        # Count how many newlines happened BEFORE this character index
        # Add 1 because line numbers are 1-indexed
        return sum(1 for break_pos in self.line_breaks if break_pos < char_index) 

    def get_functions(self) -> Set[str]:
       return set([(value,self.get_line_number_of_char_index(index)) for index, token_type, value in self.lexer.get_tokens_unprocessed(self.buffer) if token_type in Token.Name.Function])