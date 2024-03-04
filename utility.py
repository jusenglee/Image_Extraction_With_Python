from PIL import Image
import os

def save_image(single_image, page_num, image_index):
    # 이미지를 저장할 기본 디렉토리 경로
    save_path = "C:\\Users\\fpdls\\Pictures\\Image\\"

    # 이미지 모드가 CMYK인 경우 JPEG로 저장
    if single_image.mode == "CMYK":
        single_filename = f"page_{page_num}_image_{image_index}.png"  # JPEG 확장자 사용
        full_path = os.path.join(save_path, single_filename)  # 전체 파일 경로 결합
        single_image = single_image.convert("RGB")  # RGB 모드로 변환
        single_image.save(full_path, "png")  # JPEG 형식으로 저장
    else:
        single_filename = f"page_{page_num}_image_{image_index}.png"  # PNG 확장자 사용
        full_path = os.path.join(save_path, single_filename)  # 전체 파일 경로 결합
        single_image.save(full_path)  # PNG 형식으로 저장

#   여러개 분할된 이미지 일 경우 병합 하는 함수
def merge_images(images):
    total_width = images[0].width
    max_height = sum(image.height for image in images)
    merged_image = Image.new('RGB', (total_width, max_height))

    y_offset = 0
    for image in images:
        merged_image.paste(image, (0, y_offset))
        y_offset += image.height

    return merged_image

