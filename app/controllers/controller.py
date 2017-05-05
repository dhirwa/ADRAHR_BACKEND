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
         output['Employees'].append({'employeeid':item['emp_id'],'names':names,'projectid':item['project_id'],'projectname':projname,'position':item['position']})
     return output

#-------------- GET ALL EMPLOYEES DETAILS -------------------
def getall(json_data,empid):
    output = {'Employee':[]}
    ot = []
    at = []
    et = []
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
    educ = res.education
    addr = res.address
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
    output['Employee'].append({'names':names,'dob':d110,'id_type':id_type,'id_number':id_number,'telephone':tel,'education':educ,'address':addr,'nationality':nat,'dependants':dependants,'contacts':emergency,'historic': history,'projectid':json_data['project_id'],'projectname':projname,'position':json_data['position']})
    return output


#---------------------------- PROJECT LISTING ----------------------------
def getprojs(json_data):
    output = {'Projects':[]}
    i = 0
    for item in json_data:
        pr = Payroll.query.filter_by(project_id = item['id']).all()
        e = payrolls_schema.dump(pr).data
        d1=datetime.datetime.strptime(str(item['start_date']), '%Y-%m-%dT%H:%M:%S')
        d11=d1.strftime('%d-%B-%Y')
        for j in e:
            i=i+1
        output['Projects'].append({'Project_id':item['id'],'Projectname':item['name'],'start_date':d11,'duration':item['duration'],'staffnumber':i,'salaries':item['budget']})
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
            tpr= round(((taxable-100)*0.3)+14000)
            advance = 120000
        gp = taxable + rssb
        td = round(tot_csr + tpr + advance)
        net = gp - td
        res = Employee.query.get(item['emp_id'])
        first = res.first_name
        last = res.last_name
        names = first +' '+last
        resu = Project.query.get(item['project_id'])
        projname = resu.name
        output['Payroll'].append({'Payrollid':item['id'],'Names':names,'Project':projname,'position':item['position'],'budgeted_salary':item['salary'],'taxable':taxable,'severance':severance,'employer_rssb':rssb,'Gross_pay':gp,'CSR':tot_csr,'TPR':tpr,'Advance':advance,'Total_Deductables':td,'Net_Salary':net})
    return output
#-------------------------- LEAVE ----------------------------------
def getLeaves(json_data):
    output = {'Leaves':[]}
    alld=0
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
        output['Leaves'].append({'Emp_id':item['emp_id'],'vac_type':vac_type,'start_date':d01,'end_date':item['end_date'],'duration':duration,'reason':item['reason']})
    rem = 21 - alld
    remains = {'remain':[]}
    remains['remain'].append({"remaining":rem})
    return output,remains

#-------------------------- REMAINING DAYS -----------------------------


#-------------------------- SALARY CERTIFICATE ----------------------
def getsala(json_data,empid):
    output={'Salary':[]}
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
    if str(gender) == 'M':
        gen = 'He'
        der = 'His'
    else:
        gen ='She'
        der ='Her'
    salary = int(net)
    sal = str(salary)+' frw'
    p = inflect.engine()
    ab = p.number_to_words(salary)
    dnow = datetime.datetime.utcnow()
    d10= datetime.datetime.strptime(str(dnow), '%Y-%m-%d %H:%M:%S.%f')
    d01=d10.strftime('%B %d, %Y')
    d1=datetime.datetime.strptime(str(json_data['active_time']), '%Y-%m-%dT%H:%M:%S')
    d11=d1.strftime('%B,%Y')
    output['Salary'].append({'gen':gen,'der':der,'datenow':d01,'since':d11,'names':names,'position':json_data['position'],'inwords':ab,'innumbers':sal})
    return output

#--------------------------- EMPLOYMENT CERTIFICATE ------------------------------
def getemployment(json_data,empid):
    output={'Employment':[]}
    ps=[]
    res = Employee.query.get(empid)
    first = res.first_name
    last = res.last_name
    dnow = datetime.datetime.utcnow()
    d10= datetime.datetime.strptime(str(dnow), '%Y-%m-%d %H:%M:%S.%f')
    d01=d10.strftime('%B %d, %Y')
    names = str(first)+' '+str(last)
    pays = Payroll.query.filter_by(emp_id=empid).filter_by(status = 1).first()
    curr_pos = pays.position
    d1=datetime.datetime.strptime(str(json_data['active_time']), '%Y-%m-%dT%H:%M:%S')
    d11=d1.strftime('%B,%Y')
    output['Employment'].append({'datenow':d01,'names':names,'since':d11,'position':curr_pos})
    return output

#---------------------------- LEAVING CERTIFICATE ------------------------------------
def getleaving(json_data,empid):
    output = {'Leaving':[]}
    et=[]
    res = Employee.query.get(empid)
    first = res.first_name
    last = res.last_name
    names = str(first)+' '+str(last)
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
            d1=datetime.datetime.strptime(str(k['inactive_time']), '%Y-%m-%dT%H:%M:%S')
        d11=d1.strftime('%B, %Y')
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
    output['Leaving'].append({'now':d101,'Names':names,'history':history})
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
    res = Employee.query.get(empid)
    first = res.first_name
    last = res.last_name
    names = str(first) +' '+str(last)
    salary = int(net)
    nets = str(salary)+' frw'
    pj = Project.query.get(json_data['project_id'])
    jnam = pj.name
    p = inflect.engine()
    ab = p.number_to_words(salary)
    output['Payslip'].append({'Names':names,'month':d01,'Project':jnam,'position':json_data['position'],'budgeted_salary':json_data['salary'],'Basic_salary':taxable,'severance':severance,'employer_rssb':rssb,'Gross_pay':gp,'csr':tot_csr,'tpr':tpr,'Advance':advance,'Total_Deductables':td,'Net_Salary':nets})
    return output


#================================ FINAL PAY =================================================================================
def finalpay(json_data,empid):

    output = {'FinalPay':[]}
    for item in json_data:
        res = Employee.query.get(empid)
        first = res.first_name
        last = res.last_name
        names = str(first) + ' ' +str(last)
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
        taxable2=(taxable*yb)
        taxable3=(taxable*d2)/12
        totalt = round(taxable1+taxable2+taxable3)
        if totalt <=30000:
            tpr = 0
            advance = 0

        elif totalt > 30000 and taxable <=100000:
            tpr = totalt * 0.2
            advance = 5000
        else:
            tpr= ((totalt-100000)*0.3)+14000
            advance = 80000
        gp = totalt
        ded = round(tpr+advance)
        net = round(totalt - ded)
        i=0
        ww=[]

        for i in range(0,yb):
            full = dict()
            full['year']=yz[i]
            full['taxable']=taxable
            ww.append(full)
            i=i+1
        output['FinalPay'].append({'Names':names,'Start':start1,'End':end1,'Budgeted_Salary':item['salary'],'Taxable':taxable,'Start_Year':y,'End_Year':z,'Taxable_1st_year':taxable1,'Taxable_full_years':taxable2,'Taxable_last_year':taxable3,'total_taxable':totalt,'tpr':tpr,'advance':advance,'Deductables':ded,'Net':net,'months_in_first':d1,'monthsin_btn':d3,'months_in_last':d2,'years':ww})
    return output
