from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from datetime import datetime
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/adrahr'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db=SQLAlchemy(app)
migrate= Migrate(app, db)


manager=Manager(app)
manager.add_command('db', MigrateCommand)

#-------------- EMPLOYEE CLASS-----------------
class Employee(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    id_type = db.Column(db.String(100))
    id_number = db.Column(db.String(100))
    telephone = db.Column(db.String(30))
    telephone2 = db.Column(db.String(30))
    email = db.Column(db.String(50))
    email2 = db.Column(db.String(50))
    dob = db.Column(db.DateTime)
    gender = db.Column(db.String(30))
    hobby = db.Column(db.String(30))
    education = db.Column(db.String(100))
    address = db.Column(db.String(100))
    status = db.Column(db.Integer)
    startdate = db.Column(db.DateTime)
    nationality = db.Column(db.String(50))
    cv_link = db.Column(db.String(200))
    nid_link = db.Column(db.String(200))
    contract = db.Column(db.String(200))
    picture = db.Column(db.String(200))
    regDate = db.Column(db.DateTime)
    emp_dependant = db.relationship('Emp_dependant',backref="employee",lazy='dynamic')
    emp_emergency = db.relationship('Emp_emergency',backref="employee",lazy='dynamic')
    payroll = db.relationship('Payroll', backref='employee',lazy='dynamic')
    leave = db.relationship('Leave', backref = 'employee', lazy = 'dynamic')

    def __init__(self, first_name, last_name, id_type, id_number, telephone, telephone2, email, email2,dob, gender, hobby,education, address,  status, startdate,nationality, cv_link, nid_link, contract, picture, regDate= None):

        self.first_name = first_name
        self.last_name = last_name
        self.id_type = id_type
        self.id_number = id_number
        self.telephone = telephone
        self.telephone2 = telephone2
        self.email = email
        self.email2 = email2
        self.dob = dob
        self.gender = gender
        self.hobby = hobby
        self.education = education
        self.address = address
        self.status = status
        self.startdate = startdate
        self.nationality = nationality
        self.cv_link = cv_link
        self.nid_link = nid_link
        self.contract = contract
        self.picture = picture
        if regDate is None:
            regDate = datetime.datetime.utcnow()


#-------------- EMPLOYEE DEPENDANTS CLASS-----------------
class Emp_dependant(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    names = db.Column(db.String(100))
    relation = db.Column(db.String(100))
    dob = db.Column(db.DateTime)
    regDate = db.Column(db.DateTime)

    def __init__(self, emp_id, names, relation, dob, regDate = None):

        self.emp_id = emp_id
        self.names = names
        self.relation = relation
        self.dob = dob
        if regDate is None:
            self.regDate = datetime.datetime.utcnow()


#-------------- EMPLOYEE EMERGENCY CONTACTS CLASS-----------------
class Emp_emergency(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    names = db.Column(db.String(100))
    relation = db.Column(db.String(100))
    number = db.Column(db.String(100))
    regDate = db.Column(db.DateTime)

    def __init__(self, emp_id, names, relation, number, regDate=None):

        self.emp_id = emp_id
        self.names = names
        self.relation = relation
        self.number = number
        if regDate is None:
            self.regDate = datetime.datetime.utcnow()


#-------------- EMP TERMINATED --------------

class Terminated(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    end_date = db.Column(db.DateTime)
    reason = db.Column(db.String(100))
    comment = db.Column(db.String(255))
    regDate = db.Column(db.DateTime)

    def __init__(self, emp_id, end_date, reason, comment, regDate = None):

        self.emp_id = emp_id
        self.end_date = end_date
        self.reason = reason
        self.comment = comment

        if regDate is None:
            regDate = datetime.datetime.utcnow()

#-------------- PROJECT CLASS-----------------
class Project(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200))
    donor = db.Column(db.String(50))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.Integer)
    regDate = db.Column(db.DateTime)
    project_loc = db.relationship('Project_loc',backref="project", lazy='dynamic')
    # funding = db.relationship('Funding',backref='project',lazy='dynamic')
    payroll = db.relationship('Payroll', backref='project',lazy='dynamic')

    def __init__(self, name, donor,start_date, end_date, status, regDate=None):

        self.name = name
        self.donor = donor
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        if regDate is None:
            self.regDate = datetime.datetime.utcnow()


#-------------- PROJECT LOCATIONS CLASS-----------------
class Project_loc(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    location = db.Column(db.String(200))
    regDate = db.Column(db.DateTime)

    def __init__(self, project_id, location, regDate = None):
        self.project_id = project_id
        self.location = location
        if regDate is None:
            self.regDate = datetime.datetime.utcnow()


#-------------- USER CLASS-----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    names = db.Column(db.String(40))
    email = db.Column(db.String(40))
    username = db.Column(db.String(40))
    password = db.Column(db.String(200))
    regDate = db.Column(db.DateTime)
    def __init__(self, names, email, username, password, regDate = None):

        self.names = names
        self.email = email
        self.username = username
        self.password = password
        if regDate is None:
            self.regDate = datetime.datetime.utcnow()

#-------------- PAYROLL CLASS-----------------
class Payroll(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    project_id = db.Column(db.Integer,db.ForeignKey('project.id'))
    position = db.Column(db.String(100))
    salary = db.Column(db.Integer)
    staff_location = db.Column(db.String(100))
    status = db.Column(db.Integer)
    active_time = db.Column(db.DateTime)
    inactive_time = db.Column(db.DateTime)
    regDate = db.Column(db.DateTime)
    expense = db.relationship('Expense', backref='payroll',lazy='dynamic')

    def __init__(self, emp_id,project_id, position, salary, staff_location, status, active_time, inactive_time, reason, regDate= None):

        self.emp_id = emp_id
        self.project_id = project_id
        self.position = position
        self.salary = salary
        self.staff_location = staff_location
        self.status = status
        self.active_time = active_time
        self.inactive_time = inactive_time
        self.reason = reason
        if regDate is None:
            self.regDate = datetime.datetime.utcnow()


#-------------- EXPENSE CLASS-----------------
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    payroll_id = db.Column(db.Integer, db.ForeignKey('payroll.id'))
    expense_reason = db.Column(db.String(100))
    amount = db.Column(db.Integer)
    regDate = db.Column(db.DateTime)

    def __int__(self, payroll_id, expense_reason, amount, regDate=None):

        self.payroll_id = payroll_id
        self.expense_reason = expense_reason
        self.amount = amount
        if regDate is None:
            self.regDate = datetime.utcnonw()


#--------------- VACATION CLASS ------------------
class Vacation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    vac_type = db.Column(db.String(40))
    duration = db.Column(db.Integer)
    regDate = db.Column(db.DateTime)
    leav = db.relationship('Leave', backref='vacation',lazy='dynamic')

    def __init__(self, vac_type, duration, regDate = None):
        self.vac_type = vac_type
        self.duration = duration
        if regDate is None:
            self.regDate = datetime.datetime.utcnow()


#-------------- LEAVE CLASS-----------------
class Leave(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    vacation_id = db.Column(db.Integer, db.ForeignKey('vacation.id'))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    reason = db.Column(db.String(100))
    address = db.Column(db.String(100))
    status = db.Column(db.Integer)
    regDate = db.Column(db.DateTime)

    def __int__(self, emp_id, start_date, end_date, reason, address, status, regDate=None):

        self.emp_id = emp_id
        self.start_date = start_date
        self.end_date = end_date
        self.reason = reason
        self.address = address
        self.status = status
        if regDate is None:
            self.regDate = datetime.datetime.utcnow()


#-------------- DONOR CLASS-----------------
# class Donor(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String(200))
#     regDate = db.Column(db.DateTime)
#     fundings = db.relationship('Funding',backref='donor',lazy='dynamic')
#
#     def __init__(self, name, regDate=None):
#         self.names = names
#         if regDate is None:
#             self.regDate = datetime.utcnow()
#
#
# #-------------- FUNDING CLASS-----------------
# class Funding(db.Model):
#     id = db.Column(db.Integer, primary_key= True)
#     project_id = db.Column(db.Integer,db.ForeignKey('project.id'))
#     donor_id = db.Column(db.Integer, db.ForeignKey('donor.id'))
#     regDate = db.Column(db.DateTime)
#
#     def __init__(self, project_id, donor_id, regDate = None):
#         self.project_id = project_id
#         self.donor_id = donor_id
#         if regDate is None:
#             self.regDate = datetime.utcnow()





if __name__ == '__main__':
    manager.run()
