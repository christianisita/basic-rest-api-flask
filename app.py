from flask import Flask, jsonify, abort, make_response, request
import sys
import os
from werkzeug.utils import secure_filename
import urllib.request
import logging

PHOTOS_FOLDER = "./files"

app = Flask(__name__)
app.config['PHOTOS_FOLDER'] = PHOTOS_FOLDER
logging.basicConfig(level=logging.DEBUG)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


student_data = [
    {
        'id' : 1,
        'name' : 'Clara Anderson',
        'score' : 95,
        'image_path' : ""
    },
    {
        'id' : 2,
        'name' : 'Denisse Lawson',
        'score' : 55,
        'image_path' : ""
    }
]

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/studentdatabank/api/v1.0/students', methods=['GET'])
def get_student():
    return jsonify({'students': student_data})

@app.route('/studentdatabank/api/v1.0/students/<int:student_id>', methods=['GET'])
def get_student_id(student_id):
    student = [data for data in student_data if data['id'] == student_id]
    if len(student) == 0:
        abort(404)
    return jsonify({'student': student[0]})

@app.route('/studentdatabank/api/v1.0/create', methods=['POST'])
def create_data():
    if not request.json or not 'name' in request.json or not 'score' in request.json:
        abort(400)
    student = {
        'id' : student_data[-1]['id'] + 1,
        'name' : request.json['name'],
        'score' : request.json['score'],
        'image_path' : ""
    }
    student_data.append(student)
    return jsonify(({'student': student}), 201)

@app.route('/studentdatabank/api/v.1.0/students/edit/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = [data for data in student_data if data['id'] == student_id]
    print(student[0], file=sys.stdout)
    if len(student) == 0:
        abort(404)
    if not request.json:
        abort(400)
    student[0]['name'] = request.json.get('name', student[0]['name'])
    student[0]['score'] = request.json.get('score', student[0]['score'])
    return jsonify({'student': student[0]})

@app.route('/studentdatabank/api/v.1.0/students/delete/<int:student_id>', methods=['DELETE'])
def delete_task(student_id):
    student = [data for data in student_data if data['id'] == student_id]
    if len(student) == 0:
        abort(404)
    student_data.remove(student[0])
    return jsonify({'result' : 'Student data has sucessfully deleted!'})

@app.route('/studentdatabank/api/v.1.0/upload', methods=['POST'])
def upload():
    # file = request.files['file']
    # if '' not in request.files:
    #     return jsonify({'message' : 'File not found'})
    file = request.files['']
    # if file.filename == '':
    #     resp = jsonify({'message' : 'No file selected for uploading'})
    #     resp.status_code = 400
    #     return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['PHOTOS_FOLDER'], filename))
        resp = jsonify({'message' : 'File successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp
    # filename = secure_filename(file.filename)
    # print(str(filename), flush=True)
    # app.logger.info('hello')
    # #flash('hello')
    # file.save(os.path.join('PHOTOS_FOLDER', filename))
    # return jsonify({'message' : 'File sucessfully uploaded'})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error' : 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error' : 'Bad Request'}), 400)

if __name__ == '__main__':
    app.run(debug=True)