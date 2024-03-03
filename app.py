from flask import Flask, request, jsonify, render_template, session
import os
from werkzeug.utils import secure_filename
from subprocess import Popen, PIPE
import json
from main import run  
from openai import OpenAI
from flask import redirect, url_for
client = OpenAI()
global summary
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'mp3'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            run(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Call run function here with the uploaded file
            return jsonify({"message": "File uploaded successfully", "filename": filename}), 201
        else:
            return jsonify({"error": "Invalid file format"}), 400
    else:
        return render_template('index.html')
@app.route('/query', methods=['POST']) 
def submit_query():
    query = request.form['query']
    import os
    from dotenv import load_dotenv

    load_dotenv()
    TOKEN = os.getenv("token")
    command = [
        "grpcurl",
        "-H",
        "Authorization: Bearer {}".format(token),
        "-d",
        '{"query": {"semantic_query": "' + query + '"}, "count": 5}',
        "--proto",
        "./chunks.proto",
        "--proto",
        "./Search.proto",
        "grpc.staging.redactive.ai:443",
        "redactive.grpc.v1.Search/QueryChunks"
    ]

    process = Popen(command, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        output_json = stdout.decode()
        data = json.loads(output_json)
        chunk_body = data['relevantChunks'][0]['chunkBody']

        role = "You are a lecturer who is able to explain concepts in easy-to-understand ways. Please avoid adding extra information, specify when information is not from the given context."

        completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"{role}"},
                    {"role": "user", "content": f"{chunk_body}"}
                ]
            )
        transcript = completion.choices[0].message.content
        print(transcript)

        return render_template('notes.html', query=query, transcript=transcript)

    else:
        return jsonify({"error": stderr.decode()}), 500


@app.route('/notes')
def notes():
    return render_template('notes.html')


@app.route('/process', methods=['POST'])
async def process_file():
    if 'filename' not in request.json:
        return jsonify({"error": "No filename provided"}), 400
    filename = request.json['filename']
    if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        return jsonify({"error": "File not found"}), 404

    summary = run(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    session['summary'] = summary
    print(session['summary'])

    return jsonify({"message": "Processing initiated"}), 200

if __name__ == '__main__':
    app.run(debug=True)
