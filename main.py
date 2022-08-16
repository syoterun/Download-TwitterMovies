# coding: UTF-8
#!/usr/bin/python3

import os
import tweepy
from time import sleep
import urllib.error
import urllib.request
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import configparser
import ssl

config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')
CONSUMER_KEY = config_ini['CONSUMER']['KEY']
CONSUMER_SECRET = config_ini['CONSUMER']['SECRET']
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth)

class Application(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.pack()

        self.master.geometry("250x130")
        self.master.title(u"動画一括保存")

        self.create_widgets()


    # Create Widgets function
    def create_widgets(self):
        #Label
        self.label_target = ttk.Label(self)
        self.label_target.configure(text='対象アカウント')
        self.label_target.pack()

        #Entry
        self.target = tk.StringVar()
        self.entry_target = ttk.Entry(self)
        self.entry_target.configure(textvariable = self.target)
        self.entry_target.pack()

        #Label2
        self.label_count=ttk.Label(self)
        self.label_count.configure(text = '対象ツイート数')
        self.label_count.pack()

        #Entry2
        self.count = tk.StringVar()
        self.entry_count = ttk.Entry(self)
        self.entry_count.configure(textvariable = self.count)
        self.entry_count.pack()

        #Button
        self.button_run = ttk.Button(self)
        self.button_run.configure(text="実行")
        self.button_run.configure(command = self.download_movies) 
        self.button_run.pack()

    # Event Callback Function
    def download_movies(self): 
        search_results = tweepy.Cursor(api.user_timeline, screen_name = self.target.get()).items(int(self.count.get()))
        if not os.path.exists('img'):
            os.mkdir('img')
        i = 0
        for result in search_results:
            try:
                #動画
                movie_url = [variant['url'] for variant in result.extended_entities["media"][0]["video_info"]['variants'] if variant['content_type'] == 'video/mp4'][0]
                print(movie_url)
                dst_path = 'img/{}.mp4'.format(i)
                try:
                    with urllib.request.urlopen(movie_url) as web_file:
                        data = web_file.read()
                        with open(dst_path, mode='wb') as local_file:
                            local_file.write(data)
                except urllib.error.URLError as e:
                    print(e)
                i += 1
                sleep(1)
            except:
                pass
        messagebox.showinfo('成功', '保存完了しました')
        print('exit')

def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
