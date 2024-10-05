from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


# In mysql cmd : create database db_name

# 連線至SQL資料庫
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://user_name:password@IP:3306/db_name"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:01220122@localhost:3306/csie_db'

app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)  # 建立物件


# 班級
class Class(db.Model):
    __tablename__ = 'Class'

# 班級編號
    class_id = db.Column(db.Integer, primary_key=True)
# 班導師編號
    teacher_id = db.Column(db.Integer, db.ForeignKey(
        'TeacherList.teacher_id'), nullable=False)
# 人數
    num_of_class = db.Column(db.Integer)

    class_to_student = db.relationship('StudentList', backref='Class')
    class_to_work = db.relationship('ClassWork', backref='Class')


# 教師
class TeacherList(db.Model):
    __tablename__ = 'TeacherList'
# 教師編號
    teacher_id = db.Column(db.Integer, primary_key=True, nullable=False)
# 教師姓名
    t_name = db.Column(db.String(16))
# 電話
    t_tel = db.Column(db.Integer)
# 薪水
    salary = db.Column(db.Integer)

    teacher_to_class = db.relationship(
        'Class', backref='TeacherList', uselist=False)
    teacher_to_course = db.relationship(
        'Course', backref='TeacherList', uselist=False)

# 學生


class StudentList(db.Model):
    __tablename__ = 'StudentList'
# 學號
    student_id = db.Column(db.Integer, primary_key=True)
# 班級編號
    class_id = db.Column(db.Integer, db.ForeignKey("Class.class_id"))
# 學生姓名
    s_name = db.Column(db.String(128))


class ClassWork(db.Model):
    __tablename__ = 'Classwork'
# 課程編號
    course_id = db.Column(db.Integer, primary_key=True)
# 班級編號
    class_id = db.Column(db.Integer, db.ForeignKey('Class.class_id'))
# 上課日期
    date = db.Column(db.Date, primary_key=True)

# 缺席人數
    absent_nr = db.Column(db.Integer)
# 缺席名單
    absent_list = db.Column(db.String(1024), nullable=True)
# 考試範圍
    test = db.Column(db.String(16), nullable=True)
# 備忘錄
    memo = db.Column(db.String(1024), nullable=True)

    work_to_course = db.relationship(
        'Course', backref='Classwork', uselist=False)
    # backref裡面填table名稱


class Course(db.Model):
    # 課程編號
    course_id = db.Column(db.Integer, db.ForeignKey(
        'Classwork.course_id'), primary_key=True)
# 教師編號
    teacher_id = db.Column(db.Integer, db.ForeignKey('TeacherList.teacher_id'))
# 課程名稱
    course_name = db.Column(db.String(32))
# 上課節次 (星期時間)
    course_date = db.Column(db.String(4))
# 上課地點
    place = db.Column(db.String(32))


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/all_class/<int:page>')
def all_class(page=None):
    if page == None:  # 如果沒有Page則顯示第一頁
        page = 1
    page_data = Class.query.order_by('class_id').paginate(
        page=page, per_page=10)

    return render_template('all_class.html', all_info=page_data, page_data=page_data)


@app.route('/all_teacher/<int:page>', methods=['GET'])
def all_teacher(page=None):
    if page == None:  # 如果沒有Page則顯示第一頁
        page = 1
    page_data = TeacherList.query.order_by('teacher_id').paginate(
        page=page, per_page=10)
    print(page_data)
    return render_template('all_teacher.html', all_info=page_data, page_data=page_data)


@app.route('/all_student/<int:page>', methods=['GET'])
def all_student(page=None):
    if page == None:  # 如果沒有Page則顯示第一頁
        page = 1
    page_data = StudentList.query.order_by('student_id').paginate(
        page=page, per_page=10)
    print(page_data)
    return render_template('all_student.html', all_info=page_data, page_data=page_data)


@app.route('/all_course/<int:page>', methods=['GET'])
def all_course(page=None):
    if page == None:  # 如果沒有Page則顯示第一頁
        page = 1
    page_data = Course.query.order_by('course_id').paginate(
        page=page, per_page=10)
    print(page_data)
    return render_template('all_course.html', all_info=page_data, page_data=page_data)


