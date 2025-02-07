from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from main import load_config
from enhanced_analysis import EnhancedCodeSage
from improved_reporting import generate_detailed_report
from parallel_processing import analyze_files_parallel

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    files = request.files.getlist('file')
    file_paths = []
    for file in files:
        if file.filename == '':
            continue
        if file and file.filename.endswith('.py'):
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)
            file.save(file_path)
            file_paths.append(file_path)

    if not file_paths:
        return jsonify({'error': 'No valid Python files uploaded'})

    config = load_config('config.yaml')
    results = analyze_files_parallel(file_paths, config)

    # Generate detailed report
    report = generate_detailed_report(results)

    # Clean up uploaded files
    for file_path in file_paths:
        try:
            os.remove(file_path)
        except PermissionError:
            print(f"Could not delete {file_path}. It will be deleted later.")

    return report

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)