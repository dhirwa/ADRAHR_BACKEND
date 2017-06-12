from app import *
from app.model.model import *
from app.model.schema import *
from flask import jsonify,request
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import datetime
from app.controllers.controller import *
from werkzeug import secure_filename
import string, time, math, random
import os

app.config['UPLOAD_FOLDER'] = '/tmp'
app.config['ALLOWED_EXTENSIONS'] = set(['xlsx','xls','csv','png','pdf','doc','docx'])
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
    username = get_username(data['email'])
    try:
        user = User(
            names=data['names'],
            email=data['email'],
            username=username,
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
#=========================== POST API FOR POSTING EMPLOYEE'S DETAILS,DEPENDANTS,CONTACTS AND PAYROLL,===================
@app.route('/adra/addemployee/', methods=['POST'])
def add_empall():
    json_data = request.get_json()

    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    # data, errors = emp_schema.load(json_data)
    #
    # if errors:
    #     return jsonify(errors), 422
    contacts = filter(None, json_data['contacts'])
    # ======================== SAVE FROM HERE =================
    try:
        employee = Employee(
            first_name=json_data['first_name'],
            last_name=json_data['last_name'],
            id_type = None,
            id_number = json_data['id_number'],
            telephone= json_data['telephone'],
            telephone2= json_data['telephone2'],
            email = json_data['email'],
            email2 = json_data['email2'],
            dob = json_data['dob'],
            gender = json_data['gender'],
            hobby = json_data['hobby'],
            education = json_data['education'],
            address = json_data['address'],
            status = 1,
            startdate = json_data['start'],
            nationality = None,
            cv_link = None,
            nid_link = None,
            contract = None,
            picture = None,
            regDate = None
        )

        db.session.add(employee)
        db.session.commit()
        empid = employee.id

    except IntegrityError:
        db.session().rollback()
        emptel = Employee.query.filter_by(telephone = json_data["telephone"]).first()
        empid = emptel.id

    dnow = datetime.datetime.utcnow()
    try:
        payroll = Payroll(
            emp_id=empid,
            project_id=json_data['project_id'],
            position = json_data['position'],
            salary = json_data['salary'],
            staff_location=json_data['staff_location'],
            status = 1,
            active_time = json_data['start'],
            inactive_time = None,
            reason = None,
            regDate = None
        )

        db.session.add(payroll)
        db.session.commit()

    except IntegrityError:
        db.session().rollback()

    try:
        for item in json_data['dependants']:
            dependant = Emp_dependant(
                emp_id=empid,
                names=item['name'],
                relation=item['relation'],
                dob=item['dob'],
                regDate = None
                )
            db.session.add(dependant)
            db.session.commit()


    except IntegrityError:
        db.session().rollback()

    try:
        for item in contacts:
            emergency = Emp_emergency(
                emp_id=empid,
                names=item['name'],
                relation=item['relation'],
                number=item['phone'],
                regDate = None
                )
            db.session.add(emergency)
            db.session.commit()
        return jsonify(empid)
    except IntegrityError:
        db.session().rollback()
#===============================UPLOADING =====================================
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def uniqid(prefix='c-', more_entropy=False):
    m = time.time()
    uniqid = '%8x%05x' % (math.floor(m), (m - math.floor(m)) * 1000000)
    if more_entropy:
        valid_chars = list(set(string.hexdigits.lower()))
        entropy_string = ''
        for i in range(0, 10, 1):
            entropy_string += random.choice(valid_chars)
        uniqid = uniqid + entropy_string
    uniqid = prefix + uniqid
    return uniqid
@app.route('/api/upload/test_adra/<int:empid>', methods=['POST','GET'])
def upload_adra(empid):
    files = [request.files['file'], request.files['file_1'], request.files['file_2'], request.files['file_3']]
    dest = list()
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            tmp_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(tmp_filename)

            file_name,file_extension = os.path.splitext(tmp_filename)
            re_filename = uniqid()+file_extension
            destination = "/home/dieume/Documents/ADRA/uploads/new/"+re_filename
            #destination = "/home/www/cartix/uploads/user/"+re_filename
            os.rename(tmp_filename, destination)
            dest.append(destination)
    emp = Employee.query.get(empid)
    emp.cv_link = dest[0]
    emp.nid_link=dest[1]
    emp.contract=dest[2]
    emp.picture=dest[3]
    db.session.commit()
    return jsonify(dest)

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
            telephone2= data['telephone2'],
            email = data['email'],
            email2 = data['email2'],
            dob = data['dob'],
            gender = data['gender'],
            hobby = data['hobby'],
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
            donor = data['donor'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            regDate = None
        )
        db.session.add(project)
        db.session.commit()

        proj = proj_schema.dump(Project.query.get(project.id)).data
        return jsonify({'auth':1, 'Project':proj})

    except IntegrityError:
        return jsonify({'auth': 0})

#========================== POST API FOR PROJECT, DONOR AND FUNDING ===========
@app.route('/adra/addproject/', methods=['POST'])
def add_everyproject():
    json_data = request.get_json()

    # if not json_data:
    #     return jsonify({'message': 'No input data provided'}), 400
    #
    #
    try:
        project = Project(
            name=json_data['name'],
            donor=json_data['donor'],
            start_date=json_data['start_date'],
            end_date=json_data['end_date'],
            status = 1,
            regDate = None
        )
        db.session.add(project)
        db.session.commit()
        pid = project.id

    except IntegrityError:
        db.session.rollback()
        proj = Project.query.filter_by(name=json_data['name']).first()
        pid = proj.id

    # try:
    #     fund = Funding(
    #         project_id=pid,
    #         donor_id=json_data['donor_id'],
    #         regDate=None
    #     )
    #     db.session.add(fund)
    #     db.session.commit()
    #
    # except IntegrityError:
    #     db.session.rollback()

    try:
        for item in json_data['locations']:
            projloc = Project_loc(
                project_id=pid,
                location = item['location'],
                regDate = None
                )
            db.session.add(projloc)
            db.session.commit()
        return jsonify({"Message":"Done"})

    except IntegrityError:
        db.session.rollback()
    return json_data


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
            duration = None,
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
        address = data['address'],
        status = 1,
        regDate = None
        )

        db.session.add(leav)
        db.session.commit()

        le = leave_schema.dump(Leave.query.get(leav.id)).data
        return jsonify({'auth':1, 'Leave':le})

    except IntegrityError:
        return jsonify({'auth': 0})


