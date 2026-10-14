#여러분들만의 클래스 정의
#속성 3개 이상
#메서드 2개이상
#객체 2개 이상
#메서드 2개 호출

class crochet:
    #생성자
    def __init__(self, yarn, create, time):
        self.yarn=yarn
        self.create=create
        self.time=time
    #메서드 만들기
    def make_yarn(self, name):
        print(f"작품명 {name}:{self.yarn}실로 {self.create}작품을 만드는데에 {self.time}이 걸렸습니다.")
    def info(self):
        print(f"실: {self.yarn}, 작품: {self.create}, 걸린 시간: {self.time}")
#객체 생성
first=crochet("벨벳","키링","2시간")
second=crochet("모헤어","목도리","7시간")
first.make_yarn("피크민")
second.info()
    