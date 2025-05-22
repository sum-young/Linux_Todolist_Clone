from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
db = SQLAlchemy(app)

#유저 클래스 (디비랑 연결됨) => 아이디=1, 비번=1이 저장되어있긴함 (다른데에서도 동작하는지는 모름)
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    pw = db.Column(db.String(120), nullable=False)

#투두리스트 클래스 (디비랑 연결됨) => 클래스만 정의하고 아직 아무것도 안함
class listtodo(db.Model):
    __tablename__='todolist'
    category = db.Column(db.String(50), nullable=True)
    todo = db.Column(db.String(300), nullable=False, primary_key=True)
    state = db.Column(db.Boolean)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)

#디비 만드는 코드
with app.app_context():
    db.create_all()


#웹페이지 코드 

#홈화면 (체크박스만 있는 화면)
@app.route('/')
def defaultpage():
    return render_template("default.html")

#로그인 화면
@app.route('/login', methods=["GET", "POST"])
def loginpage():
    if request.method == "POST":
        user_id = request.form.get("id")
        user_pw = request.form.get("pw")

        #이렇게 가져오면 check_user는 객체로 받아오는거라고합니다.
        check_user = User.query.filter_by(id=user_id).first()
        if check_user and check_user.pw == user_pw:
            return render_template("loginsuccess.html")
        else:
            return render_template("loginfail.html")
    return render_template("login.html")

#회원가입 페이지로 이동
@app.route('/join', methods=["GET", "POST"])
def join():
    if request.method == "POST":
        user_id = request.form.get("id")
        user_pw = request.form.get("pw")

        if User.query.filter_by(id=user_id).first():
            return "이미 존재하는 아이디입니다."

        #디비에 회원정보 추가하는 코드
        new_user = User(id=user_id, pw=user_pw)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("loginpage"))
    return render_template("join.html")

#여기가 달력있는 투두리스트 본 페이지
@app.route('/taskmain')
def taskmain():
    return render_template("taskpage.html")

#이 밑으로 투두리스트 추가하는 페이지 추가하고 다른 작업하면 좋을 것 같아요
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5500)

