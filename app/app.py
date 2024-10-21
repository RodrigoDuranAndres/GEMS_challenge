from flask import Flask, request, jsonify
from utils.methods_advance import *
from utils.classes import *

app = Flask(__name__)

@app.route('/productionplan', methods=['POST'])
def dispatch():
    data = request.get_json()
    # Do something with the data
    response = process_json(data)
   
    try: 
        return jsonify(response)
    except:
        return jsonify("Nothing")

if __name__ == '__main__':
    app.run(port=8808)