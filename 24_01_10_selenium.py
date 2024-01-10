# 크롬 드라이버 기본 모듈
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json
import codecs

# 크롬 드라이버 자동 업데이트를 위한 모듈
from webdriver_manager.chrome import ChromeDriverManager

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러 메시지 삭제
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 크롬 드라이버 최신 버전 설정
service = Service(executable_path=ChromeDriverManager().install())

browser = webdriver.Chrome(service=service, options=chrome_options)

# 웹페이지 해당 주소 이동
url = input('웹페이지 URL를 입력하세요: ')
browser.get(url)
time.sleep(5)

# 페이지 소스코드 가져오기
html = browser.page_source

# JSON 데이터 추출을 위한 JavaScript 실행
json_data = browser.execute_script("return JSON.stringify(window.__PRELOADED_STATE__)")

# JSON 데이터가 있는지 확인
if json_data:
    # JSON 데이터 파싱
    parsed_json = json.loads(json_data)

    # JSON 데이터 출력
    print(parsed_json)

    # 파일 저장
    with codecs.open('output.json', 'w', encoding='utf-8') as file:
        json.dump(parsed_json, file, indent=4, ensure_ascii=False)
        print("JSON 파일이 성공적으로 저장되었습니다.")

# 파일 읽기
filename = 'output.json'  # 이전에 저장한 'output.json'으로 고정합니다.

with open(filename, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# 경로를 입력받아 해당하는 데이터를 찾는 함수
def find_data_by_path(data, path):
    keys = path.split('->')  # '->' 구분자를 기준으로 키 목록 생성
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]  # 다음 키로 데이터 접근
        else:
            return None  # 경로에 해당하는 데이터가 없으면 None 반환
    return data

# JSON 파일에 데이터 추가
def append_to_json_file(data, file_name):
    try:
        with open(file_name, 'r+', encoding='utf-8') as file:
            file_data = json.load(file)
            file_data.append(data)  # 리스트에 새로운 데이터 추가
            file.seek(0)  # 파일 포인터를 시작으로 이동
            file.truncate()  # 기존 내용을 삭제
            json.dump(file_data, file, indent=4, ensure_ascii=False)
    except FileNotFoundError:
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump([data], file, indent=4, ensure_ascii=False)

# 사용자가 '종료'를 입력할 때까지 반복
while True:
    path_input = input("데이터의 경로를 '->' 기호로 구분하여 입력하세요 (예: product->A), 또는 종료하려면 '종료'를 입력하세요: ")
    
    if path_input.lower() == "종료":
        print("프로세스를 종료합니다.")
        break

    key_input = input("추출하고 싶은 키를 입력하세요: ")
    extracted_data = find_data_by_path(json_data, path_input)
    
    if extracted_data is not None and key_input in extracted_data:
        value_output = extracted_data[key_input]
        print(f"{key_input} 키를 가진 데이터:")
        print(json.dumps(value_output, indent=4, ensure_ascii=False))
        
        # JSON 파일에 데이터 추가
        data_to_append = {key_input: value_output}
        append_to_json_file(data_to_append, 'extracted_data.json')
        print(f"데이터가 'extracted_data.json' 파일에 추가되었습니다.")
    else:
        print(f"{key_input} 키를 가진 데이터가 없거나 입력하신 경로에 해당하는 데이터를 찾을 수 없습니다.")

browser.quit()  # 브라우저 종료

# https://shopping.naver.com/logistics/products/6042668419?NaPm=ct%3Dlr7cczoy%7Cci%3Dshoppingwindow%7Ctr%3Davgtc%7Chk%3D3e463a756e039477264adf22c5d2df43ae875dcf%7Ctrx%3D