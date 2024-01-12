import os

import openai
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("API_VERSION")
)


def send_message(messages, model_name):
    """Gửi 1 message mới tới model
    :param messages List các tin nhắn giữa assistant và user
    :param model_name Tên model sử dụng GPT35TURBO | GPT35TURBO16K | ADA
    """
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages
        )
        return response.choices[0].message.content
    except openai.OpenAIError as e:
        print(f"OpenAI returned an Error: {e}")


def main():
    messages = [
        {"role": "system", "content": "How can I help you today"},
        {"role": "user", "content": "What food do cats like to eat?"}
    ]
    model = "GPT35TURBO"
    response = send_message(messages, model)
    print(response)


if __name__ == "__main__":
    main()
