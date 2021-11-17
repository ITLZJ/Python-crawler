import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotInteractableException, ElementClickInterceptedException
from spider import chrome
import urllib.parse as urlcode
from pandas import DataFrame, ExcelWriter
import random





# #初始总界面
# new_url = "https://movie.douban.com/cinema/nowplaying/hangzhou/"
# driver.get(new_url)
# init_url = []  # 总url
# li_list = driver.find_elements_by_xpath('//*[@id="db-nav-movie"]//*[@class="nav-items"]/ul//*[@href]')
# for i in li_list:
#     init_url.append(i.get_attribute('href'))


# 单个豆瓣电影评论



# 选电影
def perMovie(url, driver):
    h_xpath = '//*[@id="content"]/h1//*'
    score_xpath = '//*[@id="interest_sectl"]//*[@class="rating_self clearfix"]//strong'
    name = ''
    driver.get(url)
    time.sleep(0.5)
    spans = driver.find_elements_by_xpath(h_xpath)
    for span in spans:
        name+=span.text
    score = driver.find_element_by_xpath(score_xpath).text
    data.append([name, score])
    print("详细信息为："+name+"\t"+score)
    return 1




# 加载一页
def load_page(driver, movie_xpath):
    global data
    movies = driver.find_elements_by_xpath(movie_xpath)[-20:]
    try:
        moviesName = [''.join(str(i.text).split(' ')[0:-1]) for i in movies]
        scoresList = [str(i.text).split(' ')[-1] for i in movies]
        for index,v in enumerate(moviesName):
            data.append([v,scoresList[index]])
        return 1
    except IndexError as e:
        scores = driver.find_elements_by_xpath('//*[@id="content"]//*[@class="list"]//*[@class="item"]/p/strong')[-20:]
        moviesName = [i.text for i in movies]
        scoresList = [i.text for i in scores]
        for index, v in enumerate(moviesName):
            data.append([v, scoresList[index]])


def single_begin():
    driver = chrome.Headless_Chrome()
    print("创建驱动成功")
    with open('D:\pythonEdit\Intelligent\spider\\tool\stealth.min.js-main\stealth.min.js') as f:
        js = f.read()
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })


    destinationUrlTemplate = "https://movie.douban.com/explore#!type=movie&tag={}&sort=time&page_limit=20&page_start=0"
    m = urlcode.quote("热门")
    url = destinationUrlTemplate.format(m)
    init_xpath = '//*[@id="content"]//*[@class="tag-list"]//label'
    driver.get(url)
    labels = driver.find_elements_by_xpath(init_xpath)
    wordQuoteList = []
    for i in labels:
        wordQuoteList.append(i.text)

    movie_xpath = '//*[@id="content"]//*[@class="list"]//*[@class="item"]/p'

    for word in wordQuoteList:
        global data
        data = []
        # 加载热门板块
        print("开始抓取{}板块".format(word))
        newurl = destinationUrlTemplate.format(urlcode.quote(word))
        time.sleep(random.randint(1,3))
        driver.get(newurl)
        time.sleep(random.randint(1,3))
        driver.refresh()
        time.sleep(2)
        while 1:
            load_page(driver, movie_xpath)
            time.sleep(random.randint(1,3))
            loadMore_xpath = '//*[@id="content"]//*[@class="more"]'
            f = driver.find_element_by_xpath(loadMore_xpath)

            if "加载更多" in f.text:
                try:
                    f.click()
                    time.sleep(random.randint(1,3))
                    print("抓取20个数据成功, 开始抓取下20个数据")
                    continue
                except Exception as e:
                    print(e)
                    print("无加载更多？")
                    print(newurl)
                    return
            else:
                print(newurl)
                break

        print("抓取{}数据完毕，开始保存数据".format(word))
        df = DataFrame(data)
        df.to_excel('./downloadData/{}.xlsx'.format(word), sheet_name=word)

if __name__ == '__main__':
    data = []
    startTime = time.time()
    single_begin()
    print("总耗时长\n")
    print(time.time()-startTime)


    # scoresList = [i.text for i in scores]
    # if len(moviesName) == len(scoresList):
    #     for index,v in enumerate(moviesName):
    #         print(v + scoresList[index])
    # else:
    #     print("获取数据与分数不匹配")