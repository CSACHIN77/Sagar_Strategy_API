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

# Initialize Flask app
#app = Flask(__name__)

with open('db.json', 'r') as f:
    data = json.load(f)
#print("Data from db.json:", data) 
#return jsonify(data), 200

# FOR PASSING THE DATA TO SERVICE
#strategy = Strategyservice(data)
#strategy.process_data(data)

# FOR GETTING THE DISTINCT STRATEGY NAMES
repo = StraddleRepo()
repo.getStrategyName()

#FOR GETTING THE STRATEGY DETAILS
strategy_id = 23  # Replace 1 with the desired strategy_id
strategy_details = repo.getStrategyDetails(strategy_id)

# Print the strategy details
for row in strategy_details:
    print(row)

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
