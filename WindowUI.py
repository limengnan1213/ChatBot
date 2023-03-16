# -*- coding: utf-8 -*-
import json
import tkinter as tk
import time
import ChatBot
class ChatUI:
    def __init__(self):
        chatbot = ChatBot.MyChatBot()
        # Create GUI window
        root = tk.Tk()
        root.configure(bg='#efe4e1')
        WINDOW_WIDTH, WINDOW_HEIGHT = (1080, 640)

        # 获取屏幕宽度和高度并计算左上角坐标值
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_coordinate = int((screen_width - WINDOW_WIDTH) / 2)
        y_coordinate = int((screen_height - WINDOW_HEIGHT) / 2)
        root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x_coordinate}+{y_coordinate}")
        root.title('Chatbot')
        root.attributes("-topmost", True)

        # Create conversation area
        conversation_label = tk.Label(root, text="聊天框", bg="#efe4e1", font=("华文楷体", 12))
        conversation_label.grid(row=0, column=0, sticky='w', padx=15, pady=5)

        conversation_frame = tk.Frame(root, bd=1, bg='white', width=50, height=30)
        conversation_frame.grid(row=1, column=0, sticky='nsew', padx=15, pady=(0, 5))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        # 插入初始消息
        conversation = tk.Text(conversation_frame, state='disabled', bg='#edd9be', font=("华文楷体", 14), padx=15, pady=15)
        conversation.pack(fill='both', expand=True)
        conversation.config(state='normal')
        conversation.insert(tk.END, " 哆啦a梦: 你好呀，大雄！有什么需要我帮助的吗？")
        conversation.config(state='disabled')

        # Create input field
        input_label = tk.Label(root, text="输入:", bg="#efe4e1", font=("华文楷体", 12))
        input_label.grid(row=2, column=0, sticky='w', padx=15, pady=(0, 10))
        input_field = tk.Entry(root, width=50, bg='light gray')
        input_field.bind("<Return>", (lambda event: self.chatting()))
        input_field.grid(row=3, column=0, sticky='nsew', padx=15, pady=(0, 10))

        # Create send and clear buttons
        button_frame = tk.Frame(root, bg="#efe4e1")
        button_frame.grid(row=1, column=1, sticky='nsew', padx=15, pady=(0, 10))
        root.columnconfigure(1, weight=1)
        root.rowconfigure(1, weight=1)

        send_button = tk.Button(button_frame, text='发送', command=self.chatting, width=10, height=2, bg='#fff2df',
                                font=("华文楷体", 13))
        send_button.pack(padx=2, pady=15)

        reset_button = tk.Button(button_frame, text='重置聊天', command=self.reset_conversation, width=10, height=2,
                                 bg='#fff2df', font=("华文楷体", 13))
        reset_button.pack(padx=2, pady=15)

        clear_button = tk.Button(button_frame, text='清理页面', command=self.clear_conversation, width=10, height=2,
                                bg='#fff2df', font=("华文楷体", 13))
        clear_button.pack(padx=2, pady=15)

        restore_button = tk.Button(button_frame, text="载入聊天", command=self.restore_conversation, width=10, height=2,
                                   bg='#fff2df', font=("华文楷体", 13))
        restore_button.pack(padx=2, pady=15)

        delete_button = tk.Button(button_frame, text='删除密钥', width=10, height=2, bg='#fff2df', font=("华文楷体", 13),
                                  command=self.deletekey)
        delete_button.pack(padx=2, pady=15)

        self.chatbot = chatbot
        self.root = root
        self.conversation = conversation
        self.input_field = input_field

    def deletekey(self):
        with open('data/apikey.json', 'w') as f1:
            json.dump([{"key": "sk-0000"}], f1)

    def save_conversation(self,msg):
        with open('data/conversation.txt', 'a') as f:
            if msg['role'] == ChatBot.USER_ROLE:
                f.write(' 大雄: ' + msg['content'] + '\n')
            if msg['role'] == ChatBot.BOT_ROLE:
                f.write(' 哆啦a梦: ' + msg['content'] + '\n')


    def restore_conversation(self):
        with open('data/conversation.txt', 'r', encoding="GBK") as f:
            lines = f.read()
        conversation = self.conversation
        self.clear_conversation()
        conversation.config(state='normal')
        conversation.insert(tk.END, lines)
        conversation.config(state='disabled')  # 设置成不可编辑模式
        conversation.see(tk.END)
        with open('data/history.json', 'r') as f:
            self.chatbot.messages = json.load(f)

    def clear_conversation(self):
        self.chatbot.messages = self.chatbot.reset_log()
        self.conversation.config(state='normal')
        self.conversation.delete('1.0', tk.END)
        self.conversation.config(state='disabled')

    def reset_conversation(self):
        self.clear_conversation()
        with open('data/conversation.txt', 'w') as f:
            f.write(' 哆啦a梦: 你好呀，大雄！有什么需要我帮助的吗？\n')
        self.chatbot.reset_log()
        with open('data/history.json', 'w') as f:
            json.dump(self.chatbot.messages, f)
        self.restore_conversation()

    def print_response(self, input_text):
        self.conversation.config(state='normal')
        stream_response = self.chatbot.get_response(input_text)
        answer = ""
        timeout_cnt = 0
        while True:  # 连续获取stream
            try:
                package = next(stream_response)
                if hasattr(package.choices[0].delta, 'role'):
                    continue
                single_token = package.choices[0].delta.content
                self.insert(single_token)
                self.conversation.see(tk.END)
                self.conversation.update()
                answer += single_token
                if package.choices[0].finish_reason == "stop":
                    break
            except:
                if len(answer) > 0:
                    break
                timeout_cnt += 1
                if timeout_cnt >= ChatBot.TIME_OUT:
                    self.conversation.insert(tk.END, "[Timeout In Stream]")
                    self.conversation.see(tk.END)
                    break
                time.sleep(1)
        self.conversation.config(state='disabled')
        return answer

    def summary_response(self, input_text):
        self.conversation.config(state='normal')
        stream_response = self.chatbot.get_response(input_text)
        answer = ""
        timeout_cnt = 0
        while True:  # 连续获取stream
            try:
                package = next(stream_response)
                if hasattr(package.choices[0].delta, 'role'):
                    continue
                single_token = package.choices[0].delta.content
                answer += single_token
                if package.choices[0].finish_reason == "stop":
                    break
            except:
                if len(answer) > 0:
                    break
                timeout_cnt += 1
                if timeout_cnt >= ChatBot.TIME_OUT:
                    self.conversation.insert(tk.END, "[Timeout In Stream]")
                    self.conversation.see(tk.END)
                    break
                time.sleep(1)
        self.conversation.config(state='disabled')
        return answer

    def insert(self, text):
        self.conversation.config(state='normal')
        self.conversation.insert(tk.END, text)
        self.conversation.config(state='disabled')
        self.conversation.see(tk.END)

    # 定义获取响应的函数
    def chatting(self):
        input_text = self.input_field.get()
        self.insert(' 大雄: ' + input_text+'\n')  # 导出用户输入
        self.input_field.delete(0, tk.END)  # 清空输入bar
        self.input_field.update()
        self.input_field.config(state='disabled')
        if len(ChatBot.ENCODER.encode(str(self.chatbot.messages))) > ChatBot.MAX_TOKEN_LEN:
           # print(len(ChatBot.ENCODER.encode(str(self.chatbot.messages))))
            self.insert(' 正在总结对话请稍等~\n')
            answer0 = self.summary_response("Please summarize our conversation concisely and effectively.")
            #print(answer0)
            self.chatbot.messages = self.chatbot.reset_log()
            self.chatbot.add_bot_content(answer0)
        self.insert(' 哆啦a梦: ')  # 开始导出回答
        answer = self.print_response(input_text)
        self.insert('\n')  # 导出机器人回答'
        self.chatbot.add_bot_content(answer)  # 记录机器人的回答
        #print(self.chatbot.messages)
        with open('data/history.json', 'w') as f:
            json.dump(self.chatbot.messages, f)
        self.save_conversation(self.chatbot.get_user_content())
        self.save_conversation(self.chatbot.get_bot_content())
        self.input_field.config(state='normal')

    def run(self):
        self.restore_conversation()
        self.root.mainloop()
