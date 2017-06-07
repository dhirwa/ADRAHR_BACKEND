from app.model.model import *
from app.model.schema import *
from datetime import date
from datetime import datetime
from datetime import timedelta
import datetime
import inflect
import numpy as np
import workdays
import calendar
import math
from sqlalchemy import text

#----------- CONTROLLING EMPLOYEES VIEW ----------------
def getallemp(json_data):
     output = {'Employees':[]}
     for item in json_data:
         res = Employee.query.get(item['emp_id'])
         first = res.first_name
         last = res.last_name
         names = str(first) + ' ' + str(last)
         resu = Project.query.get(item['project_id'])
         projname = resu.name
         if res.status == 0:
             pass
         else:
             output['Employees'].append({'employeeid':item['emp_id'],'names':names,'projectid':item['project_id'],'projectname':projname,'position':item['position']})
     return output

#----------- CONTROLLING TERMINATED VIEW ----------------
def getalltermi(json_data):
     output = {'Employees':[]}
     for item in json_data:
         res = Employee.query.get(item['emp_id'])
         first = res.first_name
         last = res.last_name
         names = str(first) + ' ' + str(last)
         d100=datetime.datetime.strptime(str(item['end_date']), '%Y-%m-%dT%H:%M:%S')
         d110=d100.strftime('%d-%B-%Y')
         output['Employees'].append({'employeeid':item['emp_id'],'names':names,'reason':item['reason'],'end_date':d110})
     return output
#-------------- GET ALL EMPLOYEES DETAILS -------------------
def getall(json_data,empid):
    output = {'Employee':[]}
    ot = []
    at = []
    et = []
    med = 50000
    ar = 1500
    taxable=0
    #for item in json_data:
    res = Employee.query.get(empid)
    first = res.first_name
    last = res.last_name
    names = first+' '+last
    dob = res.dob
    d100=datetime.datetime.strptime(str(dob), '%Y-%m-%d %H:%M:%S')
    d110=d100.strftime('%d-%m-%Y')
    id_type = res.id_type
    id_number = res.id_number
    tel = res.telephone
    tel2 = res.telephone2
    educ = res.education
    addr = res.address
    email = res.email
    email2 = res.email2
    hobby = res.hobby
    cv = res.cv_link
    nid = res.nid_link
    contract = res.contract
    picture = res.picture
    nat = res.nationality
    dep = Emp_dependant.query.filter_by(emp_id = empid).all()
    d = empdeps_schema.dump(dep).data
    for i in d:
        d1=datetime.datetime.strptime(str(i['dob']), '%Y-%m-%dT%H:%M:%S')
        d11=d1.strftime('%d-%m-%Y')
        ot.append({'names':i['names'],'relation':i['relation'],'dob':d11})
    dependants = ot
    emer = Emp_emergency.query.filter_by(emp_id = empid).all()
    e = empemers_schema.dump(emer).data
    for j in e:
        at.append({'names':j['names'],'relation':j['relation'],'number':j['number']})
    emergency = at
    resu = Project.query.get(json_data['project_id'])
    projname = resu.name
    loc = Project_loc.query.filter_by(location=json_data["staff_location"]).first()
    locname = loc.location
    hist = Payroll.query.filter_by(emp_id = empid).all()
    h = payrolls_schema.dump(hist).data
    for k in h:
        pj = Project.query.get(k['project_id'])
        jnam = pj.name
        d0=datetime.datetime.strptime(str(k['active_time']), '%Y-%m-%dT%H:%M:%S')
        if k['inactive_time'] is None:
            pass
        else:
            taxable = (3000 * (k['salary']-(med+ar)))/3409
            taxable2 = format(taxable, ',d')
            d1=datetime.datetime.strptime(str(k['inactive_time']), '%Y-%m-%dT%H:%M:%S')
            d11=d1.strftime('%B, %Y')
            d01=d0.strftime('%B, %Y')
            period = str(d01)+' - '+str(d11)

        if int(k['status'])!=0:
            pass
        else:
            et.append({'Period':period,'Project':jnam,'Position':k['position'],'Salary':taxable2})
    history = et
    output['Employee'].append({'first':first,'last':last,'names':names,'dob':d110,'id_type':id_type,'id_number':id_number,'telephone':tel,'telephone2':tel2,'email':email,'email2':email2,'education':educ,'hobby':hobby,'address':addr,'nationality':nat,'dependants':dependants,'contacts':emergency,'historic': history,'projectid':json_data['project_id'],'projectname':projname,'position':json_data['position'],'salary': json_data['salary'],'location':locname,'cv':cv,'nid':nid,'contract':contract,'picture':picture})
    return output


