#windows+pycharm+python3.6

import os
import requests
from   multiprocessing import Pool#导入进程池加快下载速度

def temp(i):


    url = 'https://cn2.okokyun.com/20171128/JQPNBqRh/800kb/hls/HEUm0Cr4486%03d.ts'% i
    #模拟浏览器
    headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"
    }
    result = requests.get(url=url,headers  = headers)
    #print(result.content)#content返回的是二进制，text返回的是字符串
    name = 'mp5'
    file_name = os.getcwd()+'\%s\\' % name
    if not os.path.exists(file_name):
        os.mkdir(file_name)

    with open('./mp5/{}'.format(url[-10:]),'wb') as f :
        f.write(result.content)

if __name__ == "__main__":
    pool = Pool(20)
    for i in range(7013):
        pool.apply_async(temp,(i,))
    pool.close()
    pool.join()

#视频下载完毕后拼接命令：copy /b *.ts "你的电影名字".mp4