import google.generativeai as genai
import config

genai.configure(api_key=config.API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')
def text_request(request_text, user_history):
    if user_history:
        response = model.generate_content(f'Мои предыдущие 5 запросов - {user_history}\nМой текущий запрос - {request_text}')
        print(user_history)
        return response.text
    else:
        print(user_history)
        response = model.generate_content(request_text)
        return response.text