
from flask import Flask, request
from service.straddleservice import StraddleService

app = Flask(__name__)
straddle_service = StraddleService()

@app.route('/data', methods=['POST'])
def get_data():
    data = request.json
    straddle_service.process_data(data)

if __name__ == '__main__':
    app.run(debug=True)
    