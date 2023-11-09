from flask import Flask, request, jsonify
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

@app.route('/make_cocktail', methods=['POST', 'GET'])
def make_cocktail():
    data = request.json
    
    if data:
        UserID = data.get('UserID')
        cocktail_name = data.get('cocktail_name')
        first = data.get('first')
        second = data.get('second')
        third = data.get('third')
        fourth = data.get('fourth')

        if all([UserID, cocktail_name, first, second, third, fourth]):
            current_date = datetime.now().strftime("%Y%m%d")
            return jsonify({
                'UserID': UserID,
                'cocktail_name': cocktail_name,
                'first': first,
                'second': second,
                'third': third,
                'fourth': fourth
            })
        else:
            return "Invalid JSON data", 400
    else:
        return "JSON data is required", 400

if __name__ == '__main__':
    app.run(host='192.168.0.104', port=10000)

