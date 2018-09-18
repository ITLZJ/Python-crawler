from pygeocoder import Geocoder

import requests

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
        #address = self.paraments['address']
        print(Geocoder.geocode(address=self._address)[0].split(' ')[0])

    #----------使用Request库
    def geocode_2(self):
        base = 'http://ditu.google.cn/maps/api/geocode/json'
        response = requests.get(url=base,params=self._paraments)#开始请求
        answer  = response.json()#获得数据进行JSON解析
        print(answer['results'][0]['formatted_address'].split(' ')[0])

    #-------Http+json+Requset
    def geocode_3(self):

        base_3 = '/maps/api/geocode/json'
        path = '{}?address{}&sensor=false'.format(base_3,quote_plus(self._address))#路径拼接
        connection = http.client.HTTPConnection('ditu.google.cn')#建立连接
        connection.request('GET',path)#开始请求
        rawreply = connection.getresponse().read()#读取
        reply = json.loads(rawreply.decode('utf-8'))#二进制编码UTF-8，对JSON进行解码
        print(reply['results'][0]['formatted_address'].split(' ')[0])

    #---------socket完成原始HTTP网络会话
    def geocode_4(self):
        request_text = """\
        GET /maps/api/geocode/json?address={}&sensor=false HTTP/1.1\r\n\
        Host: ditu.google.cn:80\r\n\
        User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64)\r\n
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110\r\n
        Safari/537.36 SE 2.X MetaSr 1.0\r\n
        Accept: */*\r\n
        DNT: 1\r\n
        Referer: http://www.google.cn/\r\n
        Accept-Encoding: gzip, deflate\r\n
        Accept-Language: zh-CN,zh;q=0.8\r\n
        Cookie: NID=139=IMWBZJNhT3OUNjykWdVYA1t-X-ClWAA3sUsoXxIOorPsgO-hfYkvkdxCkovARgJIc_Nb-bcf7T9ufeCltTreq_RQfsfSvisHiOLcKtAgx4Uo6cg2RAbnKcLVwHPclnkkSS7bCOue4QJ7eBc; 1P_JAR=2018-09-18-09\r\n
        Connection: close\r\n\
        \r\n\
        \r\n
        """  # 构造请求头
        sock = socket.socket()
        sock.connect(('ditu.google.cn', 80))  # 指定端口连接
        request = request_text.format(quote_plus(self._address))
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
        temp = reply_arr[1].strip().strip('950')#去掉头尾状态码
        json_temp = json.loads(temp)['results'][0]['formatted_address'].split(' ')[0]#数据处理
        print(json_temp)

if __name__ == '__main__':
    parameters = {'address': '你的英文地址名称', 'sensor': 'false'}
    API = Maps(paraments=parameters)
    #使用调试
    API.geocode_1()