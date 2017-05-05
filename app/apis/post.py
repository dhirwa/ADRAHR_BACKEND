from app import *
from app.model.model import *
from app.model.schema import *
from flask import jsonify,request
from sqlalchemy.exc import IntegrityError
from datetime import datetime

#========================== POST API FOR SIGN UP ======================
@app.route('/adra/signup/', methods=['POST'])
def add_user():
    json_data = request.get_json()

    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    data, errors = user_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    pwd_hash = bcrypt.generate_password_hash(data['password'])

    try:
        user = User(
            names=data['names'],
            email=data['email'],
            username=data['email'],
            password=pwd_hash,
        )
        db.session.add(user)
        db.session.commit()

        last_user = user_schema.dump(User.query.get(user.id)).data
        return jsonify({'auth':1, 'user':last_user})

    except IntegrityError:
        return jsonify({'auth': 0,})


#============================== POST API FOR LOGIN ===========================
@app.route('/adra/login/',methods=['POST'])
def login():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'Message':'No input data provided'}), 400
    data,errors = user_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    username,password = data['username'],data['password']

    user = User.query.filter(User.username==username).first()

    try:
        pw_hash = bcrypt.check_password_hash(user.password, password)
        if pw_hash:
            result = user_schema.dump(User.query.get(user.id))
            return jsonify({'auth': 1, 'user': result.data})
        else:
            return jsonify({'auth': 0})
    except AttributeError:
        return jsonify({'auth':2})

#=========================== POST API FOR RECORDING A NEW EMPLOYEE ============
@app.route('/adra/employee/', methods=['POST'])
def add_emp():
    json_data = request.get_json()

    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    data, errors = emp_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    try:
        employee = Employee(
            first_name=data['first_name'],
            last_name=data['last_name'],
            id_type = data['id_type'],
            id_number = data['id_number'],
            telephone= data['telephone'],
            email = data['email'],
            dob = data['dob'],
            gender = data['gender'],
            education = data['education'],
            address = data['address'],
            status = data['status'],
            nationality = data['nationality'],
            cv_link = None,
            nid_link = None,
            contract = None,
            regDate = None
        )

        db.session.add(employee)
        db.session.commit()

        emp = emp_schema.dump(Employee.query.get(employee.id)).data
        return jsonify({'auth':1, 'Employee':emp})

    except IntegrityError:
        return jsonify({'auth': 0})

#======================== POST API FOR RECORDING EMPLOYEE DEPENDANTS ==========
@app.route('/adra/employee/dependant/', methods=['POST'])
def add_dependant():
    json_data = request.get_json()

    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    data, errors = empdep_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    try:
        dependant = Emp_dependant(
            emp_id=data['emp_id'],
            names=data['names'],
            relation=data['relation'],
            dob=data['dob'],
            regDate = None
        )
        db.session.add(dependant)
        db.session.commit()

        dep = empdep_schema.dump(Emp_dependant.query.get(dependant.id)).data
        return jsonify({'auth':1, 'dependant':dep})

    except IntegrityError:
        return jsonify({'auth': 0})

#========================== POST API FOR RECORDING EMERGENCY CONTACT ==========
@app.route('/adra/employee/emergency/', methods=['POST'])
def add_emergency():
    json_data = request.get_json()

    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    data, errors = empemer_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    try:
        emergency = Emp_emergency(
            emp_id=data['emp_id'],
            names=data['names'],
            relation=data['relation'],
            number=data['number'],
            regDate = None
        )
        db.session.add(emergency)
        db.session.commit()

        emer = empemer_schema.dump(Emp_emergency.query.get(emergency.id)).data
        return jsonify({'auth':1, 'emergency contact':emer})

    except IntegrityError:
        return jsonify({'auth': 0})


#======================= POST API FOR RECORDING A PROJECT ===============
@app.route('/adra/project/', methods=['POST'])
def add_project():
    json_data = request.get_json()

    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    data, errors = proj_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    try:
        project = Project(
            name=data['name'],
            start_date=data['start_date'],
            duration=data['duration'],
            budget = data['budget'],
            regDate = None
        )
        db.session.add(project)
        db.session.commit()

        proj = proj_schema.dump(Project.query.get(project.id)).data
        return jsonify({'auth':1, 'Project':proj})

    except IntegrityError:
        return jsonify({'auth': 0})

