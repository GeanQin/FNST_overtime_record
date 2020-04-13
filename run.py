from flask import Flask, render_template, request, jsonify, json, send_file, send_from_directory, session
import requests
import sqlite3
from models import User, Record, Manager, Project
import os
import flask_excel as excel

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
excel.init_excel(app)

@app.route('/record',methods=['POST','GET'])
def record():
    if request.method == 'GET':
        return render_template("record.html")
    else:
        work_id = request.form.get('work_id')
        over_year = int(request.form.get('over_year'))
        over_month = int(request.form.get('over_month'))
        over_day = int(request.form.get('over_day'))
        over_date = str(over_year) + "/" + str(over_month) + "/" + str(over_day)
        over_type = request.form.get('over_type')
        time_start = request.form.get('time_start')
        time_end = request.form.get('time_end')
        time_pay = request.form.get('time_pay')
        time_holiday = request.form.get('time_holiday')
        user_project = request.form.get('user_project')
        record = Record(None,work_id,over_year,over_month,over_day,over_date,over_type,time_start,time_end,time_pay,time_holiday,user_project)
        record.save()
        return '1'

@app.route('/list/<work_id>')
def list(work_id):
    records = Record.queryByID(work_id)
    recordlist = []
    recordid = []
    for record in records:
        recordid.append(record.record_id)
    recordlist = splice(records)
    recordid.reverse()
    recordlist.reverse()
    rlist = {}
    rlist['id'] = recordid
    rlist['record'] = recordlist
    return json.dumps(rlist,ensure_ascii=False)

@app.route('/delete/<record_id>')
def delete(record_id):
    Record.delete(record_id)
    return '1'

@app.route('/useradd',methods=['POST','GET'])
def useradd():
    if request.method == 'GET':
        return render_template("useradd.html")
    else:
        user_id = request.form.get('user_id')
        work_id = request.form.get('work_id')
        user_project = request.form.get('user_project')
        user = User(user_id,work_id,user_project)
        user.save()
        return '1'

@app.route('/search/<user_id>')
def search(user_id):
    user = User.search(user_id)
    info = dict()
    info['user_id'] = user.user_id
    info['work_id'] = user.work_id
    info['user_project'] = user.user_project
    return jsonify(info)

@app.route('/useredit',methods=['POST','GET'])
def useredit():
    if request.method == 'GET':
        return render_template("useredit.html")
    else:
        user_id = request.form.get('user_id')
        user_project = request.form.get('user_project')
        user = User(user_id,None,user_project)
        user.edit()
        info = dict()
        info['user_id'] = user_id
        info['user_project'] = user_project
        return jsonify(info)

@app.route('/manager',methods=['POST','GET'])
def manager():
    work_id = session.get('manager')
    projects = getpro(work_id)
    if request.method == 'GET':
        return render_template("manager.html", allrec = '', work_id = work_id, projects = projects)
    else:
        user_project = request.form.get('user_project')
        start_year = int(request.form.get('start_year'))
        start_month = int(request.form.get('start_month'))
        start_day = int(request.form.get('start_day'))
        end_year = int(request.form.get('end_year'))
        end_month = int(request.form.get('end_month'))
        end_day = int(request.form.get('end_day'))
        session['user_project'] = user_project
        session['start_year'] = start_year
        session['start_month'] = start_month
        session['start_day'] = start_day
        session['end_year'] = end_year
        session['end_month'] = end_month
        session['end_day'] = end_day
        records = getrec(user_project, start_year, start_month, start_day, end_year, end_month, end_day)
        allrec = splice(records)
        allrec.sort()
        return render_template("manager.html", allrec = allrec, work_id = work_id, projects = projects)

