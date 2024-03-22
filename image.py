import google.generativeai as genai
import os
from pathlib import Path
import string
import random
# Replace with your actual API key


genai.configure(os.environ["API_KEY"])

model = genai.GenerativeModel('gemini-pro-vision')

cookie_picture = {
    'mime_type': 'image/png',
    'data': Path('cookie.jpeg').read_bytes()
}
prompt = """• 👊 Try new true competitor of ChatGPT 4
• 💡 Create an app with intuitive support from Gemini Ultra 1.0
• 🤝 Take part alone or form a team with other participants
• 🚀 The final project can be used for your portfolio, and the startup application to the Slingshot accelerator
"""

response = model.generate_content(
    contents=[prompt, cookie_picture]
)
print(response.text)