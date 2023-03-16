import openai
import tiktoken
from tkinter import messagebox
import json

with open('data/apikey.json', 'r') as f:
    line = json.load(f)
    SECRET_KEY = line[0]['key']

openai.api_key = SECRET_KEY
MAX_TOKEN_LEN = 2048
TIME_OUT = 30
BOT_ROLE = 'assistant'
USER_ROLE = 'user'
ENCODER = tiktoken.get_encoding("gpt2")

class MyChatBot:
    def __init__(self) -> None:
        self.messages = []
        self.reset_log()

    def receive_message_from_api(self):
        response = []
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=self.messages,
                temperature=0.5,
                max_tokens=MAX_TOKEN_LEN,
                top_p=1.0,
                frequency_penalty=2.0,
                presence_penalty=0.0,
                stream=True,
                timeout=TIME_OUT,
            )
        except openai.error.APIConnectionError:
            messagebox.showerror("API Connection Error", "Please check your internet connection.")
            print('Error: OpenAI API timeout')
        return response

    def get_response(self, prompt):
        self.add_user_content(prompt)
        stream_response = self.receive_message_from_api()
        return stream_response

    def reset_log(self):
        self.messages = [{'role': 'system',
                          'content': f'Doraemon and Nobita are two cartoon characters. Doraemon often helps Nobita solve problems. Now, I will play the role of Nobita, and you can be Doraemon to talk with me in his tone.'}]
        return self.messages

    def add_user_content(self, content):
        self.messages.append({'role': USER_ROLE, 'content': content})

    def add_bot_content(self, content):
        self.messages.append({'role': BOT_ROLE, 'content': content})

    def get_bot_content(self):
        return self.messages[-1]

    def get_user_content(self):
        return self.messages[-2]
