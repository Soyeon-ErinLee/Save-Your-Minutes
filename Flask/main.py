from flask import Flask, render_template, request
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import Admin
from flask_dropzone import Dropzone
from werkzeug.utils import secure_filename
import os
import sys


basedir = os.path.abspath(os.path.dirname(__file__))
upload_dir = os.path.join(basedir, 'uploads')
output_dir = os.path.join(basedir, 'output')
sys.path.append(os.path.join(os.path.dirname(basedir), 'Python_Modules'))
from _transcriber import TRANSCRIBER

app = Flask(__name__)
app.debug = True

admin = Admin(name='Uploaded Files')
admin.init_app(app) 
dropzone = Dropzone(app)
admin.add_view(FileAdmin(upload_dir, name='FILES'))
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'audio/*, .mp3, .wav, .m4a'

transcriber = TRANSCRIBER()

@app.route("/", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        filename = secure_filename(f.filename)
        transcriber._upload(f, filename)
    return render_template('homepage.html')

@app.route("/result", methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(upload_dir, f.filename))
    return render_template('result.html')


if __name__ == '__main__':
    app.run(host = '0.0.0.0')
