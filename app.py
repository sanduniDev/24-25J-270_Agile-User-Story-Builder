from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from extractor import extract_requirements
from preprocessor import preprocess_text, load_noise_dataset

# Flask app configuration
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data/Conversations/'
app.config['ALLOWED_EXTENSIONS'] = {'txt'}


def allowed_file(filename):
    """Check if the uploaded file is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    """Render the file upload form."""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and processing."""
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(filepath)

        # Load the noise dataset
        noise_phrases = load_noise_dataset("data/noise_dataset.csv")

        # Extract tasks, subtasks, and NFRs
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        preprocessed_content = "\n".join([preprocess_text(line, noise_phrases) for line in content.splitlines()])
        tasks, subtasks, nfrs = extract_requirements(preprocessed_content)

        tasks_and_subtasks = {task: subtasks.get(task, []) for task in tasks}

        return render_template('results.html', filename=filename, tasks_and_subtasks=tasks_and_subtasks, nfrs=nfrs)

    return redirect(request.url)


if __name__ == '__main__':
    app.run(debug=True)
