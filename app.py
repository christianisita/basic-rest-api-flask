from flask import Flask, jsonify, abort, make_response, request
import sys

app = Flask(__name__)

student_data = [
    {
        'id' : 1,
        'name' : 'Clara Anderson',
        'score' : 95
    },
    {
        'id' : 2,
        'name' : 'Denisse Lawson',
        'score' : 55
    }
]

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
        'score' : request.json['score']
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

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error' : 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error' : 'Bad Request'}), 400)

if __name__ == '__main__':
    app.run(debug=True)