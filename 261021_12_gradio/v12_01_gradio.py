import gradio as gr

#1.간단한 함수 정의
def say_hello(name):
    return "Hello" + name
#2.Gradio 인터페이스 정의
gr_web=gr.Interface(
    fn=say_hello,       #실행할 함수
    inputs="text",       #텍스트 입력창
    outputs="text"      #텍스트 출력창
)

#3.웹 실행
gr_web.launch(share=True)   #웹배포까지 가능(시간제한,파이썬코드가 실행되는동안만)