from marshmallow import fields,Schema
class EmployeeSchema(Schema):
    id = fields.Integer(dump_only = True)
    first_name = fields.String()
    last_name = fields.String()
    id_type = fields.String()
    id_number = fields.String()
    telephone = fields.String()
    telephone2 = fields.String()
    email = fields.String()
    email2 = fields.String()
    dob = fields.Date()
    gender = fields.String()
    hobby = fields.String()
    education = fields.String()
    address = fields.String()
    status = fields.Integer()
    nationality = fields.String()
    cv_link = fields.String()
    nid_link = fields.String()
    contract = fields.String()
    picture = fields.String()
    regDate = fields.Date()

emp_schema = EmployeeSchema()
emps_schema = EmployeeSchema(many = True)

class Emp_depSchema(Schema):
    id = fields.Integer(dump_only = True)
    emp_id = fields.Integer()
    names = fields.String()
    relation = fields.String()
    dob = fields.Date()
    regDate = fields.Date()

empdep_schema = Emp_depSchema()
empdeps_schema = Emp_depSchema(many = True)

class Emp_emerSchema(Schema):
    id = fields.Integer(dump_only = True)
    emp_id = fields.Integer()
    names = fields.String()
    relation = fields.String()
    number = fields.String()
    regDate = fields.Date()

empemer_schema = Emp_emerSchema()
empemers_schema = Emp_emerSchema(many = True)

class ProjectSchema(Schema):
    id = fields.Integer(dump_only = True)
    name = fields.String()
    donor = fields.String()
    start_date = fields.Date()
    end_date = fields.Date()
    status = fields.Integer()
    regDate = fields.Date()

proj_schema = ProjectSchema()
projs_schema = ProjectSchema(many = True)


class Proj_locSchema(Schema):
    id = fields.Integer(dump_only = True)
    project_id = fields.Integer()
    location = fields.String()
    regDate = fields.Date()

projloc_schema = Proj_locSchema()
projlocs_schema = Proj_locSchema(many = True)

class UserSchema(Schema):
    id = fields.Integer(dump_only = True)
    names = fields.String()
    email = fields.String()
    username = fields.String()
    password = fields.String()
    regDate = fields.Date()

user_schema = UserSchema()
users_schema = UserSchema(many = True)


class PayrollSchema(Schema):
    id = fields.Integer(dump_only = True)
    project_id = fields.Integer()
    emp_id = fields.Integer()
    position = fields.String()
    salary = fields.Integer()
    staff_location = fields.String()
    status = fields.Integer()
    active_time = fields.Date()
    inactive_time = fields.Date()
    regDate = fields.Date()

payroll_schema = PayrollSchema()
payrolls_schema = PayrollSchema(many = True)


class ExpenseSchema(Schema):
    id = fields.Integer(dump_only = True)
    payroll_id = fields.String()
    expense_reason = fields.String()
    amount = fields.Integer()
    regDate = fields.Date()

expense_schema = ExpenseSchema()
expenses_schema = ExpenseSchema(many = True)

class LeaveSchema(Schema):
    id = fields.Integer(dump_only = True)
    emp_id = fields.Integer()
    vacation_id = fields.Integer()
    start_date = fields.Date()
    end_date = fields.Date()
    reason = fields.String()
    address = fields.String()
    status = fields.String()
    regDate = fields.Date()

leave_schema = LeaveSchema()
leaves_schema = LeaveSchema(many = True)

class VacationSchema(Schema):
    id = fields.Integer(dump_only = True)
    vac_type = fields.String()
    duration = fields.Integer()
    regDate = fields.Date()

vac_schema = VacationSchema()
vacs_schema = VacationSchema(many = True)

class TerminatedSchema(Schema):
    id = fields.Integer(dump_only = True)
    emp_id = fields.Integer()
    end_date = fields.Date()
    reason = fields.String()
    comment = fields.String()
    regDate = fields.Date()

term_schema = TerminatedSchema()
terms_schema = TerminatedSchema(many = True)

# class DonorSchema(Schema):
#     id = fields.Integer(dump_only = True)
#     name = fields.String()
#     regDate = fields.String()
#
# donor_schema = DonorSchema()
# donors_schema = DonorSchema(many = True)
#
# class fundingSchema(Schema):
#     id = fields.Integer(dump_only = True)
#     project_id = fields.Integer()
#     donor_id = fields.Integer()
#     regDate = fields.Date()
#
# fund_schema = fundingSchema()
# funds_schema = fundingSchema(many = True)
