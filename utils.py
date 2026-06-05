import os
from werkzeug.utils import secure_filename


def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_uploaded_file(file, upload_folder, allowed_extensions):
    if file and allowed_file(file.filename, allowed_extensions):
        filename = secure_filename(file.filename)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        return filepath
    return None


def export_to_txt(text, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    return filepath


def format_text_stats(text):
    if not text:
        return {'characters': 0, 'words': 0, 'lines': 0}
    return {
        'characters': len(text),
        'words': len(text.split()),
        'lines': len(text.splitlines())
    }
