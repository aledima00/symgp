from colorama import Fore, Back, Style

_FORE_ALLOWED_VALUES =  [Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE, Fore.RESET]
_BACK_ALLOWED_VALUES =  [Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE, Back.RESET]
_STYLE_ALLOWED_VALUES = [Style.DIM, Style.NORMAL, Style.BRIGHT, Style.RESET_ALL]

class Formatted:
    _text:str
    _indentation:int
    _fore:str
    _back:str
    _style:str

    def __init__(self):
        self._style = Style.RESET_ALL
        self._fore = Fore.WHITE
        self._back = Back.BLACK
        self._indentation = 0
        self._text = f"{self._fore}{self._back}{self._style}"
    def indent(self,times:int=1):
        self._indentation += times
        return self
    def unindent(self,times:int=1):
        self._indentation -= times
        if self._indentation<0:
            self._indentation = 0
        return self
    def ret(self):
        self._text+=f"\n"+(f"\t"*self._indentation)
        return self
    def add(self, text:str):
        self._text += text
        return self
    def fore(self,color:str):
        assert color in _FORE_ALLOWED_VALUES, f"Invalid fore color: {color}"
        self._fore = color
        self._text += color
        return self
    def back(self,color:str):
        assert color in _BACK_ALLOWED_VALUES, f"Invalid back color: {color}"
        self._text += color
        return self
    def style(self,style:str):
        assert style in _STYLE_ALLOWED_VALUES, f"Invalid style: {style}"
        self._text += style
        return self
    
    def __str__(self):
        return self._text+f"{Fore.RESET}{Back.RESET}{Style.RESET_ALL}"
    def __repr__(self):
        return str(self)