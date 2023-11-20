from flask import Flask, request, jsonify
import logging
from datetime import datetime
import actuator
import neo_act as n
import threading
import socket
import requests
from multiprocessing import Process

               
app = Flask(__name__)
my_serial_num = 202311080001
url = 'http://ceprj.gachon.ac.kr:60005/'
status = "waiting"
prev_ip_address = 'address'



logging.basicConfig(filename='app.log', level=logging.DEBUG)

file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)

app.logger.addHandler(file_handler)

def parse(just_string):
    just_string = str(just_string)
    just_string.replace('ml', '')
    
    return int(just_string)

def send_ip():
    global prev_ip_address, ip_address, server
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
                server.terminate()
                server.join()
                server = Process(target = lambda: app.run(host = ip_address, port = 10000))
                server.start()
                send_status()
                
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
    global neopixel_t1
    neopixel_t1.change_pattern("123")
    return "hello"

@app.route('/set_brightness', methods=['POST', 'GET'])
def set_brightness():
    global bright
    
    data = request.json
    if data:
        print("GOT SOMETHING")
        bright = data.get("brightness")
        
    return jsonify({
                "brightness": bright
            })
    
@app.route('/make_cocktail', methods=['POST', 'GET'])
def make_cocktail():
    global status
    data = request.json
    
    if data:
        UserID = data.get('UserID')
        recipeTitle = data.get('recipeTitle')
        first = parse(data.get('first'))
        second = parse(data.get('second'))
        third = parse(data.get('third'))
        fourth = parse(data.get('fourth'))
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
                    actuator.sleep(int(first)//15*sec)
                elif pump == actuator.pump2:
                    actuator.sleep(int(second)//15*sec)
                elif pump == actuator.pump3:
                    actuator.sleep(int(third)//15*sec*0.6)
                else:
                    actuator.sleep(int(fourth)//15*sec)

                actuator.g.output(pump, False)
            status = "done"
            send_status()
            status = "waiting"
            send_status()
            return jsonify({
                'UserID':UserID,
                'recipeTitle': recipeTitle,
                'date' : current_date,
                'success' : True
            })
        else:
            return jsonify({
                'success' : False
            })
    else:
        return jsonify({
            'success' : False
        })
def make_pattern(timing, bright):
    global pattern
    while True:
        ledpattern = pattern
        if ledpattern == 'rainbow':
            n.rainbow_cycle(timing, bright)
            print('ledpatter:',ledpattern,"pattenr:",pattern)
        else:
            n.off()
        actuator.sleep(0.001)

class led_thread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.pattern = 'rainbow'
        self.timing = 0.001
        self.bright = 0.8
    def run (self):
        while True:
            if self.pattern == 'rainbow':
                n.rainbow_cycle(self.timing, self.bright)
            else:
                n.off()
            actuator.sleep(0.001)
            
    def change_pattern(self, new_pattern):
            self.pattern = new_pattern
            print("123")
        
        
        
if __name__ == '__main__':
    
    actuator.setup()
    ip_address = get_ip_address()
    print("My IP Address is:", ip_address)

    threading.Thread(target=send_ip).start()
    #led_thread = threading.Thread(target=lambda:make_pattern(0.001, 0.5))
    neopixel_t1 = led_thread('Thread 1')
    neopixel_t1.start()
    
    server = Process(target = lambda: app.run(host = ip_address, port = 10000))
    server.start()
    send_status()
    neopixel_t1.change_pattern("123")
    actuator.sleep(3)
    neopixel_t1.change_pattern("rainbow")
