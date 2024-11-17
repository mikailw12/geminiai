import google.generativeai as genai
from config import API_KEY

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')
def text_request(request_text, user_history):
    if user_history:
        response = model.generate_content(f'Мои предыдущие 5 запросов и ответов - {user_history}\nМой текущий запрос - {request_text}')
        return response.text
    else:
        response = model.generate_content(request_text)
        return response.text