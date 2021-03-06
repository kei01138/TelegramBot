from flask import Flask, request
import requests, random
from decouple import config
app = Flask(__name__)

# Telegram
token = config('TELE_TOKEN')
api_url = f'https://api.telegram.org/bot{token}'

# Naver
NAVER_CLIENT_ID = config('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = config('NAVER_CLIENT_SECRET')
papago_url = 'https://openapi.naver.com/v1/papago/n2mt'


@app.route(f'/{token}', methods=["POST"])
def telegram():
  # request.args # GET
  # request.forms # POST
  # print(request.get_json())

  # lotto('key) # => value, 'key'가 없다면 예외 발생
  # lotto.get('key') # => value, 'key'가 없다면 none 반환
  message = request.get_json().get('message')
  print(message)

  # data 가져오기
  if message is not None:
    chat_id = message.get('from').get('id')
    text = message.get('text')
    # 1. 로또
    if text == "로또":
      text = random.sample(range(1,46),6)
    # 2. 네이버 번역
    # /번역 안녕하세요!
    if text[0:4] == '/번역 ':   
      headers = {
        'X-Naver-Client-id': NAVER_CLIENT_ID,
        'X-Naver-Client-Secret': NAVER_CLIENT_SECRET
      }
      data = {
        'source': 'ko',
        'target': 'en',
        'text': text[4:]
      }
      papago_res = requests.post(papago_url, headers=headers, data=data)
      text = papago_res.json().get('message').get('result').get('translatedText')
      
      
      
      
    send_url = f'{api_url}/sendMessage?chat_id={chat_id}&text={text}'
      
    # sendMessage 요청 보내기
    response = requests.get(send_url)
  
  return '', 200 # body, status_code

if __name__ == '__main__':
  app.run(debug=True)