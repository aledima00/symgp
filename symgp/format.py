from colorama import Fore, Back, Style
from typing import List as _List, Tuple as _Tuple

_FORE_ALLOWED_VALUES =  [Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE, Fore.RESET]
_BACK_ALLOWED_VALUES =  [Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE, Back.RESET]
_STYLE_ALLOWED_VALUES = [Style.DIM, Style.NORMAL, Style.BRIGHT, Style.RESET_ALL]

class Formatted:
    _lines:_List[_Tuple[int,str]]
    # each line is a tuple of (indentation:int, text_line:str)
    _fore:str
    _back:str
    _style:str

    def __init__(self):
        self._style = Style.RESET_ALL
        self._fore = Fore.WHITE
        self._back = Back.BLACK
        self._lines = [(0,"")]
    def indent(self,times:int=1):
        indt,text = self._lines[-1]
        indt += times
        self._lines[-1] = (indt, text)
        return self
    def unindent(self,times:int=1):
        indt, text = self._lines[-1]
        indt -= times
        if indt<0:
            indt = 0
        self._lines[-1] = (indt, text)
        return self
    def ret(self):
        indt = self._lines[-1][0]
        self._lines.append((indt, ""))
        return self
    def append(self, text:str):
        indt, line = self._lines[-1]
        line += text
        self._lines[-1] = (indt, line)
        return self
    def fore(self,color:str):
        assert color in _FORE_ALLOWED_VALUES, f"Invalid fore color: {color}"
        self._fore = color
        self.append(color)
        return self
    def back(self,color:str):
        assert color in _BACK_ALLOWED_VALUES, f"Invalid back color: {color}"
        self.back = color
        self.append(color)
        return self
    def style(self,style:str):
        assert style in _STYLE_ALLOWED_VALUES, f"Invalid style: {style}"
        self.style = style
        self.append(style)
        return self
    def concatenate(self,formatted:"Formatted",*,inline=True):
        base_indt,base_text = self._lines[-1]
        numlines = len(formatted._lines)
        for n in range(numlines):
            indt,text = formatted._lines[n]
            if n!=0 or (not inline):
                self._lines.append((base_indt+indt,text))
            else:
                self._lines[-1] = (base_indt+indt, base_text+text)
        self._fore = formatted._fore
        self._back = formatted._back
        self._style = formatted._style
        return self

    def __str__(self):
        delim = f"{Fore.RESET}{Back.RESET}{Style.RESET_ALL}"
        ret = ""
        for indt, text in self._lines:
            ret += f"\t"*indt + text + f"\n"
        return delim + ret + delim
    def __repr__(self):
        return str(self)