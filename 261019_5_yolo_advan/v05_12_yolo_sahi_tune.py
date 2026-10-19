from sahi.predict import get_sliced_prediction
from sahi import AutoDetectionModel

#1.모델 경로
model_path="yolo11n.pt"
#2. 모델 로드
detection_model=AutoDetectionModel.from_pretrained(
    model_type="ultralytics",
    model_path=model_path,
    confidence_threshold=0.4#신뢰도 0.4이상 탐지하겠다.
)
#3. SAHI 적용
results=get_sliced_prediction(
    "261019_5_yolo_advan/pexels-jakub-samberger-2079109211-33361905.jpg",
    detection_model,
    slice_height=200,
    slice_width=200,
    overlap_height_ratio=0.1,
    overlap_width_ratio=0.1
)
#4. 결과 저장
results.export_visuals(export_dir="sahi/", file_name="my_result2")


#5.탐지 출력 로그
print("모든 코드가 성공적으로 수행됐습니다.")