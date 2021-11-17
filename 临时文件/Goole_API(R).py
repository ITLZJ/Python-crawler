from pygeocoder import Geocoder
import requests
import time
import http.client
import json
from urllib.parse import quote_plus
import socket

class Maps:
    def __init__(self,paraments):
        self._paraments = paraments
        self._address = self._paraments['address']


    def print_m(self):
        print(type(self._address))

    #简单实现
    def geocode_1(self):
        try:
            #address = self.paraments['address']
            print(Geocoder.geocode(address=self._address)[0].formatted_address.split(' ')[0])
        except Exception:

            self.geocode_1()

    #----------使用Request库
    def geocode_2(self):
        try:
            base = 'http://ditu.google.cn/maps/api/geocode/json'
            response = requests.get(url=base,params=self._paraments)#开始请求
            answer  = response.json()#获得数据进行JSON解析
            print(answer['results'][0]['formatted_address'].split(' ')[0])
        except Exception:
           # time.sleep(5)
            self.geocode_2()

    #-------Http+json+Requset
    def geocode_3(self):
        try:
            base_3 = '/maps/api/geocode/json'
            path = '{}?address={}&sensor=false'.format(base_3,quote_plus(self._address))#路径拼接
            connection = http.client.HTTPConnection('ditu.google.cn')#建立连接
            connection.request('GET',path)#开始请求
            rawreply = connection.getresponse().read()#读取
            reply = json.loads(rawreply.decode('utf-8'))#二进制编码UTF-8，对JSON进行解码
            print(reply['results'][0]['formatted_address'].split(' ')[0])
        except Exception:
            #time.sleep(5)
            self.geocode_3()

    #---------socket完成原始HTTP网络会话
    def geocode_4(self):

        self.request_text = """\
        GET /maps/api/geocode/json?address={}&sensor=false HTTP/1.1\r\n\
        Host: ditu.google.cn:80\r\n\
        User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0\r\n
        Accept: */*\r\n
        DNT: 1\r\n
        Referer: http://www.google.cn/\r\n
        Accept-Encoding: gzip, deflate\r\n
        Accept-Language: zh-CN,zh;q=0.8\r\n
        Cookie:NID=139=LkIFXm2emuOxaQIPiLeAAAhDNzPaypvHMSugqaMrJeSIV0Cv_QTy53CMokY3fSJya0XSq6vsrqTYG3rSik5_LoARbp9ittBy0RNinUjVwSY5E6EFPvynILTIhiC2f0PLIjuyLG1XNn4uaew; 1P_JAR=2018-09-19-08\r\n
        Connection: close\r\n\
        \r\n
        """  # 构造请求头
        try:
            sock = socket.socket()
            sock.connect(('ditu.google.cn',80))  # 指定端口连接
            request = self.request_text.format(quote_plus('hangzhou dianzi university'))
            sock.sendall(request.encode('ascii'))
            raw_reply = b''
            while True:
                more = sock.recv(4096)
                if not more:
                    break
                raw_reply += more
            sock.close()
            reply = raw_reply.decode('utf-8')
            reply_arr = reply.split('\r\n\r\n')
            temp = reply_arr[1].strip().strip('950')  # 去掉头尾状态码
            json_temp = json.loads(temp)['results'][0]['formatted_address'].split(' ')[0]  # 数据处理
            print(json_temp)
        except Exception:
            #time.sleep(10)
            self.geocode_4()



if __name__ == '__main__':
    parameters = {'address':'hangzhou dianzi university', 'sensor': 'false'}
    API = Maps(paraments=parameters)
    API.geocode_4()
    #使用调试
"""
    print("----程序开始执行-----")
    print("执行第一种方式")
    API.geocode_1()
    #time.sleep(5)
    print('执行第二种方式')
    API.geocode_2()
    #time.sleep(5)
    print('执行第三种方式')
    API.geocode_3()
    time.sleep(15)
"""
   # print('执行第四种方式')