@app.route('/all_classwork/<int:page>', methods=['GET'])
def all_classwork(page=None):
    if page == None:  # 如果沒有Page則顯示第一頁
        page = 1
    page_data = ClassWork.query.order_by('course_id').paginate(
        page=page, per_page=10)
    print(page_data)
    return render_template('all_classwork.html', all_info=page_data, page_data=page_data)

# read


@app.route('/read_student/<int:page>', methods=['GET', 'POST'])
def read_student(page=None):
    if page == None:  # 如果沒有Page則顯示第一頁
        page = 1
    if request.method == 'POST':
        check_data = (not request.form['student_id'])
        if check_data:
            flash('Please enter all the fields correctly', 'error')

            return render_template('read_student.html')

        select_student_info = StudentList.query.filter(StudentList.student_id == request.form['student_id']).order_by('student_id').paginate(
            page=page, per_page=10)
        # page_data = StudentList.query.order_by('student_id').paginate(
        # page=page, per_page=10)
        print(StudentList.query.filter(
            StudentList.student_id == request.form['student_id']) == None)
        return render_template('all_student.html', all_info=select_student_info, page_data=select_student_info)
    return render_template('read_student.html')
    # return render_template('all_student.html', all_info=page_data, page_data=page_data)


@app.route('/read_teacher/<int:page>', methods=['GET', 'POST'])
def read_teacher(page=None):
    if page == None:  # 如果沒有Page則顯示第一頁
        page = 1
    if request.method == 'POST':
        check_data = (not request.form['teacher_id'])
        if check_data:
            flash('Please enter all the fields correctly', 'error')

            return render_template('read_teacher.html')

        select_teacher_info = TeacherList.query.filter(TeacherList.teacher_id == request.form['teacher_id']).order_by('teacher_id').paginate(
            page=page, per_page=10)

        return render_template('all_teacher.html', all_info=select_teacher_info, page_data=select_teacher_info)
    return render_template('read_teacher.html')


@app.route('/update_select_memo/<int:u_id>/<string:s_date>', methods=['GET', 'POST'])
def update_select_memo(u_id, s_date):
    # u_memo = ClassWork.query.filter_by(course_id=u_id).first()
    if request.method == 'GET':
        return render_template('update_memo.html', all_info=ClassWork.query.filter_by(course_id=u_id, date=s_date).all())
    elif request.method == 'POST':
        us_info = db.session.query(ClassWork).filter_by(
            course_id=u_id, date=s_date).first()
        us_info.memo = request.form["update_memo"]

        db.session.commit()

        flash('已成功更新備忘錄內容')
        print(request.form)
        return redirect(url_for('all_classwork', page=1))
        # return redirect(url_for('home'))


@app.route('/read_course/<int:page>', methods=['GET', 'POST'])
def read_course(page=None):
    if page == None:  # 如果沒有Page則顯示第一頁
        page = 1
    if request.method == 'POST':
        check_data = (not request.form['course_id'])
        if check_data:
            flash('Please enter all the fields correctly', 'error')

            return render_template('read_course.html')

        select_course_info = Course.query.filter(Course.course_id == request.form['course_id']).order_by('course_id').paginate(
            page=page, per_page=10)

        return render_template('all_course.html', all_info=select_course_info, page_data=select_course_info)
    return render_template('read_course.html')


@app.route('/read_memo/<int:page>', methods=['GET', 'POST'])
def read_memo(page=None):
    if page == None:  # 如果沒有Page則顯示第一頁
        page = 1
    if request.method == 'POST':
        check_data = (
            not request.form['course_id'] or not request.form['r_s_date'] or not request.form['r_e_date'])
        if check_data:
            flash('Please enter all the fields correctly', 'error')

            return render_template('read_memo.html')

        select_classwork_info = ClassWork.query.filter(
            ClassWork.course_id == request.form['course_id'],
            ClassWork.date >= request.form['r_s_date'],
            ClassWork.date <= request.form['r_e_date'],
        ).order_by('course_id').paginate(
            page=page, per_page=10)

        return render_template('all_classwork.html', all_info=select_classwork_info, page_data=select_classwork_info)
    return render_template('read_memo.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    # app.run()
    app.run(debug=True)
    # app.run('0.0.0.0')
