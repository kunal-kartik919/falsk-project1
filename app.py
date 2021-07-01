from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, Time
import os
from flask_marshmallow import Marshmallow

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'student.db')

db = SQLAlchemy(app)
ma = Marshmallow(app)



class Student(db.Model):
    __tablename__ = 'student'
    student_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    phone_number = Column(Integer, unique=True)


@app.cli.command('db_seed')
def db_seed():

    kartikey = Student(first_name=' kartikey',
                       last_name='kunal',
                       email='kunal@gmail.com',
                       phone_number=10)

    sonali = Student(first_name='sonali',
                     last_name='choudhary',
                     email='sonali@gmail.com',
                     phone_number=90)

    db.session.add(kartikey)
    db.session.add(sonali)
    db.session.commit()
    print('database seeded')


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print("database created")


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('database removed')


@app.route('/students', methods=['GET'])
def students():
    student_list = Student.query.all()
    result = students_schema.dump(student_list)
    return jsonify(result.data)


@app.route('/find_student/<int:student_id>', methods=['GET'])
def find_student(student_id: int):
    student = Student.query.filter_by(student_id=student_id).first()
    if student:
        result = student_schema.dump(student)
        return jsonify(result.data)
    else:
        return jsonify(message='student does not exist')


@app.route('/add_student', methods=['POST'])
def add_student():
    email = request.form['email']
    test = Student.query.filter_by(email=email).first()
    if test:
        return jsonify(message='Email already in use')
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']

        new_student = Student(first_name=first_name,
                              last_name=last_name,
                              email=email,
                              phone_number=phone_number)

        db.session.add(new_student)
        db.session.commit()
        return jsonify(message='new student added')


@app.route('/update_student', methods=['PUT'])
def update_student():
    student_id = int(request.form['student_id'])
    student = Student.query.filter_by(student_id=student_id).first()
    if student:
        student.first_name = request.form['first_name']
        student.last_name = request.form['last_name']
        student.email = request.form['email']
        student.phone_number = int(request.form['phone_number'])
        db.session.commit()
        return jsonify(message='you updated ')
    else:
        return jsonify(message='no record found')


@app.route('/remove_student/<int:student_id>',methods=['DELETE'])
def remove_student(student_id:int):
    student = Student.query.filter_by(student_id=student_id).first()
    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify(message='data deleted')
    else:
        return jsonify(message='data not present')

class StudentSchema(ma.Schema):
    class Meta:
        fields = ('student_id', 'first_name', 'last_name', 'email', 'phone_number')


student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

if __name__ == '__main__':
    app.run()
