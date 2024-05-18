import os
import json
from flask import Flask, request, jsonify


os.chdir('E:/Sagar_Strategy_API-main')
print(f"Changed directory to: {os.getcwd()}")

try:
    from service.straddleservice import Strategyservice
except ImportError as e:
    print(f"Error importing StraddleService: {e}")

# Initialize Flask app
#app = Flask(__name__)

with open('db.json', 'r') as f:
    data = json.load(f)
#print("Data from db.json:", data) 
#return jsonify(data), 200
strategy = Strategyservice(data)
strategy.process_data(data)
#print(strategy)

'''
@app.route('/get_data', methods=['POST'])
def get_data():
    with open('db.json', 'r') as f:
        data = json.load(f)
    #print("Data from db.json:", data) 
    return jsonify(data), 200
    strategy_instance = Strategy()
    strategy_instance.process_data(data)
'''

#if __name__ == '__main__':

    #app.run(debug=True)