#========================== POST API FOR RECORDING PROJECT EMPLOYEES ==========
# @app.route('/adra/project/donor/', methods=['POST'])
# def add_donor():
#     json_data = request.get_json()
#
#     if not json_data:
#         return jsonify({'message': 'No input data provided'}), 400
#
#     data, errors = donor_schema.load(json_data)
#
#     if errors:
#         return jsonify(errors), 422
#
#     try:
#         donor = Donor(
#             name=data['name'],
#             regDate=None
#         )
#         db.session.add(donor)
#         db.session.commit()
#
#         don = donor_schema.dump(Donor.query.get(donor.id)).data
#         return jsonify({'auth':1, 'Donor':don})
#
#     except IntegrityError:
#         return jsonify({'auth': 0})

#=============================== POST API FOR TERMINATED CONTRACTS ============
# @app.route('/adra/project/funding/', methods=['POST'])
# def add_funding():
#     json_data = request.get_json()
#
#     if not json_data:
#         return jsonify({'message': 'No input data provided'}), 400
#
#     data, errors = fund_schema.load(json_data)
#
#     if errors:
#         return jsonify(errors), 422
#
#     try:
#         fund = Funding(
#             project_id=data['project_id'],
#             donor_id=data['donor_id'],
#             regDate=None
#         )
#         db.session.add(fund)
#         db.session.commit()
#
#         fu = fund_schema.dump(Funding.query.get(fund.id)).data
#         return jsonify({'auth':1, 'Funding':fu})
#
#     except IntegrityError:
#         return jsonify({'auth': 0})

#================================ TERMINATE ==========================
@app.route('/adra/employee/terminate/', methods=['POST'])
def terminate():

    json_data = request.get_json()

    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    data, errors = term_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    try:
        term = Terminated(
        emp_id=data['emp_id'],
        end_date = data['end_date'],
        reason = data['reason'],
        comment = data['comment'],
        regDate = None
        )


        em = Employee.query.get(data['emp_id'])
        em.status = 0
        pay = Payroll.query.filter_by(emp_id = data['emp_id']).filter_by(status=1).first()
        pay.status = 0
        pay.inactive_time = data['end_date']
        db.session.add(term)
        db.session.commit()

        le = term_schema.dump(Terminated.query.get(term.id)).data
        return jsonify({'auth':1, 'Terminated':le})

    except IntegrityError:
        return jsonify({'auth': 0})
