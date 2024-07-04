from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from PIL import Image
from modeltest import classify

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

@app.route('/predict', methods=["POST", "GET"], strict_slashes=False)
@cross_origin()
def predict():
    if request.is_json:
        data = request.json.get('data', None)
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
    
        image_data = base64.b64decode(data.split(',')[1])
        image = Image.open(BytesIO(image_data))
        image_np = np.array(image)
        
        return jsonify({"prediction": classify(image_np)}), 200
    else:
        return jsonify({"error": "Request must be JSON"}), 415

if __name__ == '__main__':
    app.run(debug=True)