#---------------------------- PROJECT LISTING ----------------------------
def getprojs(json_data):
    output = {'Projects':[]}
    i = 0
    for item in json_data:
        d1=datetime.datetime.strptime(str(item['start_date']), '%Y-%m-%dT%H:%M:%S')
        d11=d1.strftime('%d-%B-%Y')
        pr = Payroll.query.filter_by(project_id = item['id']).filter_by(status = 1).all()
        e = payrolls_schema.dump(pr).data

        output['Projects'].append({'id':item['id'],'Projectname':item['name'],'start_date':d11,'duration':item['duration'],'staffnumber':5,'salaries':item['budget']})
    return output

#--------------------------- PAYROLL ----------------------------------
def getpay(json_data):
    output = {'Payroll':[]}
    med = 50000
    ar = 1500
    advance = 0
    taxable=0
    net=0
    gp=0
    td=0
    rssb=0
    tpr=0
    emp_rssb=0
    severance=0
    tot_csr=0
    for item in json_data:
        d0=datetime.datetime.strptime(str(item['active_time']), '%Y-%m-%dT%H:%M:%S')
        dnow = datetime.datetime.utcnow()
        d1= datetime.datetime.strptime(str(dnow), '%Y-%m-%d %H:%M:%S.%f')
        c,ddays=calendar.monthrange(d1.year,d1.month)
        num_days=int(ddays)-int(d1.day)
        last_date = d1.replace(day=d1.day + num_days)
        d2= datetime.datetime.strptime(str(last_date), '%Y-%m-%d %H:%M:%S.%f')
        if d0.month == d1.month and d0.year == d1.year:
            dura=workdays.networkdays(d0, d1)
            pretaxable = (3000 * (item['salary']-(med+ar)))/3409
            taxable = (pretaxable * dura)/22
        else:
            taxable = (3000 * (item['salary']-(med+ar)))/3409
        severance = taxable/12
        rssb = round(taxable*0.053)
        emp_rssb = round(taxable*0.033)
        tot_csr = rssb + emp_rssb
        if taxable <=30000:
            tpr = 0
            advance = 0

        elif taxable > 30000 and taxable <=100000:
            tpr = round(taxable * 0.2)
            advance = 5000
        else:
            tpr= round(((taxable-100000)*0.3)+14000)
            advance = 120000
        gp = taxable + rssb
        td = tot_csr + tpr + advance
        net = gp - td
        res = Employee.query.get(item['emp_id'])
        first = res.first_name
        last = res.last_name
        names = first +' '+last
        resu = Project.query.get(item['project_id'])
        projname = resu.name
        output['Payroll'].append({'Payrollid':item['id'],'Names':names,'Project':projname,'position':item['position'],'budgeted_salary':'{0:,}'.format(item['salary']),'taxable':'{0:,}'.format(taxable),'severance':'{0:,}'.format(severance),'employer_rssb':'{0:,}'.format(rssb),'Gross_pay':'{0:,}'.format(gp),'CSR':'{0:,}'.format(tot_csr),'TPR':'{0:,}'.format(tpr),'Advance':'{0:,}'.format(advance),'Total_Deductables':'{0:,}'.format(td),'Net_Salary':'{0:,}'.format(net)})
    return output
