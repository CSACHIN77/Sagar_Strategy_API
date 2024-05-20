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

@app.route('/get_strategy_name', methods=['GET'])
def get_strategy_name():
    try:
        data=[]
        strategy = Strategyservice(data)
        strategy_name = strategy.getStrategyName()
        return jsonify(strategy_name), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/save_strategy', methods=['POST'])
def save_strategy():
    try:
        data = request.get_json()
        print("Received JSON data:", data)
        
        # Example processing (you might want to pass this data to Strategyservice)
        strategy = Strategyservice(data)
        strategy.process_data(data)
        
        response = {
            "status": "success",
            "received_data": data
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_strategy_details/<int:strategy_id>', methods=['GET'])
def get_strategy_details(strategy_id):
    #print("Data from db.json:", data) 
    data =[]
    strategy = Strategyservice(data)
    print('1')
    strategy_details = strategy.getStrategyDetails(strategy_id)
    
    return jsonify(strategy_details), 200

try:
    if __name__ == '__main__':
        app.run(debug=True,use_reloader=False)
except SystemExit as e:
    print("SystemExit Exception:", e)
