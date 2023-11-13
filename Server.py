from flask import Flask, request, jsonify
import logging
from datetime import datetime
import actuator
import neo_act as n
import threading
import socket
import requests


app = Flask(__name__)
my_serial_num = 202311080001
url = 'http://ceprj.gachon.ac.kr:60005/'
status = "waiting"
prev_ip_address = 'address'


logging.basicConfig(filename='app.log', level=logging.DEBUG)

file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)

app.logger.addHandler(file_handler)

def send_ip():
    global prev_ip_address, ip_address
    url = 'http://ceprj.gachon.ac.kr:60005/device/send_ip'
    
    while True:
        try:
            ip_address = get_ip_address()
            json_data = {
            "serial_number": my_serial_num,
            "ip_address": ip_address
            }
            if prev_ip_address != ip_address:
                response = requests.post(url, json=json_data)
                print(response.text)
                prev_ip_address = ip_address
        except:
            print("sth wnet wrong :(")
        actuator.sleep(1)
        
def send_status():
    url = 'http://ceprj.gachon.ac.kr:60005/device/send_status' 
    json_data = {
    "serial_number": my_serial_num,
    "status": status 
    }
    response = requests.post(url, json=json_data)
    print(response.text)

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

@app.route('/', methods=['GET', 'POST'])
def hello():
    return "hello"

@app.route('/make_cocktail', methods=['POST', 'GET'])
def make_cocktail():
    global status
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
            
            status = "inprogress"
            send_status()
            
            pumps = actuator.pumps
            timings = [first, second, third, fourth]
            sec = 7.5
            for pump in pumps:
                actuator.g.output(pump, True)
                if pump == actuator.pump1:
                    actuator.sleep(first//15*sec)
                elif pump == actuator.pump2:
                    actuator.sleep(second//15*sec)
                elif pump == actuator.pump3:
                    actuator.sleep(third//15*sec*0.6)
                else:
                    actuator.sleep(fourth//15*sec)

                actuator.g.output(pump, False)
            status = "done"
            send_status()
            status = "waiting"
            send_status()
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
    ip_address = get_ip_address()
    print("My IP Address is:", ip_address)
    threading.Thread(target=send_ip).start()
    threading.Thread(target=lambda:n.make_rainbow(0.001)).start()
    send_status()
    app.run(host=ip_address, port=10000)

