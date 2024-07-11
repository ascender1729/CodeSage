from flask import Flask, render_template, request, jsonify
from main import CodeSage, load_config
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        config = load_config('config.yaml')
        sage = CodeSage(config)
        issues = sage.analyze_file(file_path)
        os.remove(file_path)  # Remove the uploaded file after analysis
        return jsonify(issues)

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)