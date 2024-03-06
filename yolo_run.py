import torch
from matplotlib import pyplot as plt
from PIL import Image

# 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'custom', path='\\runs\\train\\exp10\\weights\\last.pt', force_reload=True)

# 이미지 로드 및 탐지 수행
img = 'PDF_Image\\page_3.png'  # 테스트할 이미지 경로
results = model(img)

# 결과 표시
results.print()  # 탐지된 객체의 정보를 콘솔에 출력
results.show()  # 탐지 이미지를 보여줌
