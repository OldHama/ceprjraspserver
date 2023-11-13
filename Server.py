from flask import Flask, request, jsonify
import logging
from datetime import datetime
import actuator
import neo_act as n
import threading

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
        recipeTitle = data.get('recipeTitle')
        first = data.get('first')
        second = data.get('second')
        third = data.get('third')
        fourth = data.get('fourth')
        Serial_Number = data.get('Serial_Number')

        if all([UserID, recipeTitle, first, second, third, fourth]):
            current_date = datetime.now().strftime("%Y%m%d")
            
            pumps = actuator.pumps
            timings = [first, second, third, fourth]
            for pump in pumps:
                actuator.g.output(pump, True)
                if pump == actuator.pump1:
					actuator.sleep(first//15*1.5)
				elif pump == actuator.pump2:
					actuator.sleep(second//15*1.5)
				elif pump == actuator.pump3:
					actuator.sleep(third//15*1.5)
				else:
					actuator.sleep(fourth//15*1.5) 
					
                actuator.sleep(3)
                actuator.g.output(pump, False)
            
            return jsonify({
                'UserID':UserID,
                'recipeTitle': recipeTitle,
                'date' : current_date
            })
        else:
            return "Invalid JSON data", 400
    else:
        return "JSON data is required", 400

if __name__ == '__main__':
    actuator.setup()
    threading.Thread(target=lambda:n.make_rainbow(0.001)).start()
    app.run(host='192.168.0.104', port=10000)
