import os
import json
import sys

current_directory = os.path.dirname('straddleapi.py')
# Construct the path to the parent directory
parent_directory = os.path.abspath(os.path.join(current_directory, '..'))
# Add the parent directory to the system path
sys.path.append(parent_directory)#os.chdir('D:/Rupendra/Work/Sagar/Sagar_Strategy_API')
#print(f"Changed directory to: {os.getcwd()}")
from repo.straddlerepo import StraddleRepo
from flask import Flask, request, jsonify
from flask_cors import CORS
# Change directory
#os.chdir('C:/Ajay')
#print(f"Changed directory to: {os.getcwd()}")

# Attempt to import StraddleRepo and Strategyservice
try:
    from repo.straddlerepo import StraddleRepo
except ImportError as e:
    print(f"Error importing StraddleRepo: {e}")

try:
    from service.straddleservice import Strategyservice
except ImportError as e:
    print(f"Error importing Strategyservice: {e}")

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route('/strategies/name', methods=['GET'])
def get_strategy_name():
    try:
        data=[]
        strategy = Strategyservice(data)
        strategy_name = strategy.getStrategyName()
        return jsonify(strategy_name), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/strategies', methods=['POST'])
def save_strategy():
    try:
        data = request.get_json()
        print("Received JSON data:", data)
        
        # Example processing (you might want to pass this data to Strategyservice)
        strategy = Strategyservice(data)
        strategy.process_insert_data(data)
        
        response = {
            "status": "success",
            "received_data": data
        }
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/strategies/<int:strategy_id>', methods=['PUT'])
def update_strategy(strategy_id):
    try:
        data = request.get_json()
        print("Received JSON data:", data)
        
        # Example processing (you might want to pass this data to Strategyservice)
        strategy = Strategyservice(data)
        strategy.process_update_data(data,strategy_id)
        
        
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Return single strategy
@app.route('/strategies/<int:strategy_id>', methods=['GET'])
def get_strategy_details(strategy_id):
    #print("Data from db.json:", data) 
    data =[]
    strategy = Strategyservice(data)
    #print('1')
    strategy_details = strategy.getStrategyDetails(strategy_id)
    
    return jsonify(strategy_details), 200

#Return all strategies
@app.route('/strategies', methods=['GET'])
def get_all_strategies():
    data =[]
    strategy = Strategyservice(data)
    #print('1')
    strategy_details = strategy.getAllStrategyDetails()
    
    return jsonify(strategy_details), 200

try:
    if __name__ == '__main__':
        app.run(debug=True,use_reloader=False)
except SystemExit as e:
    print("SystemExit Exception:", e)
