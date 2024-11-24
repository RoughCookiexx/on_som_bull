import openai
from openai import OpenAI
from secrets import CHATGPT_API_KEY


def send_message_to_chatgpt(message, chat_gpt_client):
    response = chat_gpt_client.chat.completions.create(
        model='gpt-3.5-turbo',
              messages=[{"role": "user", "content": message}],
              max_tokens=500)

    return response.choices[0].message.content


# Example usage
if __name__ == "__main__":
    client = OpenAI(api_key=CHATGPT_API_KEY)
    user_message = input("Enter your message for ChatGPT: ")
    reply = send_message_to_chatgpt(user_message, client)
    print("ChatGPT's reply:", reply)
