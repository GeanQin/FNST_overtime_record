import sqlite3

def get_conn():
    return sqlite3.connect("db/overtime.db")

class Manager(object):
    def __init__(self,work_id,password):
        self.work_id = work_id
        self.password = password

    def save(self):
        sql = "insert into managers VALUES (?,?)"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql,(self.work_id,self.password))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def search(work_id):
        sql = "select * from managers where work_id = ?"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql,(work_id,))
        rows = cursor.fetchall()
        manager = Manager(rows[0][0],rows[0][1])
        conn.commit()
        cursor.close()
        conn.close()
        return manager

    def edit(self):
        sql = "update managers set password = ? where work_id = ?"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql,(self.password,self.work_id))
        conn.commit()
        cursor.close()
        conn.close()

class Project(object):
    def __init__(self,project_id,work_id,project):
        self.project_id = project_id
        self.work_id = work_id
        self.project = project

    def save(self):
        sql = "insert into projects VALUES (?,?,?)"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql,(self.project_id,self.work_id,self.project))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def search(work_id):
        sql = "select * from projects where work_id = ?"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql,(work_id,))
        rows = cursor.fetchall()
        projects = []
        for row in rows:
            project = Project(row[0],row[1],row[2])
            projects.append(project)
        conn.commit()
        cursor.close()
        conn.close()
        return projects

    @staticmethod
    def searchall():
        sql = "select * from projects"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql,)
        rows = cursor.fetchall()
        projects = []
        for row in rows:
            project = Project(row[0],row[1],row[2])
            projects.append(project.project)
        conn.commit()
        cursor.close()
        conn.close()
        return projects

    @staticmethod
    def delete(project_id):
        sql = "delete from projects where project_id = ?"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql,(project_id,))
        conn.commit()
        cursor.close()
        conn.close()

class User(object):
    def __init__(self,user_id,work_id,user_project):
        self.user_id = user_id
        self.work_id = work_id
        self.user_project = user_project

    def save(self):
        sql = "insert into users VALUES (?,?,?)"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql,(self.user_id,self.work_id,self.user_project))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def search(user_id):
        sql = "select * from users where user_id = ?"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql,(user_id,))
        rows = cursor.fetchall()
        user = User(rows[0][0],rows[0][1],rows[0][2])
        conn.commit()
        cursor.close()
        conn.close()
        return user

    def edit(self):
        sql = "update users set user_project = ? where user_id = ?"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql,(self.user_project,self.user_id))
        conn.commit()
        cursor.close()
        conn.close()

class Record(object):
    def __init__(self,record_id,work_id,over_year,over_month,over_day,over_date,over_type,time_start,time_end,time_pay,time_holiday,user_project):
        self.record_id = record_id
        self.work_id = work_id
        self.over_year = over_year
        self.over_month = over_month
        self.over_day = over_day
        self.over_date = str(over_year) + "/" + str(over_month) + "/" + str(over_day)
        self.over_type = over_type
        self.time_start = time_start
        self.time_end = time_end
        self.time_pay = time_pay
        self.time_holiday = time_holiday
        self.user_project = user_project

    def save(self):
        sql = "insert into records VALUES (?,?,?,?,?,?,?,?,?,?,?)"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql,(self.record_id,self.work_id,self.over_year,self.over_month,self.over_day,self.over_type,self.time_start,self.time_end,self.time_pay,self.time_holiday,self.user_project))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def queryByID(work_id):
        sql = "select * from records where work_id = ?"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql,(work_id,))
        rows = cursor.fetchall()
        records = []
        for row in rows:
            record = Record(row[0],row[1],row[2],row[3],row[4],str(row[2]) + "/" + str(row[3]) + "/" + str(row[4]),row[5],row[6],row[7],row[8],row[9],row[10])
            records.append(record)
        conn.commit()
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def queryByYear(user_project,start_year,end_year):
        sql = "select * from records where user_project = ? and over_year > ? and over_year < ?"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql,(user_project,start_year,end_year))
        rows = cursor.fetchall()
        records = []
        for row in rows:
            record = Record(row[0],row[1],row[2],row[3],row[4],str(row[2]) + "/" + str(row[3]) + "/" + str(row[4]),row[5],row[6],row[7],row[8],row[9],row[10])
            records.append(record)
        conn.commit()
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def queryByMonth(user_project,over_year,start_month,end_month):
        sql = "select * from records where user_project = ? and over_year = ? and over_month > ? and over_month < ?"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql,(user_project,over_year,start_month,end_month))
        rows = cursor.fetchall()
        records = []
        for row in rows:
            record = Record(row[0],row[1],row[2],row[3],row[4],str(row[2]) + "/" + str(row[3]) + "/" + str(row[4]),row[5],row[6],row[7],row[8],row[9],row[10])
            records.append(record)
        conn.commit()
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def queryByDay(user_project,over_year,over_month,start_day,end_day):
        sql = "select * from records where user_project = ? and over_year = ? and over_month = ? and over_day >= ? and over_day <= ?"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql,(user_project,over_year,over_month,start_day,end_day))
        rows = cursor.fetchall()
        records = []
        for row in rows:
            record = Record(row[0],row[1],row[2],row[3],row[4],str(row[2]) + "/" + str(row[3]) + "/" + str(row[4]),row[5],row[6],row[7],row[8],row[9],row[10])
            records.append(record)
        conn.commit()
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def delete(record_id):
        sql = "delete from records where record_id = ?"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql,(record_id,))
        conn.commit()
        cursor.close()
        conn.close()