#-------------------------- LEAVE ----------------------------------
def getLeaves(json_data,empid):
    output = {'Leaves':[]}
    alld=0
    ot = []
    at = []
    et = []
    med = 50000
    ar = 1500
    taxable=0
    rem = 0
    #for item in json_data:
    res = Employee.query.get(empid)
    first = res.first_name
    last = res.last_name
    names = first+' '+last
    dob = res.dob
    d100=datetime.datetime.strptime(str(dob), '%Y-%m-%d %H:%M:%S')
    d110=d100.strftime('%d-%m-%Y')
    id_type = res.id_type
    id_number = res.id_number
    tel = res.telephone
    tel2 = res.telephone2
    educ = res.education
    hobby = res.hobby
    addr = res.address
    email = res.email
    email2 = res.email2
    picture = res.picture
    nat = res.nationality
    dep = Emp_dependant.query.filter_by(emp_id = empid).all()
    d = empdeps_schema.dump(dep).data
    for i in d:
        d1=datetime.datetime.strptime(str(i['dob']), '%Y-%m-%dT%H:%M:%S')
        d11=d1.strftime('%d-%m-%Y')
        ot.append({'names':i['names'],'relation':i['relation'],'dob':d11})
    dependants = ot
    emer = Emp_emergency.query.filter_by(emp_id = empid).all()
    e = empemers_schema.dump(emer).data
    for j in e:
        at.append({'names':j['names'],'relation':j['relation'],'number':j['number']})
    emergency = at
    resu = Project.query.get(json_data['project_id'])
    projname = resu.name
    leav = Leave.query.filter_by(emp_id = empid).all()
    leavss = leaves_schema.dump(leav).data
    status = ''
    for item in leavss:
        i = int(item['vacation_id'])
        vac = Vacation.query.get(i)
        vac_type = vac.vac_type
        d0=datetime.datetime.strptime(str(item['start_date']), '%Y-%m-%dT%H:%M:%S')
        d1=datetime.datetime.strptime(str(item['end_date']), '%Y-%m-%dT%H:%M:%S')
        d01=d0.strftime('%d-%B-%Y')
        d10=d1.strftime('%d-%B-%Y')
        dura=workdays.networkdays(d0, d1)
        duration = dura
        alld = alld+duration
        rem = 21 - alld
        address = item['address']
        if int(item['status'] == 1):
            status = 'Pending'
        elif int(item['status'] == 2):
            status = 'Approved'
        elif int(item['status'] == 0):
            status = 'Declined'

        et.append({'Emp_id':item['emp_id'],'vac_type':vac_type,'start_date':d01,'end_date':d10,'duration':duration,'reason':item['reason'],'address':address,'status':status})
    output['Leaves'].append({'names':names,'dob':d110,'id_type':id_type,'id_number':id_number,'telephone':tel,'telephone2':tel2,'email':email,'email2':email2,'education':educ,'hobby':hobby,'address':addr,'nationality':nat,'dependants':dependants,'contacts':emergency,'leaves': et,'projectid':json_data['project_id'],'projectname':projname,'position':json_data['position'],'picture':picture})
    return output

#-------------------------- REMAINING DAYS -----------------------------
def getlvs(json_data,items):
    output = {'remain':[]}
    alld = 0
    for item in json_data:
        i = int(item['vacation_id'])
        vac = Vacation.query.get(i)
        vac_type = vac.vac_type
        d0=datetime.datetime.strptime(str(item['start_date']), '%Y-%m-%dT%H:%M:%S')
        d1=datetime.datetime.strptime(str(item['end_date']), '%Y-%m-%dT%H:%M:%S')
        d01=d0.strftime('%d-%B-%Y')
        dura=workdays.networkdays(d0, d1)
        duration = dura
        alld = alld+duration
    rem = 21 - alld
    rema = []
    output['remain'].append({"remaining":rem})
        # if not remain:
        #     rema.append({'remaining':str(0)})
        #     return rema
        # else:
    return output
