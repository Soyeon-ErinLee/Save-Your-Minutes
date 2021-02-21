from flask import Flask, render_template, request, session, redirect, url_for
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import Admin
from flask_dropzone import Dropzone
from werkzeug.utils import secure_filename
import os
import sys
import time


basedir = os.path.abspath(os.path.dirname(__file__))
upload_dir = os.path.join(basedir, 'static/uploads')
output_dir = os.path.join(basedir, 'output')


app = Flask(__name__)
app.debug = True

admin = Admin(name = 'Uploaded Files')
admin.init_app(app) 
dropzone = Dropzone(app)
admin.add_view(FileAdmin(upload_dir, name = 'FILES'))
app.config.from_pyfile('config.py')
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'audio/*, .mp3, .wav, .m4a'

@app.route("/", methods = ['GET', 'POST'])
def upload():
    session.clear()
    return render_template('homepage.html')

if __name__ == '__main__':
    app.run(host = '0.0.0.0')