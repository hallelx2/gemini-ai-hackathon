import os
import google.generativeai as genai

# Replace with your actual API key

genai.configure(api_key=os.environ("API_KEY"))

model = genai.GenerativeModel('gemini-pro')

chat = model.start_chat(history=[])
messages = []
count = 0

while True:
    message = input("You: ")
    messages.append({'role': 'user', 'parts': [message]})
    response = model.generate_content(messages)
    messages.append({'role': 'gemniai', 'parts': [response.text]})
    print(response.text)
    count += 1
    if count == 3:
        break

i = 0
while i < len(messages):
    print(messages[i]['role'],": ", messages[i]['parts'][0])
    i += 1
