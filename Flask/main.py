from flask import Flask, render_template, request, session, redirect, url_for
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import Admin
from flask_dropzone import Dropzone
from werkzeug.utils import secure_filename
import os
import sys
import time
import warnings

warnings.filterwarnings("ignore")
basedir = os.path.abspath(os.path.dirname(__file__))
upload_dir = os.path.join(basedir, 'static/uploads')
output_dir = os.path.join(basedir, 'output')
sys.path.append(os.path.join(os.path.dirname(basedir), 'Python_Modules'))
from _transcriber import TRANSCRIBER
from _file_transformer import SttTransformer
from make_tables import MAKE_TABLES

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
front = None
model = None
query_faq = {'table_top': {
    'Participants': 'who are the attendees at the meeting?',
    'Topic': 'what was the main topic of the meeting?',
    'num_agendas': 'How many ideas discussed?',
},
    'table_main1': {
        'Idea 1': 'what was the first idea?'
    },
    'table_main1_1': {
        'quest1': 'what can be advantage of the first idea?',
        'quest2': 'what is the problem of the first idea?',
        'quest3': 'what can be the possible solution for the first  idea?'
    },
    'table_main2': {
        'Idea 2': 'what was the second idea?'
    },
    'table_main2_1': {
        'quest1': 'what can be advantage of the second idea?',
        'quest2': 'what is the problem of the second idea?'
    }
}

@app.route("/", methods = ['GET', 'POST'])
def upload():
    if 'audio_file_name' not in session:
        session['audio_file_name'] = '.'
    if request.method == 'POST':
        audio_file_name = session['audio_file_name']
        if audio_file_name == '.':
            f = request.files.get('file')
            filename = secure_filename(f.filename)
            file_path = os.path.join(upload_dir, filename)
            f.save(file_path)
            session['audio_file_name'] = filename
            transcriber.upload(file_path, filename)
        else:
            session['num_speakers'] = request.form['speakers']
    return render_template('homepage.html')

@app.route("/result", methods = ['GET', 'POST'])
def result():
    path, file_type = transcribe()
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(upload_dir, f.filename))
    return render_template(
        'result.html', path = path, file_type = file_type
    )

@app.route("/result_interview", methods=['GET', 'POST'])
def result1():
    path, file_type = transcribe()
    mtl = MAKE_TABLES(query_faq['query_dict_agenda'], model, types="Agenda")
    mtl.get_table()
    with open(os.path.join(basedir, "templates/result.html"), "r", encoding="UTF-8") as file:
        result_1 = file.read()
    with open(os.path.join(basedir, "templates/result_0_1.html"), "r", encoding="UTF-8") as file:
        result_2 = file.read()
    with open(os.path.join(basedir, "templates/result_0.html"), "r", encoding="UTF-8") as file:
        result_3 = file.read()
    with open(os.path.join(upload_dir, "Output.txt"), 'r', encoding="UTF-8") as file:
        txt = file.read()
    result_1 += front
    result_1 += result_2
    result_1 += txt
    result_1 += result_3
    with open(os.path.join(basedir, "templates/final_result.html"), "w", encoding="UTF-8") as file:
        file.write(result_1)
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(upload_dir, f.filename))
    return render_template(
        'result1.html', path = path, file_type = file_type
    )

@app.route("/result_idea", methods=['GET', 'POST'])
def result2():
    path, file_type = transcribe()
    mtl = MAKE_TABLES(query_faq['query_dict_agenda'], model, types="Agenda")
    mtl.get_table()
    with open(os.path.join(basedir, "templates/result.html2"), "r", encoding="UTF-8") as file:
        result_1 = file.read()
    with open(os.path.join(basedir, "templates/result_1_1.html"), "r", encoding="UTF-8") as file:
        result_2 = file.read()
    with open(os.path.join(basedir, "templates/result_1.html"), "r", encoding="UTF-8") as file:
        result_3 = file.read()
    with open(os.path.join(upload_dir, "Output.txt"), 'r', encoding="UTF-8") as file:
        txt = file.read()
    result_1 += front
    result_1 += result_2
    result_1 += txt
    result_1 += result_3
    with open(os.path.join(basedir, "templates/final_result.html"), "w", encoding="UTF-8") as file:
        file.write(result_1)
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(upload_dir, f.filename))
    return render_template(
        'result2.html', path = path, file_type = file_type
    )

def transcribe():
    global front
    global model
    audio_file_name = session['audio_file_name']
    num_speakers = int(session['num_speakers'])
    session.pop('audio_file_name', None)
    path = 'uploads/' + audio_file_name
    file_type = 'audio/' + audio_file_name.rsplit('.')[-1]
    data = transcriber.transcribe(num_speakers)
    current_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
    front = SttTransformer(data).html_transfomer()  
    model = SttTransformer(data).model_transfomer(current_time)
    return path, file_type


if __name__ == '__main__':
    app.run(host = '0.0.0.0')