#========================== POST API FOR RECORDING PROJECT EMPLOYEES ==========
@app.route('/adra/project/donor/', methods=['POST'])
def add_donor():
    json_data = request.get_json()

    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    data, errors = donor_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    try:
        donor = Donor(
            name=data['name'],
            regDate=None
        )
        db.session.add(donor)
        db.session.commit()

        don = donor_schema.dump(Donor.query.get(donor.id)).data
        return jsonify({'auth':1, 'Donor':don})

    except IntegrityError:
        return jsonify({'auth': 0})

#========================= POST API FOR RECORDING PROJECT LOCATIONS ===========
@app.route('/adra/project/locations/', methods=['POST'])
def add_location():
    json_data = request.get_json()

    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    data, errors = projloc_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    try:
        projloc = Project_loc(
            project_id=data['project_id'],
            location = data['location'],
            regDate = None
        )
        db.session.add(projloc)
        db.session.commit()

        loc = projloc_schema.dump(Project_loc.query.get(projloc.id)).data
        return jsonify({'auth':1, 'Project location':loc})

    except IntegrityError:
        return jsonify({'auth': 0})


#=============================== POST API FOR TERMINATED CONTRACTS ============
@app.route('/adra/project/funding/', methods=['POST'])
def add_funding():
    json_data = request.get_json()

    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    data, errors = fund_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    try:
        fund = Funding(
            project_id=data['project_id'],
            donor_id=data['donor_id'],
            regDate=None
        )
        db.session.add(fund)
        db.session.commit()

        fu = fund_schema.dump(Funding.query.get(fund.id)).data
        return jsonify({'auth':1, 'Funding':fu})

    except IntegrityError:
        return jsonify({'auth': 0})

#=================================== POST API FOR PAYROLL ======================
@app.route('/adra/payroll/', methods=['POST'])
def payroll():
    json_data = request.get_json()

    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    data, errors = payroll_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    try:
        payroll = Payroll(
            emp_id=data['emp_id'],
            project_id=data['project_id'],
            position = data['position'],
            salary = data['salary'],
            staff_location=data['staff_location'],
            status = data['status'],
            active_time = data['active_time'],
            inactive_time = data['inactive_time'],
            reason = None,
            regDate = None
        )

        db.session.add(payroll)
        db.session.commit()

        payr= payroll_schema.dump(Payroll.query.get(payroll.id)).data
        return jsonify({'auth':1, 'Payroll':payr})

    except IntegrityError:
        return jsonify({'auth': 0})


#========================== POST API FOR EXPENSE ===============================
@app.route('/adra/payroll/expense/', methods=['POST'])
def add_expense():
    json_data = request.get_json()

    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    data, errors = expense_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    try:
        expense = Expense(
            payroll_id=data['payroll_id'],
            expense_reason = data['expense_reason'],
            amount = data['amount'],
            regDate = None
        )

        db.session.add(expense)
        db.session.commit()

        exp = expense_schema.dump(Expense.query.get(expense.id)).data
        return jsonify({'auth':1, 'Expense':exp})

    except IntegrityError:
        return jsonify({'auth': 0})

#========================= POST API FOR VACATION ==============================
@app.route('/adra/vacation/', methods=['POST'])
def add_vacation():
    json_data = request.get_json()

    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    data, errors = vac_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    try:
        vaca = Vacation(
            vac_type=data['vac_type'],
            duration = data['duration'],
            regDate = None
        )

        db.session.add(vaca)
        db.session.commit()

        va = vac_schema.dump(Vacation.query.get(vaca.id)).data
        return jsonify({'auth':1, 'Vacation':va})

    except IntegrityError:
        return jsonify({'auth': 0})

#============================ POST API FOR LEAVE ===============================
@app.route('/adra/leave/', methods=['POST'])
def add_leave():
    json_data = request.get_json()

    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    data, errors = leave_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    try:
        leav = Leave(
            emp_id=data['emp_id'],
            vacation_id = data['vacation_id'],
            start_date = data['start_date'],
            end_date = data['end_date'],
            reason = data['reason'],
            regDate = None
        )

        db.session.add(leav)
        db.session.commit()

        le = leave_schema.dump(Leave.query.get(leav.id)).data
        return jsonify({'auth':1, 'Leave':le})

    except IntegrityError:
        return jsonify({'auth': 0})
