from tkinter import *
import urllib.request
from HandleJs import Py4Js
from tkinter import messagebox
from tkinter import ttk
import tkinter
class GoogleTranslation:
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

    def tk(self):
        self.root = Tk()
        self.root.title('谷歌翻译')
        self.root.geometry('350x150+500+300')
        self.Lable()
        self.Entry_text()
        self.Button()
        self.root.mainloop()


    def Lable(self):
        self.lable_1 = Label(self.root,text = '输入将要翻译的文本：',font = ('微软雅黑',10))
        self.lable_1.grid(row = 0,column = 0)
        self.lable_2 = Label(self.root,text = '翻译之后的文本：',font=('微软雅黑',10))
        self.lable_2.grid(row = 1,column=0,sticky=W)

    def Entry_text(self):
        self.res = StringVar()
        self.entrytext_1 = Entry(self.root,width = 20,font=('微软雅黑',10))
        self.entrytext_1.grid(row = 0,column=1)
        self.entrytext_2 = Entry(self.root,width = 20,font = ('华文行楷',10),textvariable = self.res)
        self.entrytext_2.grid(row = 1,column=1)

    def Button(self):
        self.button_1 = Button(self.root,text = '翻译',width = 10,font = ('华文行楷',16),command = self.ClickButton)
        self.button_1.grid(row = 2,column = 0,sticky=W)
        self.button_2 = Button(self.root,text = '退出',width = 10,font=('华文行楷',16),command = self.root.quit)
        self.button_2.grid(row = 2,column = 1,sticky=E)



    def go(self):#处理事件，下拉框选择以后
        pass

    # 下拉框实现
    def comboxSelect(self):

        self.comvalue =  tkinter.StringVar()#窗体自带文本，新建一个新的值
        self.comboxlist = ttk.Combobox(self.root,textvariable = self.comvalue)#初始化文本
        self.comboxlist.grid(row = 4,column = 0,sticky = E)
        self.comboxlist["values"] = ('1','2','3','4')
        self.comboxlist.current(0)#默认选择第一个
        self.comboxlist.bind("<<ComboboxSelected>>",self.go)
        self.comboxlist.pack()



    def open_url(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        self.req = urllib.request.Request(url=self.url,headers=self.header)
        self.response = urllib.request.urlopen(self.req)
        data = self.response.read().decode('utf-8')
        return data

    """def Translate(self):

        content = urllib.request.quote(self.content)#修改结果传入到ClickButton中调用
        self.url = "https://translate.google.cn/translate_a/single?client=t&sl=en&tl=zh-CN&hl=zh-CN" \
          "&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca" \
          "&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&otf=1" \
          "&ssel=3&tsel=0&kc=5&tk=%s&q=%s" % (self.tk,content)

        #self.result =self.data

        self.end = self.data.find("\",")
        if self.end > 4:
            self.res.set(self.data[4:self.end])"""


    def ClickButton(self):
        js = Py4Js()
        self.content = self.entrytext_1.get()
        if self.content == '':
            messagebox.showinfo('提示','请输入翻译的内容')
        elif self.content == 'q':
            pass
        else:

            tk = js.getTk(self.content)
            content = urllib.request.quote(self.content)  # 修改结果传入到ClickButton中调用
            self.url = "https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=zh-CN&hl=zh-CN" \
                        "&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca" \
                        "&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&otf=1" \
                        "&ssel=3&tsel=0&kc=5&tk=%s&q=%s" % (tk,content)
            result =self.open_url()

            end = result.find("\",")
            if end > 4:
                self.res.set(result[4:end])

if __name__ == '__main__':
    begin = GoogleTranslation()
    begin.tk()
