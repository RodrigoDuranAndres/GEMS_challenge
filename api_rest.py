from flask import Flask, request, jsonify
from utils.methods import *
from utils.clases import *

app = Flask(__name__)

@app.route('/dispatch', methods=['POST'])
def dispatch():
    data = request.get_json()
    # Do something with the data
    respuesta = procesar_json(data)
   
    try: 
        return jsonify(respuesta)
    except:
        return jsonify("Nada")

if __name__ == '__main__':
    app.run(port=8808)