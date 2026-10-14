import pyfiglet
from termcolor import colored

def make_highlight(text:str):
    """
    입력된 문자열을 pyfigle,termcolor를 이용해서 꾸며준다.
        매개변수 : test(str)
    """
    py_text=pyfiglet.figlet_format(text)
    color_py_text=colored(py_text, "magenta")
    return color_py_text

print(make_highlight("hello"))

#make_highlight함수를 터미넗에서 출력되게 해주세요.