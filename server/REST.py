import os
import sys
import ast
import pandas as pd
from hashlib import md5
from __init__ import app
from werkzeug.utils import secure_filename
from geo_tools.geo_tools import Geotools
from server.pipelines import ResultsPipelines
from flask import jsonify, request, flash, redirect

ALLOWED_EXTENSIONS = {'csv'}
RESPONSE_DICT = {'links': [],
                 'points': [],
                 'result_id': ''}


def allowed_file(filename):
    return filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/getAddress', methods=['GET', 'POST'], strict_slashes=False)
def get_address():
    """
    This is the getAddress route endpoint.
        :param: GET:
        :param: POST: CSV FILE
        :return: if csv provided returns json containing points and links. else renders page as upload page
        """
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            result_id = md5(str(df).encode()).hexdigest()
            cache = ResultsPipelines().check_uuid(result_id)
            resp = RESPONSE_DICT.copy()
            if cache:
                resp['links'] = ast.literal_eval(cache.links)
                resp['points'] = ast.literal_eval(cache.points)
                resp['result_id'] = cache.uuid
                return jsonify(resp)

            else:
                res = Geotools(df).dokka_task()
                ResultsPipelines().insert_uuid(uuid=result_id, links=res['links'], points=res['points'])
                return jsonify(res)

    return '''
    <!doctype html>
    <title>Upload a CSV File</title>
    <h1>Upload a CSV File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/api/getResult', methods=['GET'], strict_slashes=False)
def get_result():
    """
    :param: GET:
    :return: a dictionary containing links and points if the result_id is already in the database
    """
    res = request.args
    if 'result_id' not in res:
        return jsonify({'error': {'status_code': 406, 'description': 'the query you have entered is not valid'}})
    cache = ResultsPipelines().check_uuid(res['result_id'])
    resp = RESPONSE_DICT.copy()
    if cache:
        resp['links'] = ast.literal_eval(cache.links)
        resp['points'] = ast.literal_eval(cache.points)
        resp['result_id'] = cache.uuid
        return jsonify(resp)
    else:
        resp['result_id'] = res['result_id']
        return jsonify(resp)


if __name__ == '__main__':
    app.run(debug=False)