#-------------------------- SALARY CERTIFICATE ----------------------
def getsala(json_data,empid):
    output={'Salary':[]}
    ot = []
    at = []
    et = []
    med = 50000
    ar = 1500
    advance = 0
    taxable=0
    net=0
    gp=0
    td=0
    rssb=0
    tpr=0
    emp_rssb=0
    severance=0
    tot_csr=0
    taxable = (3000 * (json_data['salary']-(med+ar)))/3409
    severance = taxable/12
    rssb = round(taxable*0.053)
    emp_rssb = round(taxable*0.033)
    tot_csr = rssb + emp_rssb
    if taxable <=30000:
        tpr = 0
        advance = 0

    elif taxable > 30000 and taxable <=100000:
        tpr = round(taxable * 0.2)
        advance = 5000
    else:
        tpr= round(((taxable-100000)*0.3)+14000)
        advance = 80000

    gp = taxable + rssb
    td = tot_csr + tpr + advance
    net = gp - td
    res = Employee.query.get(empid)
    first = res.first_name
    last = res.last_name
    names = str(first) +' '+str(last)
    gender = res.gender
    if str(gender) == 'Male':
        gen = 'He'
        der = 'His'
        ner = 'him'
    else:
        gen ='She'
        der ='Her'
        ner = 'her'
    salary = int(net)
    salar = '{0:,}'.format(salary)
    sal = str(salar)+' frw'
    p = inflect.engine()
    ab = p.number_to_words(salary)
    dnow = datetime.datetime.utcnow()
    d10= datetime.datetime.strptime(str(dnow), '%Y-%m-%d %H:%M:%S.%f')
    d01=d10.strftime('%B %d, %Y')
    d120=datetime.datetime.strptime(str(json_data['active_time']), '%Y-%m-%dT%H:%M:%S')
    d124=d120.strftime('%B,%Y')
    res = Employee.query.get(empid)
    first = res.first_name
    last = res.last_name
    names = first+' '+last
    dob = res.dob
    d100=datetime.datetime.strptime(str(dob), '%Y-%m-%d %H:%M:%S')
    d110=d100.strftime('%d-%m-%Y')
    id_type = res.id_type
    id_number = res.id_number
    tel = res.telephone
    educ = res.education
    addr = res.address
    nat = res.nationality
    email = res.email
    email2 = res.email2
    tel2 = res.telephone2
    hobby = res.hobby
    picture = res.picture
    dep = Emp_dependant.query.filter_by(emp_id = empid).all()
    d = empdeps_schema.dump(dep).data
    for i in d:
        d1=datetime.datetime.strptime(str(i['dob']), '%Y-%m-%dT%H:%M:%S')
        d11=d1.strftime('%d-%m-%Y')
        ot.append({'names':i['names'],'relation':i['relation'],'dob':d11})
    dependants = ot
    emer = Emp_emergency.query.filter_by(emp_id = empid).all()
    e = empemers_schema.dump(emer).data
    for j in e:
        at.append({'names':j['names'],'relation':j['relation'],'number':j['number']})
    emergency = at
    resu = Project.query.get(json_data['project_id'])
    projname = resu.name
    hist = Payroll.query.filter_by(emp_id = empid).all()
    h = payrolls_schema.dump(hist).data
    for k in h:
        pj = Project.query.get(k['project_id'])
        jnam = pj.name
        d0=datetime.datetime.strptime(str(k['active_time']), '%Y-%m-%dT%H:%M:%S')
        if k['inactive_time'] is None:
            pass
        else:
            d1=datetime.datetime.strptime(str(k['inactive_time']), '%Y-%m-%dT%H:%M:%S')
            d11=d1.strftime('%B, %Y')
            d01=d0.strftime('%B, %Y')
            period = str(d01)+' - '+str(d11)
        if int(k['status'])!=0:
            pass
        else:
            et.append({'Period':period,'Project':jnam,'Position':k['position'],'Salary':k['salary']})
    history = et
    output['Salary'].append({'ner':ner,'gen':gen,'der':der,'datenow':d01,'since':d124,'names':names,'position':json_data['position'],'inwords':ab,'innumbers':sal,'names':names,'dob':d110,'id_type':id_type,'id_number':id_number,'telephone':tel,'telephone2':tel2,'email':email,'email2':email2,'education':educ,'hobby':hobby,'address':addr,'nationality':nat,'dependants':dependants,'contacts':emergency,'projectid':json_data['project_id'],'projectname':projname,'picture':picture})
    return output

