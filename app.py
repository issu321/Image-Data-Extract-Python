import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify, get_flashed_messages
from werkzeug.utils import secure_filename
from ocr_engine import OCREngine
from utils import allowed_file, export_to_txt

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'image-data-extract-secret-key-2024')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

UPLOAD_FOLDER = os.path.join('static', 'uploads')
EXTRACTED_FOLDER = 'extracted'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'bmp', 'tiff'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXTRACTED_FOLDER, exist_ok=True)

ocr_engine = OCREngine()

# In-memory cache for OCR results (ephemeral, per-container instance)
_results_cache = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/features')
def features():
    return render_template('features.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        flash('No image file provided', 'error')
        return redirect(url_for('index'))

    file = request.files['image']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
        filename = secure_filename(file.filename)
        unique_name = f"{uuid.uuid4().hex}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
        file.save(filepath)
        return redirect(url_for('analyze_page', image=unique_name))
    else:
        flash('Invalid file type. Allowed: PNG, JPG, JPEG, WEBP, BMP, TIFF', 'error')
        return redirect(url_for('index'))


@app.route('/analyze/<image>')
def analyze_page(image):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image)
    if not os.path.exists(image_path):
        flash('Image not found or expired', 'error')
        return redirect(url_for('index'))
    return render_template('result.html', image=image, analyzing=True)


@app.route('/api/analyze/<image>', methods=['POST'])
def api_analyze(image):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image)

    if not os.path.exists(image_path):
        return jsonify({'error': 'Image file not found'}), 404

    try:
        result = ocr_engine.process_image(image_path)
        _results_cache[image] = result
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/result/<image>')
def result_page(image):
    if image not in _results_cache:
        flash('No analysis results available', 'error')
        return redirect(url_for('index'))
    return render_template('result.html',
                           image=image,
                           result=_results_cache[image],
                           analyzing=False)


@app.route('/download/<image>')
def download(image):
    if image not in _results_cache:
        flash('No extracted text available', 'error')
        return redirect(url_for('index'))

    text = _results_cache[image]['text']
    lang = _results_cache[image].get('language', 'unknown')
    filename = f"extracted_text_{lang}.txt"
    filepath = os.path.join(EXTRACTED_FOLDER, filename)

    export_to_txt(text, filepath)
    return send_file(filepath, as_attachment=True, download_name='extracted_text.txt')


@app.route('/clear/<image>')
def clear(image):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image)
    if os.path.exists(image_path):
        os.remove(image_path)
    if image in _results_cache:
        del _results_cache[image]
    return redirect(url_for('index'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 7860))
    app.run(debug=False, host='0.0.0.0', port=port)
