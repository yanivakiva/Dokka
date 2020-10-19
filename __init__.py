import os
from flask import Flask

UPLOAD_FOLDER = f'{os.getcwd()}/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dokka.db'
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
