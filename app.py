from flask import Flask, render_template, request, redirect, abort, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:////todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


app.config['SECRET_KEY'] = 'hggj@#$hkh'

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable= False)
    desc =db.Column(db.String(500), nullable= False)
    date_created = db.Column (db.DateTime, default=datetime.utcnow)

    def __repr__(self) ->str:
        return f"{self.sno} {self.title}"


@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method =="POST":
        title = request.form['title']
        desc = request.form['desc']
        todo= Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo = allTodo )
 
@app.route('/login', methods = ['GET','POST'])
def login():
    email=request.format('email')
    password= request.form.get('password')
    user_data= Todo.query.filter_by(email=email).first()
    if not user_data:
        return {"message": "Account not found, please signup"}
    if not user_data['password'] ==  password:
        return {"message": "passwrd is not correct, please provide valid password!"}
    return render_template(base.html)
    return "The email is {} and the password is {}.format(email,password)"
    


# @app.route('/logout')
# def logout():
#     session.pop('loggedin', None)
#     session.pop('id', None)
#     session.pop('username', None)
#     return redirect(url_for('login'))

# @app.route('/signup', method)
# def Signup():
#     if request.method == 'POST':

#     return render_template('signup.html')

@app.route('/about')
def About():
    return render_template('about.html')

@app.route('/show')
def product():
    
    print(allTodo)
    return 'Hello, this for query'

@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template ('update.html',todo=todo)
@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect ('/')

if __name__=='__main__':
    app.secret_key= os.urandom(12)
    app.run(debug=True) 

