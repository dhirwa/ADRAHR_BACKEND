from app import *
from app.model.model import *
from app.model.schema import *
import datetime
from datetime import datetime
import time
from sqlalchemy.exc import IntegrityError
from app.controllers.controller import *
@app.errorhandler(404)
def page_not_found(e):
    return 'Error 404: Page not found, Please check ur route well.'

@app.route('/adra/userss')
def get_users():
    users=User.query.all()
    result=users_schema.dump(users)
    return jsonify({'Users':result.data})


@app.route('/adra/user/<int:uid>')
def user_(uid):
    user = User.query.get(uid)

    if user:
        result = user_schema.dump(user)
        return jsonify({'user':result.data})

    else:
        return jsonify({'message':'0'})


#========================================GET API FOR GETTING ALL EMPLOYEES============================================================
@app.route('/adra/getemployees')
def get_emps():
    emps = Employee.query.all()
    result = emps_schema.dump(emps).data
    return jsonify({'Employees':result})

#====================================== GET API FOR DONORS =========================
@app.route('/adra/getdonors')
def get_donors():
    emps = Donor.query.all()
    result = donors_schema.dump(emps).data
    return jsonify(result)
#====================================GET API TO GET EMPLOYEES AND THEIR PROJECTS AND POSITIONS===========================================================
@app.route('/adra/allemployees')
def get_emS():
    emps= Payroll.query.filter_by(status = 1).all()
    if emps is None:
        return jsonify({'No records!'})
    else:
        json_data = payrolls_schema.dump(emps).data
        result = getallemp(json_data)
        return jsonify(result)

#=============================== GET API TO GET AN EMPLOYEE DETAILS  AND HISTORIC =============================
@app.route('/adra/employee/profile/<int:empid>')
def get_em(empid):
    emps= Payroll.query.filter_by(emp_id = empid).first()
    if emps is None:
        return jsonify({'No records'})
    else:
        json_data = payroll_schema.dump(emps).data
        result = getall(json_data,empid)
        return jsonify(result)

#================================== GET API FOR THE WHOLE PAYROLL LIST====================================
@app.route('/adra/getpayroll')
def get_pays():
    pays = Payroll.query.all()
    result = payrolls_schema.dump(pays).data
    return jsonify({'Payroll':result})

#======================== All payrolls ===================
@app.route('/adra/payrolls')
def get_allpays():
    apy=Payroll.query.all()
    #apy=Payroll.query.filter_by(status=1).all()
    if apy:
        json_data = payrolls_schema.dump(apy).data
        result= getpay(json_data)
        return jsonify(result)
    else:
        return jsonify({'No Payroll'})

#====================== Particular Payroll =====================
@app.route('/adra/payroll/<int:empid>')
def get_payone(empid):
    apy = Payroll.query.filter_by(emp_id=empid).filter_by(status=1).first()
    if apy:
        json_data = payroll_schema.dump(apy).data
        result= getpayo(json_data,empid)
        return jsonify(result)
    else:
        return jsonify({'No Payroll'})


#---------------------- Project Select ----------------------
@app.route('/adra/getprojects')
def get_p():
    emps = Project.query.all()
    result = projs_schema.dump(emps).data
    return jsonify(result)

#=========================List of Fundings======================
@app.route('/adra/fundings')
def get_fun():
    emps = Funding.query.all()
    result = s_schema.dump(emps).data
    return jsonify(result)


#---------------------- List of All Projects ---------------------
@app.route('/adra/projects')
def get_projs():
    projs= Project.query.all()
    if projs is None:
        return jsonify({'No records'})
    else:
        json_data = projs_schema.dump(projs).data
        result = getprojs(json_data)
        return jsonify(result)

#--------------------- LOCATIONS ----------------------------------
@app.route('/adra/projects/location/<int:pid>')
def get_loca(pid):
    emps = Project_loc.query.filter_by(project_id = pid).all()
    result = projlocs_schema.dump(emps).data
    return jsonify(result)

#---------------------- LEAVE PAGES -------------------------------
@app.route('/adra/leaves/<int:empid>')
def get_leav(empid):
    leav = Leave.query.filter_by(emp_id = empid).all()
    if leav is None:
        return jsonify({'No Leaves'})
    else:
        json_data = leaves_schema.dump(leav).data
        result,alld = getLeaves(json_data)
        return jsonify(result)

