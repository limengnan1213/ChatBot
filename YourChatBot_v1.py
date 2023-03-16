# -*- coding: utf-8 -*-
import json
import StartWindow
from tkinter import messagebox
import CheckAPI
with open('data/apikey.json', 'r') as f:
    line = json.load(f)
    SECRET_KEY = line[0]['key']
check = CheckAPI.CheckAPI(SECRET_KEY)
if check.check():
    messagebox.showinfo("Sign in...", "Sign in successfully!")
    import WindowUI
    WindowUI.ChatUI().run()
else:
    start_window = StartWindow.StartWindow()
    start_window.root.mainloop()


