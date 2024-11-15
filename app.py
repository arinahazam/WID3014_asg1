from flask import Flask, request, jsonify, render_template
from analyze import read_image
from dotenv import load_dotenv
import os

load_dotenv()

endpoint=os.getenv("azure_endpoint")
key= os.getenv("azure_key")

if not key or endpoint:
    raise ValueError("missing")

app = Flask(__name__, template_folder='templates')

@app.route("/")
def home():
    return render_template('index.html')


# API at /api/v1/analysis/ 
@app.route("/api/v1/analysis/", methods=['GET'])
def analysis():
    # Try to get the URI from the JSON
    try:
        get_json = request.get_json()
        image_uri = get_json['uri']
    except:
        return jsonify({'error': 'Missing URI in JSON'}), 400
    
    # Try to get the text from the image
    try:
        res = read_image(image_uri)
        
        response_data = {
            "text": res
        }
    
        return jsonify(response_data), 200
    except:
        return jsonify({'error': 'Error in processing'}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)