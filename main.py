from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password123@localhost:8889/db_blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    body = db.Column(db.String(1024))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, body, author_id):
        self.title = title
        self.body = body
        self.author_id = author_id

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256))
    password = db.Column(db.String(256))
    blogs = db.relationship('Blogs', backref='user')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route("/")
def index():
    users = Users.query.all()
    return render_template('index.html', title="Ruth's Blogz Home", users=users)

@app.route("/login", methods=['POST', 'GET'])
def login():'
    if request.method == 'GET':
        return render_template('login.html')
    # program log in form
    return render_template('login.html')

@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        user_name = request.form['user']
        password = request.form['pass']
        verify =request.form['secondpass']
        email = request.form['email']
            
        user_error=''
        password_error=''
        verify_error=''
        email_error=''

        #Verify username
        if user_name =='':
            user_error="Please enter a valid username"
        elif len(user_name)<3 or len(user_name)>20:
            user_error="Username must be between 3 and 20 characters long"
            #user_name = ''
        elif ' ' in user_name:
            user_error= "Your username cannot contain any spaces"
            


        #verify first password
        if password =='':
            password_error = "Please enter a valid password"
        elif len(password)<3 or len(password)>20:
            password_error="Password must be between 3 and 20 characters long."
        elif " "in password:
            password_error="Your password cannot contain spaces."



        
        #verify second password
        if verify == '' or verify != password:
            verify_error="Please ensure that passwords match."
            verify = ''

            #verify email
        if email !='':
            if len(email)<3 or len(email)>20:
                email_error="Email must be between 3 and 20 characters"

            elif email.count(".")>1:
                email_error=". or @ should not exceed one."

            elif " " in email:
                email_error="Email should not contain any spaces"
            
        #without errors
        if not user_error and not password_error and not verify_error and not email_error:    
            return render_template('welcome.html',name=user_name)
        else:    
            return render_template('signup.html',name=user_name, user_name_error = user_error,password_error = password_error, verify_error=verify_error, email = email, email_error = email_error)
        return render_template('signup.html',name='', user_name_error = '',password_error = '', verify_error='', email = '', email_error = '')
    
app.run()