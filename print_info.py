from fitz import fitz
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
            image_metadata = {
                'width': base_image['width'],
                'height': base_image['height'],
                'colorspace': base_image['colorspace'],
                'bpc': base_image['bpc'],  # Bits per component
                'format': base_image['ext'],  # 이미지 포맷 (예: 'png')
            }

            # 메타데이터 정보를 포함한 이미지 정보를 리스트에 추가
            images_info.append({
                'page_number': page_num,
                'image_index': image_index,
                'metadata': image_metadata
            })

    doc.close()
    return images_info
