import pyfiglet
# 함수화하기
# sentence="hello"
# py_sentence=pyfiglet.figlet_format(sentence)
# print(py_sentence)

def good_sentence(sentence: str):
    """ 
    입력된 문자를 pyfiglet 형식으로 출력
    """
    py_sentence=pyfiglet.figlet_format(sentence)
    print(py_sentence)
    
good_sentence("GOOD")