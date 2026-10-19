from ultralytics import solutions

#1.검색 앱 생성
app=solutions.SearchApp(
    device="cpu"
    # data="이미지 경로"
)
#2.웹 서버 실행
app.run(debug=True)