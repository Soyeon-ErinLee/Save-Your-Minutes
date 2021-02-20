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
from _file_transformer import SttTransformer

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
        time = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
        f = request.files.get('file')
        filename = secure_filename(f.filename)
        transcriber.upload(file_path, filename)
        data = transcriber.transribe(num_speaker) # have to check (after merging)
        front = SttTransformer(data).html_transfomer() # front value (to Soyeon)
        model = SttTransformer(data).model_transfomer(time) # input value for model (to Jihyeon)
    return render_template('homepage.html')  # 홈페이지를 나타내기 위한 파일.

@app.route("/result", methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(upload_dir, f.filename))
    return render_template('result.html')


if __name__ == '__main__':
    app.run(host = '0.0.0.0')
