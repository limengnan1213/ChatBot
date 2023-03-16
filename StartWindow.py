# -*- coding: utf-8 -*-
import json
import tkinter as tk
from tkinter import messagebox
import CheckAPI
class StartWindow:
    def __init__(self):
        root = tk.Tk()
        root.configure(bg='#efe4e1')
        WINDOW_WIDTH, WINDOW_HEIGHT = (500, 280)
        # 获取屏幕宽度和高度并计算左上角坐标值
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_coordinate = int((screen_width - WINDOW_WIDTH) / 2)
        y_coordinate = int((screen_height - WINDOW_HEIGHT) / 2)
        root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x_coordinate}+{y_coordinate}")
        root.title("Enter API Key")
        root.attributes("-topmost", True)

        self.label = tk.Label(root, text="请输入你的openai API key", bg="#efe4e1", font=("华文楷体", 12))
        self.label.grid(row=0, padx=10, pady=10)
        self.entry = tk.Entry(root, width=50, bg='light gray')
        self.entry.grid(row=1, padx=(50, 50), pady=20)
        self.submit_button = tk.Button(root, text='提交', width=5, height=2, bg='#fff2df', font=("华文楷体", 13),
                                       command=self.submit)
        self.submit_button.grid(row=2, columnspan=2, pady=20)
        self.label1 = tk.Label(root, text="点击提交后请等待几秒钟", bg="#efe4e1", font=("华文楷体", 12))
        self.label1.grid(row=3, columnspan=2, pady=5)
        self.root = root

    def submit(self):
        check0 = CheckAPI.CheckAPI(self.entry.get())
        if check0.check():  # 检查api key是否有效
            messagebox.showinfo("提交成功", "api key有效！")
            with open('data/apikey.json', 'w') as f1:
                json.dump([{"key":self.entry.get()}],f1)
            self.root.destroy()
            import WindowUI
            WindowUI.ChatUI().run()
        else:
            messagebox.showerror("提交失败", "api key无效！")
            self.entry.delete(0, tk.END)  # 清空输入bar
            self.entry.update()