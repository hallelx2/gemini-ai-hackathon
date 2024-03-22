import google.generativeai as genai
import os
from pathlib import Path
import string
import random

genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel('gemini-pro')

chat = model.start_chat(history=[])
def generate_random_filename(length=10):
  """Generates a random alphanumeric filename with the given length."""
  letters_and_digits = string.ascii_letters + string.digits
  return ''.join(random.choice(letters_and_digits) for _ in range(length)) + '.txt'


while True:
    message = input("You: ")
    response = chat.send_message(message or 'How can i help you?')

    random_filename = generate_random_filename()

    with open(random_filename, "a") as chat_file:
        chat_file.write(f"You: {message}\n")
        chat_file.write(f"Chatbot: {response.text}\n\n")
    print(response.text)
