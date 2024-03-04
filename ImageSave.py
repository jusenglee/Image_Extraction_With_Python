import fitz  # PyMuPDF
from PIL import Image
import io
import utility
import print_info


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
            current_image_metadata = {'page_num': page_num, 'colorspace': base_image['colorspace'],
                                      'width': base_image['width'], 'height': base_image['height'],
                                      'bpc': base_image['bpc']}

            current_image = Image.open(io.BytesIO(image_bytes))

            if last_image_metadata and last_image_metadata['page_num'] == current_image_metadata['page_num'] and \
                    last_image_metadata['colorspace'] == current_image_metadata['colorspace'] and last_image_metadata[
                'width'] == current_image_metadata['width']:
                #   분할된 이미지라 판정
                images_col.append(current_image)
            # 이미지의 bpc와 colorspace를 확인합니다.
            elif current_image_metadata['colorspace'] == 1 and current_image_metadata['bpc'] == 1:
                # bpc와 colorspace가 모두 1인 경우 재귀
                continue
            else:
                if len(images_col) > 1:
                    # 분할된 여러 이미지를 병합하는 경우
                    utility.save_image(utility.merge_images(images_col),page_num,image_index)
                elif images_col:
                    # 단일 이미지를 저장하는 경우
                    utility.save_image(images_col[0],page_num,image_index)

                images_col = [current_image]  # 현재 이미지로 새 리스트를 시작합니다.
                last_image_metadata = current_image_metadata

    if len(images_col) > 1:
        # 문서의 마지막에 여러 이미지가 남아있는 경우 병합
        utility.save_image(utility.merge_images(images_col),page_num,image_index)
    elif images_col:
        # 문서의 마지막에 단일 이미지가 남아있는 경우 저장
        utility.save_image(images_col[0],page_num,image_index)
    doc.close()


if __name__ == "__main__":
    pdf_path = "C:\\Users\\fpdls\\Downloads\\SOOOB6_2023_v26n6_2_1145.pdf"
    extract_images_from_pdf(pdf_path)
    # print(print_info.info(pdf_path))