#--------------------------- EMPLOYMENT CERTIFICATE ------------------------------
def getemployment(json_data,empid):
    output={'Employment':[]}
    ot = []
    at = []
    ps=[]
    dnow = datetime.datetime.utcnow()
    d10= datetime.datetime.strptime(str(dnow), '%Y-%m-%d %H:%M:%S.%f')
    d01=d10.strftime('%B %d, %Y')
    pays = Payroll.query.filter_by(emp_id=empid).filter_by(status = 1).first()
    curr_pos = pays.position
    d120=datetime.datetime.strptime(str(json_data['active_time']), '%Y-%m-%dT%H:%M:%S')
    d124=d120.strftime('%B,%Y')
    res = Employee.query.get(empid)
    first = res.first_name
    last = res.last_name
    names = first+' '+last
    gender = res.gender
    if str(gender) == 'Male':
        gen = 'He'
        der = 'him'
    else:
        gen ='She'
        der ='Her'
    dob = res.dob
    d100=datetime.datetime.strptime(str(dob), '%Y-%m-%d %H:%M:%S')
    d110=d100.strftime('%d-%m-%Y')
    id_type = res.id_type
    id_number = res.id_number
    tel = res.telephone
    educ = res.education
    addr = res.address
    nat = res.nationality
    tel2 = res.telephone2
    email = res.email
    email2 = res.email2
    hobby = res.hobby
    picture = res.picture
    dep = Emp_dependant.query.filter_by(emp_id = empid).all()
    d = empdeps_schema.dump(dep).data
    for i in d:
        d1=datetime.datetime.strptime(str(i['dob']), '%Y-%m-%dT%H:%M:%S')
        d11=d1.strftime('%d-%m-%Y')
        ot.append({'names':i['names'],'relation':i['relation'],'dob':d11})
    dependants = ot
    emer = Emp_emergency.query.filter_by(emp_id = empid).all()
    e = empemers_schema.dump(emer).data
    for j in e:
        at.append({'names':j['names'],'relation':j['relation'],'number':j['number']})
    emergency = at
    resu = Project.query.get(json_data['project_id'])
    projname = resu.name
    hist = Payroll.query.filter_by(emp_id = empid).all()
    output['Employment'].append({'gen':gen,'der':der,'datenow':d01,'names':names,'since':d124,'position':curr_pos,'dob':d110,'id_type':id_type,'id_number':id_number,'telephone':tel,'telephone2':tel2,'email':email,'email2':email2,'hobby':hobby,'education':educ,'address':addr,'nationality':nat,'dependants':dependants,'contacts':emergency,'projectid':json_data['project_id'],'projectname':projname,'picture':picture})
    return output

