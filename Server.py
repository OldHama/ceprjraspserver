from flask import Flask, request
import logging
from datetime import datetime

app = Flask(__name__)
my_serial_num = 202311080001

logging.basicConfig(filename='app.log', level=logging.DEBUG)

file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)

app.logger.addHandler(file_handler)

@app.route('/', methods=['GET', 'POST'])
def hello():
    return "hello"

@app.route('/make_cocktail/<string:UserID>/<string:cocktail_name>/<int:first>/<int:second>/<int:third>/<int:fourth>', methods=['POST'])
def make_cocktail(UserID, cocktail_name, first, second, third, fourth):
    current_date = datetime.now().strftime("%Y%m%d")

    if request.method == 'POST':
        # POST 요청의 데이터를 JSON 형식으로 파싱
        data = request.json
        
        if data:
            # 요청에서 받은 데이터를 이용하여 응답 생성
            if 'UserID' in data:
                UserID = data['UserID']
            if 'cocktail_name' in data:
                cocktail_name = data['cocktail_name']
            if 'first' in data:
                first = data['first']
            if 'second' in data:
                second = data['second']
            if 'third' in data:
                third = data['third']
            if 'fourth' in data:
                fourth = data['fourth']

            if cocktail_name == ' ':
                return f"UserID: {UserID} Cocktail Name: CustomCocktail\nFirst: {first},\nSecond: {second},\nThird:{third},\nFourth:{fourth} date: {current_date}"
            else:
                return f"UserID: {UserID} Cocktail Name: {cocktail_name}\nFirst: {first},\nSecond: {second},\nThird:{third},\nFourth:{fourth} date: {current_date}"
        else:
            return "POST 요청에 유효한 JSON 데이터가 필요합니다.", 400  # 잘못된 요청에 대한 응답
    else:
        return "GET 요청은 지원하지 않습니다.", 405  # 허용되지 않는 메서드에 대한 응답

if __name__ == '__main__':
    app.run(host='192.168.0.104', port=10000)
