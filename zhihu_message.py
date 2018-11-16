#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/12 15:55
# @Author  : Sa.Song
# @Desc    : 
# @File    : zhihu_message.py
# @Software: PyCharm


import time
import base64
import json
from PIL import Image
from selenium import webdriver
from dama import use_ydm


user = '15894648760'
pwd = '*hs19931221*'


def main():

    options = webdriver.ChromeOptions()
    options.add_argument('lang=zh_CN.UTF-8')  # 设置中文
    options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get('https://www.zhihu.com/signup?next=%2F')  # 请求登录界面
    span_lable = browser.find_elements_by_xpath('//div[@class="SignContainer-switch"]/span')[0]
    span_lable.click()
    username = browser.find_elements_by_name('username')[0]  # 获取username的input标签
    time.sleep(3)
    username.send_keys(user)
    time.sleep(3)
    password = browser.find_elements_by_name('password')[0]  # 获取password的input标签
    password.send_keys(pwd)
    time.sleep(3)
    return browser

def make_base64(new_img_code):  # 处理经base64加密的图片并保存到本地
    new_img_code = base64.b64decode(new_img_code)
    with open('img_code.png', 'wb') as f:
        f.write(new_img_code)

def show_img():  # 展示验证码
    img = Image.open('img_code.png')
    img.show()

def get_message(browser):  # 获取主页title列表
    title_list = browser.find_elements_by_xpath('//div[contains(@class, "TopstoryItem-isRecommend")]/div[@class="Feed"]/div[contains(@class, "AnswerItem")]')  # 获取主页标题列表
    for i in title_list:
        title_dict = i.get_attribute("data-zop")
        title_dict = json.loads(title_dict)
        print(title_dict['title'])


if __name__ == '__main__':
    while True:
        browser= main()
        span_lable = browser.find_elements_by_xpath('//div[contains(@class, SignFlow-captchaContainer)]/div/span[@class="Captcha-englishImage"]')  # 查找英文验证码的标签
        button = browser.find_elements_by_xpath('//button[contains(@class, "SignFlow-submitButton")]')[0]  # 登录按钮
        if len(span_lable) == 0:  # 判断验证码类型，是中文（点击类型）还是英文（输入类型）的
            img_lable = browser.find_elements_by_xpath('//img[@class="Captcha-chineseImg"]')[0] # 查找中文验证码标签
            img_url = img_lable.get_attribute('src')  # 验证码图片路径
            if img_url == 'data:image/jpg;base64,null':  # 判断是否有验证码
                print('没有验证码,直接点击登录！')
                button.click()
                time.sleep(3)
                get_message(browser)
                break
            else:
                print('中文验证码，暂时处理不了，跳过')
                continue
        elif len(span_lable) == 1:
            img_lable = browser.find_elements_by_xpath('//img[@class="Captcha-englishImg"]')[0]  # 查找中文验证码标签
            img_url = img_lable.get_attribute('src')  # 验证码图片路径
            if img_url == 'data:image/jpg;base64,null':  # 判断是否有验证码
                print('没有验证码,直接点击登录！')
                button.click()
                time.sleep(3)
                get_message(browser)
                break
            else:
                base64_img_url = img_url.replace('data:image/jpg;base64,','')  # 对base64做处理
                make_base64(base64_img_url)
                input_lable = browser.find_elements_by_name('captcha')[0]
                # show_img()
                # input_lable = input('手动打码，请输入验证码>>>')
                code = use_ydm('img_code.png')  # 调用云打码接口，返回识别后的内容
                input_lable.send_keys(code)    # 将验证码写入
                time.sleep(3)
                button.click()
                time.sleep(3)
                get_message(browser)  # 获取主页标题
                break
