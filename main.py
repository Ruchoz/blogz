from flask import Flask, request, render_template,session,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password123@localhost:8889/db_blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key='vickie'

db = SQLAlchemy(app)

class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    body = db.Column(db.String(1024))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, body,author):
        self.title = title
        self.body = body
        self.author = author

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(256))
    blogs = db.relationship('Blogs', backref='author')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route("/")
def index():
    users = Users.query.all()
    return render_template('index.html', title="Ruth's Blogz Home", users=users)

@app.before_request
def require_login():
    allowed_routes=['login','sign_up', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')   

@app.route('/login', methods=['POST','GET'])
def login():
    username=''
    username_error=''
    password_error=''
    
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']

        user = Users.query.filter_by(username=username).first()
        #validate password and user
        if not user or username=='':
            username_error='Please enter a valid username'
        
        if password=='':
            password_error='Please enter a valid password'
        if user and password != password:
            password_error='Invalid password'

    if request.method=='POST'and user and user.password == password and not username_error and not password_error:
            session['username']=username
            
            return redirect('/newpost')
    

    else:
        return render_template ('login.html', username_error=username_error, password_error=password_error)
       # validate password and username)


@app.route('/blog')
def main_page():
    userid=request.args.get('user')
    blogid=request.args.get('id')

    if userid:
        blogs=Blogs.query.filter_by(author_id=userid).all()
        return render_template('main_page.html', bloglist = blogs)
    if blogid:
        blog=Blogs.query.filter_by(id=blogid).first()
        return render_template('blog.html', blog = blog)
    blogs = Blogs.query.all()
    return render_template('main_page.html', bloglist = blogs)


@app.route('/newpost', methods=['POST','GET'])
def new_post():

    title_error=''
    body_error=''
    title = ''
    body = ''


    if request.method == 'POST':
        title = request.form['blog_title']
        body = request.form['blog_body'] 

        #validate 
        if title=='':
            title_error="Please fill in the title"
        if body=='':
            body_error="Please fill in the body"

    if request.method=='POST' and not title_error and not body_error:
        
        username=session['username']
        this_user = Users.query.filter_by(username=username).first()
        new_blog=Blogs(title, body,this_user)
        db.session.add(new_blog)
        db.session.commit()
        if new_blog.id:
            blog=Blogs.query.filter_by(id=new_blog.id).first()
            return render_template('blog.html', blog=blog)
        
        # blogs = Blog.query.all()
        # return render_template('main-blog.html', bloglist = blogs)
    else:
        return render_template('newpost.html', title_error=title_error, body_error=body_error,blog_title=title, blog_body=body)





@app.route('/sign_up', methods= ['POST', 'GET'])
def sign_up():
    username=''
    user_name_error=''
    password=''
    password_error=''
    verify_error=''
    email_error=''
    existing_user=''
    existing_user_error=''

    
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['pass']
        verify =request.form['secondpass']
        email = request.form['email']
        

        #Verify username
        if username =='':
            user_name_error="Please enter a valid username"
        elif len(username)<3 or len(username)>20:
            user_name_error="Username must be between 3 and 20 characters long"
            #user_name = ''
        elif ' ' in username:
            user_name_error= "Your username cannot contain any spaces"
            


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

            #existing user error
            existing_user = Users.query.filter_by(username=username).first()
            if existing_user:
                existing_user_error="Duplicate username"
            
        #without errors
    if request.method=='POST' and not user_name_error and not password_error and not verify_error and not email_error and not existing_user_error:    
            
        if not existing_user:
            new_user = Users(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username']=new_user.username

        return render_template('login.html')
        
    else:    
        return render_template('signup.html', name=username, user_name_error=user_name_error, password_error=password_error,verify_error=verify_error, email_error=email_error, existing_user_error=existing_user_error)


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')


if __name__ == '__main__':
    app.run()