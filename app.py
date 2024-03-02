from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'mp3'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        # File Upload
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({"message": "File uploaded successfully", "filename": filename}), 201
        else:
            return jsonify({"error": "Invalid file format"}), 400
    else:
        return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_file():
    if 'filename' not in request.json:
        return jsonify({"error": "No filename provided"}), 400
    filename = request.json['filename']
    if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        return jsonify({"error": "File not found"}), 404

    from main import run
    run(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    return jsonify({"message": "Processing initiated"}), 200

if __name__ == '__main__':
    app.run(debug=True)
