import fitz  # PyMuPDF
from PIL import Image
import io

def extract_images_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    images_col = []  # 합칠 이미지를 저장하는 리스트
    last_image_metadata = None

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        for image_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            current_image_metadata = {
                'page_num': page_num,
                'colorspace': base_image['colorspace'],
                'width': base_image['width'],
                'height': base_image['height']
            }
            current_image = Image.open(io.BytesIO(image_bytes))

            if last_image_metadata and last_image_metadata['page_num'] == current_image_metadata['page_num'] and \
                    last_image_metadata['colorspace'] == current_image_metadata['colorspace'] and \
                    last_image_metadata['width'] == current_image_metadata['width']:
                images_col.append(current_image)
            else:
                if len(images_col) > 1:
                    # 여러 이미지를 병합하는 경우
                    merged_image = merge_images(images_col)
                    merged_filename = f"merged_page_{page_num}_image_{image_index}.png"
                    merged_image.save(merged_filename)
                elif images_col:
                    # 단일 이미지를 저장하는 경우
                    single_image = images_col[0]
                    single_filename = f"page_{page_num}_image_{image_index}.png"
                    single_image.save(single_filename)
                images_col = [current_image]  # 현재 이미지로 새 리스트를 시작합니다.
                last_image_metadata = current_image_metadata

    if len(images_col) > 1:
        # 문서의 마지막에 여러 이미지가 남아있는 경우 병합
        merged_image = merge_images(images_col)
        merged_filename = "merged_final.png"
        merged_image.save(merged_filename)
    elif images_col:
        # 문서의 마지막에 단일 이미지가 남아있는 경우 저장
        single_image = images_col[0]
        single_filename = "final_image.png"
        single_image.save(single_filename)

    doc.close()

def merge_images(images):
    total_width = images[0].width
    max_height = sum(image.height for image in images)
    merged_image = Image.new('RGB', (total_width, max_height))

    y_offset = 0
    for image in images:
        merged_image.paste(image, (0, y_offset))
        y_offset += image.height

    return merged_image

if __name__ == "__main__":
    pdf_path = "C:\\Users\\fpdls\\Downloads\\GJMGCK_2023_v9n6_1081.pdf"
    extract_images_from_pdf(pdf_path)
