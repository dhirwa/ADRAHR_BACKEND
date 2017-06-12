from marshmallow import fields,Schema
from app.model.model import *
import datetime
from flask import jsonify
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
    startdate = fields.Date()
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


# class PayrollaSchema(Schema):
#     id = fields.Integer(dump_only = True)
#     project_id = fields.Integer()
#     emp_id = fields.Integer()
#     position = fields.String()
#     salary = fields.Integer()
#     staff_location = fields.String()
#     status = fields.Integer()
#     active_time = fields.Date()
#     inactive_time = fields.Date()
#     regDate = fields.Date()
#     since_months = fields.Method("get_days_since_created")
#     finalpay = fields.Method("get_final_pay")
#     year = fields.Method("get_year")
#
#     def get_days_since_created(self, obj):
#         return abs(((obj.inactive_time - obj.active_time).days)/30)
#
#     def get_final_pay(self, obj):
#         taxable = (3000 * (obj.salary-(50000+1500)))/3409
#         return taxable*abs(((obj.inactive_time - obj.active_time).days)/30)/12
#
#     def get_year(self, obj):
#         taxable = (3000 * (obj.salary-(50000+1500)))/3409
#         d1=obj.active_time
#         d2=obj.inactive_time
#         d3=d2.year-d1.year
#         fp=[]
#         if d3 == 0:
#             d4 = d2.month - d1.month
#             amount= taxable*d4/12
#             fp.append({"amount":amount,"month":d4,"year":d2.year})
#             return fp
#         elif d3 == 1:
#             d5 = 12-d1.month
#             amount1= taxable*d5/12
#             d6 = d2.month
#             amount2= taxable*d6/12
#             fp.append({"amount":amount1,"month":d5,"year":d1.year})
#             fp.append({"amount":amount2,"month":d6,"year":d2.year})
#             return fp
#         else:
#             for i in range(d1.year,d2.year+1):
#                 if i == d1.year:
#                     month=12-d1.month
#                     amount=(taxable*month)/12
#                 elif i == d2.year:
#                     month=d2.month
#                     amount=(taxable*month)/12
#                 else:
#                     month=12
#                     amount=(taxable*month)/12
#                 fp.append({"amount":amount,"month":month,"year":i})
#             return fp
#
# payrolla_schema = PayrollaSchema()
# payrollas_schema = PayrollaSchema(many = True)

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
    year = fields.Method("get_year")
    rowspan = fields.Method("get_span")


    def get_year(self, obj):
        taxable = (3000 * (obj.salary-(50000+1500)))/3409
        d1=obj.active_time
        d2=obj.inactive_time
        d3=d2.year-d1.year
        fp=[]
        if d3 == 0:
            d4 = d2.month - d1.month
            amount= taxable*d4/12
            fp.append({"amount":amount,"month":d4,"year":d2.year,"rowspan":0})
            return fp
        elif d3 == 1:
            d5 = 12-d1.month
            amount1= taxable*d5/12
            d6 = d2.month
            amount2= taxable*d6/12
            fp.append({"amount":amount1,"month":d5,"year":d1.year})
            fp.append({"amount":amount2,"month":d6,"year":d2.year})
            return fp
        else:
            for i in range(d1.year,d2.year+1):
                if i == d1.year:
                    month=12-d1.month
                    amount=(taxable*month)/12
                elif i == d2.year:
                    month=d2.month
                    amount=(taxable*month)/12
                else:
                    month=12
                    amount=(taxable*month)/12
                fp.append({"amount":amount,"month":month,"year":i})
            return fp

    def get_span(self, obj):
        return (obj.inactive_time.year - obj.active_time.year)+1


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
