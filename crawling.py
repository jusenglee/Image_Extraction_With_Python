from selenium.webdriver.common.keys import Keys
import time
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 크롬 드라이버 생성
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
# 검색어 리스트
search_list = ["심리"]  # 예시 검색어 추가
folder_name = ['d:\\dataSet\\심리\\']


#   이미지 다운로드 함수
def download_image(url, folder, image_count):
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = os.path.join(folder, f"image_{image_count}.jpg")
    with open(filename, "wb") as file:
        file.write(requests.get(url).content)
    print(f"다운로드 완료: {filename}")


# 이미지 탐색 함수
# 최대로 저장 가능한 이미지(기본값) 500
def find_and_download_images(folder, max_images=500):
    downloaded_images = 0
    while downloaded_images < max_images:
        # 현재 페이지에서 'objectfit' 클래스를 가진 이미지 요소들을 찾습니다.
        images = driver.find_elements(By.CLASS_NAME, "objectfit")
        # 이미지를 다운로드합니다.
        for image in images:
            if downloaded_images >= max_images:
                break  # 설정한 최대 이미지 개수에 도달하면 반복을 중단합니다.
            src = image.get_attribute("src")
            if src:
                download_image(src, folder, downloaded_images)
                downloaded_images += 1
        images = []  # 현재페이지의 이미지 다운로드가 끝나면 다음 페이지를 위해 Images를 비움
        click_next_page()


# 더 이상 탐색 할 이미지가 없을 경우 페이지 전환 함수(사이언스온 기준)
def click_next_page():
    # '다음 페이지' 버튼을 식별하기 위한 로직
    # 현재 활성화된 페이지 번호 바로 다음에 위치하는 버튼을 클릭하는 방식을 사용
    pagination_buttons = driver.find_elements(By.CSS_SELECTOR, "div.pagination button.num")
    current_page = int(driver.find_element(By.CSS_SELECTOR, "span.num.active").text)

    # 현재 페이지 번호 다음에 오는 버튼을 찾아 클릭
    for button in pagination_buttons:
        onclick_attr = button.get_attribute("onclick")
        if onclick_attr and f"fn_pageing({current_page + 1});" in onclick_attr:
            button.click()
            break


#   메인 함수
#   사이언스온 이미지 데이터 크롤링
def data_set(url):
    driver.get(url)
    index = 0
    for search_query in search_list:  # 검색어 만큼 실행
        search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "searchKeyword")))
        search_box.clear()
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[.//em[contains(text(), '표/그림')]]")))  # 검색 필터 설정 - 표/그림
        link.click()
        time.sleep(2)
        label_for_table = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='filter1_1']")))  # 검색 필터 설정 - 표
        label_for_table.click()
        checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li[.//button[contains(text(), '논문')]]")))  # 검색 필터 설정 - 논문
        checkbox.click()
        time.sleep(2)
        find_and_download_images(folder_name[index])
        index += 1
        driver.get(url)  # 다음 검색어를 위해 초기 페이지로 돌아감

    driver.quit()