#---------------------------- LEAVING CERTIFICATE ------------------------------------
def getleaving(json_data,empid):
    output = {'Leaving':[]}
    ot = []
    at = []
    et=[]
    hist = Payroll.query.filter_by(emp_id = empid).all()
    h = payrolls_schema.dump(hist).data
    ii=1
    dnow = datetime.datetime.utcnow()
    d10= datetime.datetime.strptime(str(dnow), '%Y-%m-%d %H:%M:%S.%f')
    d101=d10.strftime('%B %d, %Y')
    for k in h:
        pj = Project.query.get(k['project_id'])
        jnam = pj.name
        d0=datetime.datetime.strptime(str(k['active_time']), '%Y-%m-%dT%H:%M:%S')
        if k['inactive_time'] is None:
            pass
        else:
            d13=datetime.datetime.strptime(str(k['inactive_time']), '%Y-%m-%dT%H:%M:%S')
        d11=d13.strftime('%B, %Y')
        d01=d0.strftime('%B, %Y')
        if int(k['status'])!=0:
            pass
        else:
            iii = str(ii)+'.'
            period = str(d01)+' to '+str(d11)
            worked = str(k['position'])+' in '+str(jnam)+' Project from '+period
            et.append({'no':iii,'Projects':worked})
            ii=ii+1
    history = et
    res = Employee.query.get(empid)
    first = res.first_name
    last = res.last_name
    names = first+' '+last
    gender = res.gender
    if str(gender) == 'Male':
        gen = 'He'
        der = 'His'
    else:
        gen ='She'
        der ='Her'
    dob = res.dob
    d100=datetime.datetime.strptime(str(dob), '%Y-%m-%d %H:%M:%S')
    d110=d100.strftime('%d-%m-%Y')
    id_type = res.id_type
    id_number = res.id_number
    tel = res.telephone
    tel2 = res.telephone2
    email = res.email
    email2 = res.email2
    hobby = res.hobby
    educ = res.education
    addr = res.address
    nat = res.nationality
    picture = res.picture
    dep = Emp_dependant.query.filter_by(emp_id = empid).all()
    d = empdeps_schema.dump(dep).data
    for i in d:
        d12=datetime.datetime.strptime(str(i['dob']), '%Y-%m-%dT%H:%M:%S')
        d11=d12.strftime('%d-%m-%Y')
        ot.append({'names':i['names'],'relation':i['relation'],'dob':d11})
    dependants = ot
    emer = Emp_emergency.query.filter_by(emp_id = empid).all()
    e = empemers_schema.dump(emer).data
    for j in e:
        at.append({'names':j['names'],'relation':j['relation'],'number':j['number']})
    emergency = at
    resu = Project.query.get(json_data['project_id'])
    projname = resu.name
    output['Leaving'].append({'gen':gen,'der':der,'now':d101,'Names':names,'history':history,'dob':d110,'id_type':id_type,'id_number':id_number,'telephone':tel,'telephone2':tel2,'email':email,'email2':email2,'hobby':hobby,'education':educ,'address':addr,'nationality':nat,'dependants':dependants,'contacts':emergency,'projectid':json_data['project_id'],'projectname':projname,'position':json_data['position'],'picture':picture})
    return output

