from flask import Flask, render_template, request, session
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import Admin
from flask_dropzone import Dropzone
from werkzeug.utils import secure_filename
import os
import sys


basedir = os.path.abspath(os.path.dirname(__file__))
upload_dir = os.path.join(basedir, 'static/uploads')
output_dir = os.path.join(basedir, 'output')
sys.path.append(os.path.join(os.path.dirname(basedir), 'Python_Modules'))
from _transcriber import TRANSCRIBER

app = Flask(__name__)
app.debug = True

admin = Admin(name = 'Uploaded Files')
admin.init_app(app) 
dropzone = Dropzone(app)
admin.add_view(FileAdmin(upload_dir, name = 'FILES'))
app.config.from_pyfile('config.py')
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'audio/*, .mp3, .wav, .m4a'

transcriber = TRANSCRIBER()

@app.route("/", methods = ['GET', 'POST'])
def upload():
    if 'audio_file_name' not in session:
        session['audio_file_name'] = '.'
    if request.method == 'POST':
        f = request.files.get('file')
        filename = secure_filename(f.filename)
        file_path = os.path.join(upload_dir, filename)
        f.save(file_path)
        session['audio_file_name'] = filename
        transcriber._upload(file_path, filename)
    return render_template('homepage.html')

@app.route("/result", methods = ['GET', 'POST'])
def result():
    path, file_type = insert_audio()
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(upload_dir, f.filename))
    return render_template(
        'result.html', path = path, file_type = file_type
    )

@app.route("/result_interview", methods=['GET', 'POST'])
def result1():
    path, file_type = insert_audio()
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(upload_dir, f.filename))
    return render_template(
        'result1.html', path = path, file_type = file_type
    )

@app.route("/result_idea", methods=['GET', 'POST'])
def result2():
    path, file_type = insert_audio()
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(upload_dir, f.filename))
    return render_template(
        'result2.html', path = path, file_type = file_type
    )

def insert_audio():
    audio_file_name = session['audio_file_name']
    session.pop('audio_file_name', None)
    path = 'uploads/' + audio_file_name
    file_type = 'audio/' + audio_file_name.rsplit('.')[-1]
    return path, file_type

if __name__ == '__main__':
    app.run(host = '0.0.0.0')
