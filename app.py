from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from datetime import datetime


# Load environment variables
load_dotenv()


# Initialise Flask and SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TASK_TRACKER_DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Mission(db.Model):
    __tablename__ = 'missions'

    MissionID = db.Column(db.Integer, primary_key=True)
    QuestID = db.Column(db.Integer, db.ForeignKey('quests.QuestID'), nullable=False)
    StudentID = db.Column(db.Integer, db.ForeignKey('student.StudentID'), nullable=False)
    MissionTitle = db.Column(db.String(255))
    MissionDescription = db.Column(db.Text)
    MissionDueDate = db.Column(db.DateTime)

    quest = db.relationship('Quest', back_populates='missions')
    student = db.relationship('Student', back_populates='missions')


class Quest(db.Model):
    __tablename__ = 'quests'

    QuestID = db.Column(db.Integer, primary_key=True)
    QuestTitle = db.Column(db.String(255))
    QuestDescription = db.Column(db.Text)

    missions = db.relationship('Mission', back_populates='quest')


class Student(db.Model):
    __tablename__ = 'student'

    StudentID = db.Column(db.Integer, primary_key=True)
    StudentName = db.Column(db.String(255))
    StudentCohort = db.Column(db.String(100))

    missions = db.relationship('Mission', back_populates='student')


# Creating CRUD functions 
# Create a Quest
@app.route('/quests', methods=['POST'])
def create_quest():
    data = request.get_json()
    quest = Quest(QuestTitle=data['QuestTitle'], QuestDescription=data['QuestDescription'])
    db.session.add(quest)
    db.session.commit()
    return jsonify({'QuestID': quest.QuestID}), 201

# Read a Quest
@app.route('/quests/<int:quest_id>', methods=['GET'])
def get_quest(quest_id):
    quest = Quest.query.get_or_404(quest_id)
    return jsonify({
        'QuestID': quest.QuestID,
        'QuestTitle': quest.QuestTitle,
        'QuestDescription': quest.QuestDescription
    }), 200

# Update a Quest
@app.route('/quests/<int:quest_id>', methods=['PUT'])
def update_quest(quest_id):
    quest = Quest.query.get_or_404(quest_id)
    data = request.get_json()
    quest.QuestTitle = data.get('QuestTitle', quest.QuestTitle)
    quest.QuestDescription = data.get('QuestDescription', quest.QuestDescription)
    db.session.commit()
    return jsonify({'message': 'quest updated'}), 200

# Delete a Quest
@app.route('/quests/<int:quest_id>', methods=['DELETE'])
def delete_quest(quest_id):
    quest = Quest.query.get_or_404(quest_id)
    db.session.delete(quest)
    db.session.commit()
    return jsonify({'message': 'quest deleted'}), 200


# Create a Mission
@app.route('/missions', methods=['POST'])
def create_mission():
    data = request.get_json()
    mission = Mission(
        QuestID=data['QuestID'],
        StudentID=data['StudentID'],
        MissionTitle=data['MissionTitle'],
        MissionDescription=data['MissionDescription'],
        MissionDueDate=datetime.strptime(data['MissionDueDate'], '%Y-%m-%d')
    )
    db.session.add(mission)
    db.session.commit()
    return jsonify({'MissionID': mission.MissionID}), 201

# Read a Mission
@app.route('/missions/<int:mission_id>', methods=['GET'])
def get_mission(mission_id):
    mission = Mission.query.get_or_404(mission_id)
    return jsonify({
        'MissionID': mission.MissionID,
        'QuestID': mission.QuestID,
        'StudentID': mission.StudentID,
        'MissionTitle': mission.MissionTitle,
        'MissionDescription': mission.MissionDescription,
        'MissionDueDate': mission.MissionDueDate.strftime('%Y-%m-%d')
    }), 200

# Update a Mission
@app.route('/missions/<int:mission_id>', methods=['PUT'])
def update_mission(mission_id):
    mission = Mission.query.get_or_404(mission_id)
    data = request.get_json()
    mission.QuestID = data.get('QuestID', mission.QuestID)
    mission.StudentID = data.get('StudentID', mission.StudentID)
    mission.MissionTitle = data.get('MissionTitle', mission.MissionTitle)
    mission.MissionDescription = data.get('MissionDescription', mission.MissionDescription)
    mission.MissionDueDate = datetime.strptime(data['MissionDueDate'], '%Y-%m-%d') if data.get('MissionDueDate') else mission.MissionDueDate
    db.session.commit()
    return jsonify({'message': 'mission updated'}), 200

# Delete a Mission
@app.route('/missions/<int:mission_id>', methods=['DELETE'])
def delete_mission(mission_id):
    mission = Mission.query.get_or_404(mission_id)
    db.session.delete(mission)
    db.session.commit()
    return jsonify({'message': 'mission deleted'}), 200


# Create a Student
@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    student = Student(StudentName=data['StudentName'], StudentCohort=data['StudentCohort'])
    db.session.add(student)
    db.session.commit()
    return jsonify({'StudentID': student.StudentID}), 201

# Read a Student
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = Student.query.get_or_404(student_id)
    return jsonify({
        'StudentID': student.StudentID,
        'StudentName': student.StudentName,
        'StudentCohort': student.StudentCohort
    }), 200

# Update a Student
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    data = request.get_json()
    student.StudentName = data.get('StudentName', student.StudentName)
    student.StudentCohort = data.get('StudentCohort', student.StudentCohort)
    db.session.commit()
    return jsonify({'message': 'student updated'}), 200

# Delete a Student
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'student deleted'}), 200