#----------------------------- PARTICULAR PAYROLL ---------------------------------
def getpayo(json_data,empid):

    output = {'Payslip':[]}
    med = 50000
    ar = 1500
    advance = 0
    taxable=0
    net=0
    gp=0
    td=0
    rssb=0
    tpr=0
    emp_rssb=0
    severance=0
    tot_csr=0
    dnow = datetime.datetime.utcnow()
    d1= datetime.datetime.strptime(str(dnow), '%Y-%m-%d %H:%M:%S.%f')
    d01=d1.strftime('%B')
    taxable = (3000 * (json_data['salary']-(med+ar)))/3409
    severance = taxable/12
    rssb = round(taxable*0.053)
    emp_rssb = round(taxable*0.033)
    tot_csr = rssb + emp_rssb
    if taxable <=30000:
        tpr = 0
        advance = 0

    elif taxable > 30000 and taxable <=100000:
        tpr = round(taxable * 0.2)
        advance = 5000
    else:
        tpr= round(((taxable-100000)*0.3)+14000)
        advance = 80000

    gp = taxable + rssb
    td = tot_csr + tpr + advance
    net = gp - td
    salary = int(net)
    nets = str(salary)+' frw'
    ot = []
    at = []
    et = []
    #for item in json_data:
    res = Employee.query.get(empid)
    first = res.first_name
    last = res.last_name
    names = first+' '+last
    gender = res.gender
    if str(gender) == 'Male':
        gen = 'He'
        der = 'His'
    else:
        gen ='She'
        der ='Her'
    dob = res.dob
    d100=datetime.datetime.strptime(str(dob), '%Y-%m-%d %H:%M:%S')
    d110=d100.strftime('%d-%m-%Y')
    id_type = res.id_type
    id_number = res.id_number
    tel = res.telephone
    tel2 = res.telephone2
    email = res.email
    email2 = res.email2
    hobby = res.hobby
    educ = res.education
    addr = res.address
    nat = res.nationality
    picture = res.picture
    dep = Emp_dependant.query.filter_by(emp_id = empid).all()
    d = empdeps_schema.dump(dep).data
    for i in d:
        d1=datetime.datetime.strptime(str(i['dob']), '%Y-%m-%dT%H:%M:%S')
        d11=d1.strftime('%d-%m-%Y')
        ot.append({'names':i['names'],'relation':i['relation'],'dob':d11})
    dependants = ot
    emer = Emp_emergency.query.filter_by(emp_id = empid).all()
    e = empemers_schema.dump(emer).data
    for j in e:
        at.append({'names':j['names'],'relation':j['relation'],'number':j['number']})
    emergency = at
    resu = Project.query.get(json_data['project_id'])
    projname = resu.name
    p = inflect.engine()
    ab = p.number_to_words(salary)
    output['Payslip'].append({'gen':gen,'der':der,'Names':names,'month':d01,'budgeted_salary':json_data['salary'],'Basic_salary':taxable,'severance':severance,'employer_rssb':rssb,'Gross_pay':gp,'csr':tot_csr,'tpr':tpr,'Advance':advance,'Total_Deductables':td,'Net_Salary':nets,'dob':d110,'id_type':id_type,'id_number':id_number,'telephone':tel,'telephone2':tel2,'email':email,'email2':email2,'hobby':hobby,'education':educ,'address':addr,'nationality':nat,'dependants':dependants,'contacts':emergency,'projectid':json_data['project_id'],'projectname':projname,'position':json_data['position'],'picture':picture})
    return output


