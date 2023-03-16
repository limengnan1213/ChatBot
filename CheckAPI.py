# -*- coding: utf-8 -*-
import requests

class CheckAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        self.data = {
            "prompt": "Hello, World!",
            "max_tokens": 5,
        }

    def check(self):
        response = requests.post(
            url="https://api.openai.com/v1/engines/davinci-codex/completions",
            headers=self.headers,
            json=self.data)
        if response.status_code == 200:
            #print("OpenAI API Key is valid!")
            return True
        else:
            #print("Invalid OpenAI API Key. Please check your credentials.")
            return False
