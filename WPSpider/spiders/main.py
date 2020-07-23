# -*- coding: utf-8 -*-
# @Time    : 2020/5/24 18:07
# @Author  : Kay Luo
# @FileName: main.py
# @Software: PyCharm

from scrapy import cmdline
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import tkinter.messagebox as message



class App:

    def __init__(self, root):

        root.title('shopify导产品工具')

        # 得到屏幕宽度
        sw = root.winfo_screenwidth()
        # 得到屏幕高度
        sh = root.winfo_screenheight()
        ww = 650
        wh = 400
        x = (sw - ww)/2
        y = (sh - wh)/2
        self.siteList = ["Shopify", "WordPress"]
        # 设置窗口在屏幕中间
        root.geometry("%dx%d+%d+%d" %(ww,wh,x,y))
        self.ButtonList = IntVar()  # IntVar 是tkinter的一个类，可以管理单选按钮

        r1 = Radiobutton(root, variable=self.ButtonList, value=0, text=self.siteList[0])
        r2 = Radiobutton(root, variable=self.ButtonList, value=1, text=self.siteList[1])
        self.ButtonList.set(1)
        r1.grid(row=1, column=1)
        r2.grid(row=1, column=2)
        Label(root, text="请输入网址:").grid(row=0, column=0)
        Label(root, text="请选择网站类型:").grid(row=1, column=0)
        self.e2 = Entry(root, width=50)  # domain
        self.e2.grid(row=0, column=1, padx=10, pady=5)
        self.btn = tk.Button(root, text='下载', command=self.work)
        self.btn.grid(row=2, column=0, ipadx='3', ipady='3', padx='10', pady='20')
        self.btn1 = tk.Button(root, text='退出', command=root.quit)
        self.btn1.grid(row=3, column=0, ipadx='3', ipady='3', padx='10', pady='20')
        self.text1 = tk.Text(root, width='60', height='15')
        self.text1.grid(row=2, column=1)
        self.scroll = tk.Scrollbar(root)
        self.scroll.grid(sticky=S + W + E + N, row=2, column=3)
        self.scroll.config(orient="vertical", command=self.text1.yview)  # 将文本框关联到滚动条上，滚动条滑动，文本框跟随滑动
        self.text1.config(yscrollcommand=self.scroll.set)  # 将滚动条关联到文本框


    def work(self):
        url = self.e2.get()
        t = self.ButtonList.get()
        print(self.siteList[t])

        if 'product' in url:
            print('start products')
            cmdline.execute("scrapy crawl single_spider -a url={}".format(url).split())
        elif 'collections' in url:
            print('start collections')
            cmdline.execute("scrapy crawl wpspider -a url={}".format(url).split())
        else:
            message.showerror('系统提示','url格式有误!')



root = tk.Tk()
app = App(root)
# 开始主事件循环
root.mainloop()