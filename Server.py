from flask import Flask
import logging
from datetime import datetime

app = Flask(__name__)
my_serial_num = 202311080001

logging.basicConfig(filename='app.log', level=logging.DEBUG)

file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)

app.logger.addHandler(file_handler)

@app.route('/', methods = ['GET', 'POST'])
def hello():
    return "hello"


@app.route('/make_cocktail/<string:UserID>/<string:cocktail_name>/<int:first>/<int:second>/<int:third>/<int:fourth>', methods = ['GET', 'POST'])
def make_cocktail(UserID, cocktail_name,first, second, third, fourth):
    current_date = datetime.now().strftime("%Y%m%d")
    if cocktail_name ==' ':
        return f"UserID: {UserID} Cocktail Name: CustomCocktail\nFirst: {first},\nSecond: {second},\nThird:{third},\nFourth:{fourth} date: {current_date}"
    else:
        return f"UserID: {UserID} Cocktail Name: {cocktail_name}\nFirst: {first},\nSecond: {second},\nThird:{third},\nFourth:{fourth} date: {current_date}"

if __name__=='__main__':
    app.run(host='192.168.0.104', port = 10000)
