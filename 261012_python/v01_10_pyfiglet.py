import pyfiglet
from termcolor import colored

#구현 pyfiglet + colored를 적용한 sentence 출력
py_text=pyfiglet.figlet_format("Hello, World!")
color_text=colored(py_text,"light_yellow")
print(color_text)

py_text2=pyfiglet.figlet_format("Wellcome")
color_text2=colored(py_text2,"magenta")
print(color_text2)

#  _   _      _ _         __        __         _     _ _ 
# | | | | ___| | | ___    \ \      / /__  _ __| | __| | |
# | |_| |/ _ \ | |/ _ \    \ \ /\ / / _ \| '__| |/ _` | |
# |  _  |  __/ | | (_) |    \ V  V / (_) | |  | | (_| |_|
# |_| |_|\___|_|_|\___( )    \_/\_/ \___/|_|  |_|\__,_(_)
#                     |/                                 
