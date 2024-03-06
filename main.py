import crawling

if __name__ == "__main__":
    url = 'https://scienceon.kisti.re.kr/main/mainForm.do'  # 이미지를 다운로드할 웹페이지의 URL
    folder_name = 'd:\\dataSet\\'  # 이미지를 저장
    crawling.data_set(url)
