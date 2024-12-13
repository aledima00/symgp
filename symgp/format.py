from colorama import Fore, Back, Style

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
        self._fore = color
        self._text += color
        return self
    def back(self,color:str):
        self._text += color
        return self
    def style(self,style:str):
        self._text += style
        return self
    
    def __str__(self):
        return self._text+f"{Fore.RESET}{Back.RESET}{Style.RESET_ALL}"
    def __repr__(self):
        return str(self)