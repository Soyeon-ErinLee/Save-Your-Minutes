from flask import Flask, render_template, request
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import Admin
from flask_dropzone import Dropzone  # drop box
import os


app = Flask(__name__)
app.debug = True

basedir = os.path.abspath(os.path.dirname(__file__))  
upload_dir = os.path.join(basedir, 'uploads')
output_dir = os.path.join(basedir, 'output')


admin = Admin(name='Uploaded Files')
admin.init_app(app) 
dropzone = Dropzone(app)
admin.add_view(FileAdmin(upload_dir, name='FILES'))
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'audio/*, .mp3, .wav, .m4a'


@app.route("/", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(upload_dir, f.filename))
    return render_template('homepage.html')


@app.route("/result", methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(upload_dir, f.filename))
    return render_template('result.html')


if __name__ == '__main__':
    app.run(host = '0.0.0.0')