#================================ FINAL PAY =================================================================================
def finalpay(json_data,empid):

    output = {'FinalPay':[]}
    for item in json_data:
        ot = []
        at = []
        et = []
        res = Employee.query.get(empid)
        first = res.first_name
        last = res.last_name
        names = str(first) + ' ' +str(last)
        gender = res.gender
        if str(gender) == 'Male':
            gen = 'He'
            der = 'His'
        else:
            gen ='She'
            der ='Her'
        dob = res.dob
        d100=datetime.datetime.strptime(str(dob), '%Y-%m-%d %H:%M:%S')
        d110=d100.strftime('%d-%m-%Y')
        id_type = res.id_type
        id_number = res.id_number
        tel = res.telephone
        tel2 = res.telephone2
        email = res.email
        email2 = res.email2
        hobby = res.hobby
        educ = res.education
        addr = res.address
        nat = res.nationality
        picture = res.picture
        dep = Emp_dependant.query.filter_by(emp_id = empid).all()
        d = empdeps_schema.dump(dep).data
        for i in d:
            d1=datetime.datetime.strptime(str(i['dob']), '%Y-%m-%dT%H:%M:%S')
            d11=d1.strftime('%d-%m-%Y')
            ot.append({'names':i['names'],'relation':i['relation'],'dob':d11})
        dependants = ot
        emer = Emp_emergency.query.filter_by(emp_id = empid).all()
        e = empemers_schema.dump(emer).data
        for j in e:
            at.append({'names':j['names'],'relation':j['relation'],'number':j['number']})
        emergency = at
        resu = Project.query.get(item['project_id'])
        projname = resu.name
        start1=datetime.datetime.strptime(str(item['active_time']), '%Y-%m-%dT%H:%M:%S')
        if item['inactive_time'] is None:
            pass
        else:
            end1=datetime.datetime.strptime(str(item['inactive_time']), '%Y-%m-%dT%H:%M:%S')
        if start1.day > 15:
            tm = (end1.year - start1.year) * 12 + (end1.month - start1.month)
        else:
            tm = (end1.year - start1.year) * 12 + (end1.month - start1.month)+1
        #months worked in 1st year
        y=start1.year
        dc = str(y)+'-12-31'
        start2=datetime.datetime.strptime(dc, '%Y-%m-%d')
        if start1.day >15:
            d1=start2.month-start1.month
        else:
            d1=(start2.month-start1.month)+1
        ys = start1.year
        #months worked in last year
        z=end1.year
        dg=str(z)+'-01-01'
        end2=datetime.datetime.strptime(dg, '%Y-%m-%d')
        if end1.day > 15:
            d2=end1.month - end2.month
        else:
            d2=(end1.month -end2.month)-1
        d3= tm-(d1+d2)
        yb= d3/12
        yrs=[]
        yz =range((start1.year)+1, end1.year)
        wxyz = np.asarray(yz)
        xy =range(1,yb)
        med = 50000
        ar = 1500
        taxable = (3000 * (item['salary']-(med+ar)))/3409
        taxable1=(taxable*d1)/12
        if d3 <= 0 :
            taxable2 = 0
        else:
            taxable2=(taxable*yb)
        taxable3=(taxable*d2)/12
        totalt = round(taxable1+taxable2+taxable3)
        if totalt <=30000:
            tpr = 0
            advance = 0

        elif totalt > 30000 and totalt <=100000:
            tpr = totalt * 0.2
            advance = 0
        else:
            tpr= ((totalt-100000)*0.3)+14000
            advance = 0
        gp = totalt
        ded = round(tpr+advance)
        net = round(totalt - ded)
        i=0
        taxab1 = taxable1
        taxab2 = taxable2
        taxab3 = taxable3
        ww=[]

        for i in range(0,yb):
            full = dict()
            full['year']=yz[i]
            full['taxable']=taxab2
            ww.append(full)
            i=i+1

        output['FinalPay'].append({'gen':gen,'der':der,'Names':names,'Start':start1,'End':end1,'Budgeted_Salary':item['salary'],'Taxable':taxable,'Start_Year':y,'End_Year':z,'Taxable_1st_year':taxab1,'Taxable_full_years':ww,'Taxable_last_year':taxab3,'total_taxable':totalt,'tpr':tpr,'advance':advance,'Deductables':ded,'Net':net,'months_in_first':d1,'monthsin_btn':d3,'months_in_last':d2,'years':ww,'dob':d110,'id_type':id_type,'id_number':id_number,'telephone':tel,'telephone2':tel2,'email':email,'email2':email2,'hobby':hobby,'education':educ,'address':addr,'nationality':nat,'dependants':dependants,'contacts':emergency,'projectid':item['project_id'],'projectname':projname,'position':item['position'],'picture':picture})
    return output



#========================= username ==================
def get_username(email):
    username = email.split("@")

    return username[0]

#====================== TERMI PROJECTS =====================
def getalltermiproject(json_data):
    output = {'Projects':[]}
    for item in json_data:
        d1=datetime.datetime.strptime(str(item['start_date']), '%Y-%m-%dT%H:%M:%S')
        d11=d1.strftime('%d-%B-%Y')
        d0=datetime.datetime.strptime(str(item['end_date']), '%Y-%m-%dT%H:%M:%S')
        d10=d0.strftime('%d-%B-%Y')
        pr = Payroll.query.filter_by(project_id = item['id']).filter_by(status = 1).all()
        e = payrolls_schema.dump(pr).data
        output['Projects'].append({'id':item['id'],'Projectname':item['name'],'start_date':d11,'end_date':d10})
    return output
