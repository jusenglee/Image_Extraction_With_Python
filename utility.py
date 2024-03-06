from PIL import Image
import os
from fitz import fitz


# PDF 내의 이미지들 메타데이터를 출력해보는 함수
def info(pdf_path):
    doc = fitz.open(pdf_path)
    images_info = []  # 추출된 이미지 및 메타데이터 정보를 저장할 리스트

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        for image_index, img in enumerate(page.get_images(full=True)):
            if image_index >= 10:  # 10번째 이후에 루프 종료
                break
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            # 이미지 메타데이터 추출
            image_metadata = {'width': base_image['width'], 'height': base_image['height'],
                'colorspace': base_image['colorspace'], 'bpc': base_image['bpc'],  # Bits per component
                'format': base_image['ext'],  # 이미지 포맷 (예: 'png')
            }

            # 메타데이터 정보를 포함한 이미지 정보를 리스트에 추가
            images_info.append({'page_number': page_num, 'image_index': image_index, 'metadata': image_metadata})

    doc.close()
    return images_info


#   pdf의 전체 페이지를 이미지로 변환하여 저장하는 함수
def convert_pdf_to_images(pdf_path, resolution=300):
    # PDF 문서 열기
    doc = fitz.open(pdf_path)
    image_paths = []

    # 문서의 모든 페이지를 순회
    for page_num in range(len(doc)):
        # 페이지 로드
        page = doc.load_page(page_num)
        # 지정된 해상도로 페이지의 이미지를 생성
        pix = page.get_pixmap(matrix=fitz.Matrix(resolution / 72, resolution / 72))
        image_bytes = pix.tobytes("png")
        image_path = f"page_{page_num}.png"
        # 이미지 파일로 저장
        with open(image_path, "wb") as img_file:
            img_file.write(image_bytes)
        image_paths.append(image_path)

    # 문서 닫기
    doc.close()

    # 생성된 이미지 파일들의 경로 반환
    return image_paths


#   이미지를 경로 지정하여 저장하는 함수
#   CMYK 일 경우 RGB 모드로 변환
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


#   폴더 내에 PDF 문서의 이름들을 변경해주는 함수
def rename_files_in_folder_with_extension(folder_path):
    files = os.listdir(folder_path)
    start_number = 1

    for file_name in files:
        old_file_path = os.path.join(folder_path, file_name)
        # 파일 이름과 확장자 분리
        _, extension = os.path.splitext(file_name)
        # 새 파일 이름에 확장자 추가
        new_file_name = f"{start_number}{extension}"
        new_file_path = os.path.join(folder_path, new_file_name)

        os.rename(old_file_path, new_file_path)
        start_number += 1