@app.route('/download')
def download():
    user_project = session.get('user_project')
    start_year = int(session.get('start_year'))
    start_month = int(session.get('start_month'))
    start_day = int(session.get('start_day'))
    end_year = int(session.get('end_year'))
    end_month = int(session.get('end_month'))
    end_day = int(session.get('end_day'))
    records = getrec(user_project, start_year, start_month, start_day, end_year, end_month, end_day)
    records = sorted(records, key=lambda record: record.over_date)
    return excel.make_response_from_query_sets(
        records,
        column_names=[
            'over_date',
            'over_type',
            'time_start',
            'time_end',
            'time_pay',
            'time_holiday',
            'work_id'
        ],
        file_type = 'xlsx',
        file_name = 'list.xlsx'
    )

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        work_id = request.form.get('work_id')
        password = request.form.get('password')
        manager = Manager(work_id,password)
        manager.save()
        return render_template("login.html")

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        work_id = request.form.get('work_id')
        password = request.form.get('password')
        try:
            manager = Manager.search(work_id)
            if manager.password == password:
                session['manager'] = work_id
                projects = getpro(work_id)
                return render_template("manager.html", allrec = "", work_id = work_id, projects = projects)
            else:
                return render_template("login.html")
        except:
            return render_template("login.html")

@app.route('/addpro',methods=['POST','GET'])
def addpro():
    if request.method == 'GET':
        return render_template("addpro.html")
    else:
        work_id = session.get('manager')
        allpro = Project.searchall()
        project = request.form.get('project')
        for pro in allpro:
            if pro == project:
                return "project already exists..."
        pro = Project(None,work_id,project)
        pro.save()
        projects = getpro(work_id)
        return render_template("manager.html", allrec = "", work_id = work_id, projects = projects)

@app.route('/delpro',methods=['POST','GET'])
def delpro():
    work_id = session.get('manager')
    if request.method == 'GET':
        projects = getpro(work_id)
        return render_template("delpro.html", projects = projects)
    else:
        project = request.form.get('project')
        projects = Project.search(work_id)
        proid = 0
        for pro in projects:
            if pro.project == project:
                proid = pro.project_id
                pro.delete(proid)
        projects = getpro(work_id)
        return render_template("manager.html", allrec = "", work_id = work_id, projects = projects)

@app.route('/listpro')
def listpro():
    allpro = Project.searchall()
    rlist = {}
    rlist['projects'] = allpro
    return json.dumps(rlist,ensure_ascii=False)

def getpro(work_id):
    projects = Project.search(work_id)
    pronames=[]
    for project in projects:
        pronames.append(project.project)
    return pronames

@app.route('/api/<code>')
def api(code):
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid=wx2db0458b3cd21cc4&secret=bcbd51dc8361fec7ccf83eb262d7a13e&grant_type=authorization_code&js_code=' + code
        r = requests.get(url)
        return r.text

def getrec(user_project, start_year, start_month, start_day, end_year, end_month, end_day):
    allrec = []
    if start_year == end_year and start_month == end_month:
        records = Record.queryByDay(user_project,start_year,start_month,start_day,end_day)
        allrec.extend(records)
    elif start_year == end_year and start_month != end_month:
        records = Record.queryByMonth(user_project,start_year,start_month,end_month)
        allrec.extend(records)
        records = Record.queryByDay(user_project,start_year,start_month,start_day,32)
        allrec.extend(records)
        records = Record.queryByDay(user_project,start_year,end_month,0,end_day)
        allrec.extend(records)
    else:
        records = Record.queryByYear(user_project,start_year,end_year)
        allrec.extend(records)
        records = Record.queryByMonth(user_project,start_year,start_month,13)
        allrec.extend(records)
        records = Record.queryByMonth(user_project,end_year,0,end_month)
        allrec.extend(records)
        records = Record.queryByDay(user_project,start_year,start_month,start_day,32)
        allrec.extend(records)
        records = Record.queryByDay(user_project,end_year,end_month,0,end_day)
        allrec.extend(records)
    return allrec

def splice(records):
    allrec = []
    for record in records:
        month = ""
        day = ""
        if record.over_month < 10:
            month = "0" + str(record.over_month)
        else:
            month = str(record.over_month)
        if record.over_day < 10:
            day = "0" + str(record.over_day)
        else:
            day = str(record.over_day)
        allrec.append(record.work_id + "," + str(record.over_year) + "/" + month + "/" + day + "," + record.over_type + "," + record.time_start + "," + record.time_end + "," + record.time_pay + "," + record.time_holiday)
    return allrec

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
