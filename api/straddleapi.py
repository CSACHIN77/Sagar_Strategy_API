import os
import json
from flask import Flask, request, jsonify


os.chdir('E:/Sagar_Strategy_API-main')
print(f"Changed directory to: {os.getcwd()}")

from repo.straddlerepo import StraddleRepo
try:
    from service.straddleservice import Strategyservice
except ImportError as e:
    print(f"Error importing StraddleService: {e}")

#Initialize Flask app
app = Flask(__name__)

with open('db.json', 'r') as f:
    data = json.load(f)
#print("Data from db.json:", data) 
#return jsonify(data), 200

# FOR PASSING THE DATA TO SERVICE
strategy_id = 29
strategy = Strategyservice(data,strategy_id)
#strategy.process_data(data,strategy_id)

# FOR GETTING THE DISTINCT STRATEGY NAMES
#strategy.getStrategyName()


#FOR GETTING THE STRATEGY DETAILS  # Replace 1 with the desired strategy_id
#strategy_details = strategy.getStrategyDetails(strategy_id)


@app.route('/get_strategy_name', methods=['GET'])
def get_data():
    #print("Data from db.json:", data) 
    #strategy = Strategyservice(data)
    strategy_name = strategy.getStrategyName()
    return jsonify(strategy_name), 200

@app.route('/save_strategy', methods=['POST'])
def save_strategy():
    strategy.process_data(data,strategy_id)
    return jsonify(data),200


@app.route('/get_strategy_details', methods=['GET'])
def get_strategy_details():
    #print("Data from db.json:", data) 
    #strategy = Strategyservice(data)
    strategy_details = strategy.getStrategyDetails(strategy_id)
    return jsonify(strategy_details), 200

try:
    if __name__ == '__main__':
        app.run(debug=True,use_reloader=False)
except SystemExit as e:
    print("SystemExit Exception:", e)
