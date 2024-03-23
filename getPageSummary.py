import os
import requests
from bs4 import BeautifulSoup
import pathlib
import textwrap
import markdown
import google.generativeai as genai


def get_body_content(url):
  """Fetches the website content and extracts the body text.

  Args:
      url: The URL of the website to scrape.

  Returns:
      The extracted body text of the website, or None if there's an error.
  """
  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise exception for unsuccessful requests
    soup = BeautifulSoup(response.content, 'html.parser')
    body = soup.find('body')
    if body:
      # Extract text content, consider filtering for relevant elements (optional)
      return body.get_text(separator='\n')
    else:
      print("Error: Body element not found.")
      return None
  except requests.exceptions.RequestException as e:
    print(f"Error fetching website: {e}")
    return None


API_KEY = os.environ['API_KEY']

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-pro')

prompt_template = '''You are tasked with creating an accessible version of a website for people with disabilities. 
Thhis is the information on the website: {}.

The goal is to transform the content of the website into a more narrative and explanatory format, 
making it easier for individuals with disabilities, such as visual impairments or cognitive disabilities, 
to comprehend and navigate.

Consider the following guidelines while transforming the content:

- Simplify complex language and technical terms to enhance readability.
- Provide detailed explanations and context for images, charts, and other visual elements.
- Use descriptive headings and subheadings to organize the content and improve navigation.
- Break down lengthy paragraphs into shorter, digestible sections for better understanding.
- Incorporate alternative text (alt text) for images to convey their meaning to individuals using screen readers.
- Ensure that the overall tone is inclusive, empathetic, and engaging to encourage users to explore the content further.

Your task is to generate a narrative version of the website's content that aligns with these guidelines. 
Focus on conveying the key information in a clear, concise, and accessible manner, ensuring that individuals with 
disabilities can fully engage with the content and gain valuable insights on [topic/niche].
'''

def get_prompt_template(url):
  page_body =get_body_content(url)
  template = prompt_template.format(page_body)
  return template

def generate_response(template):
    response = model.generate_content(template).text
    return response

url = 'https://blog.hubspot.com/marketing/how-to-use-medium'
prompt_template = get_prompt_template(get_body_content(url))

def main():
    print(generate_response(prompt_template))


if __name__=='__main__':
   main()
