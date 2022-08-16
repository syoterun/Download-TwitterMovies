# coding: UTF-8
#!/usr/bin/python3

import os
import tweepy
from time import sleep
import urllib.error
import urllib.request
import tkinter as Tkinter
from tkinter import messagebox
import configparser

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

root = Tkinter.Tk()
root.title(u"動画一括保存")
root.geometry("350x50")
root.resizable(False, False)

config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')
CONSUMER_KEY = config_ini['CONSUMER']['KEY']
CONSUMER_SECRET = config_ini['CONSUMER']['SECRET']


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth)

#動画保存
def click(event):
  root.after(1, set_target)
def set_target():
  key_account = txt.get()
  count_no = int(txt2.get())
  search_results = tweepy.Cursor(api.user_timeline, screen_name=key_account).items(count_no)
  if not os.path.exists('img'):
    os.mkdir('img')
  i = 0
  for result in search_results:
    try:
      #動画
      video_url = [variant['url'] for variant in result.extended_entities["media"][0]["video_info"]['variants'] if variant['content_type'] == 'video/mp4'][0]
      print(video_url)
      dst_path = 'img/{}.mp4'.format(i)
      download_file(video_url,dst_path)
      i += 1
      sleep(1)
    except:
      pass
  messagebox.showinfo('成功', '保存完了しました')

def download_file(url, dst_path):
   try:
       with urllib.request.urlopen(url) as web_file:
           data = web_file.read()
           with open(dst_path, mode='wb') as local_file:
               local_file.write(data)
   except urllib.error.URLError as e:
       print(e)

# ラベル
lbl = Tkinter.Label(text='対象アカウント')
lbl.place(x=10,y=3)
# 対象アカウント
txt = Tkinter.Entry(width=20)
txt.place(x=10,y=20)

# ラベル
lbl = Tkinter.Label(text='対象ツイート数')
lbl.place(x=150,y=3)
# 対象ツイート数
txt2 = Tkinter.Entry(width=20)
txt2.place(x=150,y=20)

#実行ボタン
button2 = Tkinter.Button(root, text=u'実行',width=5)
button2.bind("<Button-1>",click)
button2.place(x=300,y=15)


root.mainloop()