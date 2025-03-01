from openai import OpenAI
import yaml
import os
from dotenv import load_dotenv

load_dotenv()  
API_KEY = os.getenv("OPENAI_API_KEY")


class ChatManager:
    def __init__(self):
        self.client = OpenAI(api_key=API_KEY)
        chat_config = self.load_chat_config()
        self.model_name = chat_config["model_name"]
        self.token_limit = chat_config["token_limit"]
        self.word_limit = 50  # model response size

        self.previous_trades = {}  # e.g., {"trade": [extra metadata]}
 
    def load_chat_config(self, file_path="./chatbot/chat_config.yaml"):
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data

    def load_crypto_data(self):
        return {}

    def parse_crypto_data(self, crypto_data):
        return ""
    
    def add_past_trade_info(self):
        pass

    def generate_prompt(self):
        crypto_data = self.load_crypto_data()
        supplementary_data = self.parse_crypto_data(crypto_data)
        prompt = f"Here is some relevant crypto data:\n{supplementary_data}"
        return prompt

    def query_model(self, user_query):
        prompt = self.generate_prompt()

        # print(prompt)

        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": f"{prompt}\n Respond in {self.word_limit} words or less."},
                {"role": "user", "content": user_query}
            ],
            max_tokens=self.token_limit
        )

        response = completion.choices[0].message.content
        return response


def main():
    chat_manager = ChatManager()
    print("Chatbot is ready! Type 'exit' to end the conversation.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Exiting chat. Goodbye!")
            break

        response = chat_manager.query_model(user_input)
        print(f"Bot: {response}\n")


if __name__ == "__main__":
    main()
