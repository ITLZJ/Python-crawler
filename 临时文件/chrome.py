from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def Head_Chrome():
    driver = webdriver.Chrome(executable_path='D:\pythonEdit\chromedriver\chromedriver.exe')
    return driver

def Headless_Chrome():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920, 1080")
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4484.7 Safari/537.36')
    driver = webdriver.Chrome(executable_path='D:\pythonEdit\chromedriver\\v90', options=chrome_options)
    return driver

if __name__ == '__main__':
    d = Headless_Chrome()
    print(d)