#--------------------- REMAINING DAYS -----------------------------
@app.route('/adra/leaves/remaining/<int:empid>')
def get_leaves(empid):
    leav = Leave.query.filter_by(emp_id = empid).all()
    if leav is None:
        return jsonify({'No Leaves'})
    else:
        json_data = leaves_schema.dump(leav).data
        result,alld = getLeaves(json_data)
        return jsonify(alld)

#------------------------ SALARY CERTIFICATE -----------------------
@app.route('/adra/employee/salary/<int:empid>')
def get_sal(empid):
    sal = Payroll.query.filter_by(emp_id = empid).filter_by(status = 1).first()
    if sal is None:
        return jsonify({'No records'})
    else:
        json_data = payroll_schema.dump(sal).data
        result = getsala(json_data,empid)
        return jsonify(result)

#------------------------ EMPLOYMENT CERTIFICATE --------------------
@app.route('/adra/employee/employment/<int:empid>')
def get_empl(empid):
    empl = Payroll.query.filter_by(emp_id = empid).filter_by(status = 1).order_by(Payroll.status.desc()).first()
    if empl is None:
        return jsonify({'No records'})
    else:
        json_data = payroll_schema.dump(empl).data
        result = getemployment(json_data,empid)
        return jsonify(result)

#-------------------- LEAVING  CERTIFICATE -------------------------
@app.route('/adra/employee/leaving/<int:empid>')
def get_leaving(empid):
    emps= Payroll.query.filter_by(emp_id = empid).first()
    if emps is None:
        return jsonify({'No records'})
    else:
        json_data = payroll_schema.dump(emps).data
        result = getleaving(json_data,empid)
        return jsonify(result)

#------------------------- FINAL PAY ------------------------------------
@app.route('/adra/employee/finalpay/<int:empid>')
def get_final(empid):
    emps= Payroll.query.filter_by(emp_id = empid).all()
    if emps is None:
        return jsonify({'No records'})
    else:
        json_data = payrolls_schema.dump(emps).data
        result = finalpay(json_data,empid)
        return jsonify(result)

#----------------------- EMPLOYEE EDITING -----------------------
@app.route('/adra/employee/edit/<int:empid>/', methods=['POST'])
def edit(empid):
    first_name=request.get_json()["first_name"]
    last_name=request.get_json()["last_name"]
    education = request.get_json()["education"]
    address = request.get_json()["address"]
    telephone = request.get_json()["telephone"]
    # project_id = request.get_json()["project_id"]
    # position = request.get_json()["position"]
    # salary = request.get_json()["salary"]
    # staff_location = request.get_json()["staff_location"]
    # active_time = request.get_json()["active_time"]
    # inactive_time = request.get_json()["inactive_time"]
    # reason = request.get_json()["reason"]

    emp = Employee.query.filter_by(id=empid).first()
    pay = Payroll.query.filter_by(emp_id = empid).filter_by(status=1).first()
    try:
        emp.first_name=first_name
        emp.last_name = last_name
        emp.education = education
        emp.address = address
        emp.telephone = telephone
        # pay.inactive_time = inactive_time
        # pay.status = 0
        # payroll = Payroll(
        #     emp_id=empid,
        #     project_id=project_id,
        #     position = position,
        #     salary = salary,
        #     staff_location= staff_location,
        #     status = 1,
        #     active_time = active_time,
        #     inactive_time = None,
        #     reason = reason,
        #     regDate = None
        # )

        # db.session.add(payroll)
        db.session.commit()
        return jsonify({'Message':'Edited'})
    except:
        return jsonify({'Message':'0'})

#============================ EDIT DEPENDANTS ======================================
@app.route('/employee/dependant/edit/<int:depid>/', methods=['POST'])
def edit_dep(depid):
    names=request.get_json()["names"]
    relation=request.get_json()["relation"]
    dob = request.get_json()["dob"]

    emp = Emp_dependant.query.filter_by(id=empid).first()

    try:
        names=names
        relation=relation
        dob=dob
        db.session.commit()
        return jsonify({'Message':'Edited'})
    except:
        return jsonify({'Message':'0'})
#============================ EDIT EMERGENCY ======================================
@app.route('/employee/contacts/edit/<int:emid>/', methods=['POST'])
def edit_eme(emid):
    names=request.get_json()["names"]
    relation=request.get_json()["relation"]
    number = request.get_json()["number"]

    emp = Emp_emergency.query.filter_by(id=emid).first()

    try:
        names=names
        relation=relation
        number=number
        db.session.commit()
        return jsonify({'Message':'Edited'})
    except:
        return jsonify({'Message':'0'})
