import os
from flask import Flask, request, jsonify, render_template
from analyze import read_image

app = Flask(__name__, template_folder='templates')

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

# New endpoint to handle file upload from the web interface
@app.route("/upload", methods=['POST'])
def upload_and_analyze():
    """Handle file uploads and analyze the image."""
    if 'file' not in request.files or request.files['file'].filename == '':
        return "❌ No file selected."

    file = request.files['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Process the uploaded image
    try:
        res = read_image(file_path)
        return f"✅ File uploaded and processed successfully! Extracted Text: {res}"
    except:
        return "❌ Error in processing."


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
