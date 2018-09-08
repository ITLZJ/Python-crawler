from  tkinter import *
from  tkinter import messagebox
import requests
class windowTable(object):

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    def tk(self):

        self.root = Tk()
        self.root.title('中英互译')
        self.root.geometry('500x120+500+300')
        self.Lable()
        self.Entry_text()
        self.Butoon()
        self.root.mainloop()

    def Lable(self):
        lable = Label(self.root,text = '请输入要翻译的文字：',font = ('微软雅黑',10))
        lable.grid(row = 0,column = 0)
        lable_1 = Label(self.root,text = '  翻   译  的  文  本：',font = ('微软雅黑',10))
        lable_1.grid(row = 1,column=0,sticky = W )

    def Entry_text(self):
        self.res = StringVar()
        self.entry_1 = Entry(self.root,width = 30,font = ('微软雅黑',10))
        self.entry_1.grid(row = 0,column=1)
        self.entry_2 = Entry(self.root,width = 30,font = ('微软雅黑',10),textvariable=self.res)
        self.entry_2.grid(row = 1,column = 1)

    def Butoon(self):
        button_1 = Button(self.root,text = '翻译',font = ('微软雅黑',10),command=self.translation)
        button_1.grid(row = 2,column = 0,sticky=W)
        button_2 = Button(self.root,text = '退出',font = ('微软雅黑',10),command = self.root.quit)
        button_2.grid(row=2,column = 1,sticky = E)

    def translation(self):
        self.content = self.entry_1.get()
        if self.content == '':
                messagebox.showinfo('提示','请输入要翻译的文本')
        else:

                url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
                data = {}
                data['i']= self.content
                data['from']= 'AUTO'
                data['to']= 'AUTO'
                data['smartresult']= 'dict'
                data['client']= 'fanyideskweb'
                #data['salt']= f
                #data['sign']= sign
                data['doctype']= 'json'
                data['version']= '2.1'
                data['keyfrom']= 'fanyi.web'
                data['action'] = 'FY_BY_REALTIME'
                data['typoResult'] = 'false'
                result = requests.post(url=url,data=data,headers = self.header).json()['translateResult'][0][0]['tgt']
                self.res.set(result)

if __name__  == '__main__':
    begin = windowTable()
    begin.tk()





