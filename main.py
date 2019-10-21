from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:1234@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method=='GET':
        blog_id = request.args.get('id') 
        if blog_id: 
            blog = Blog.query.filter_by(id=blog_id).first() 
            return render_template('homepage.html', blog_id=blog_id, body=blog.body, main_title=blog.title) 
        

        blog = Blog.query.all()
        main_title = "Build a Blog" 
        return render_template('homepage.html', blog=blog, main_title=main_title) 

    error_title = ""
    error_body = ""

    if request.method == 'POST': 
        title = request.form['title'] 
        body = request.form['body'] 

        if body == "": 
            error_body = "Please fill in the body"
        
        if title == "" :
            error_title = "Please fill in the title"

        if error_body != "" or error_title != "" :
            return render_template('/addblogpost.html', error_title=error_title, error_body=error_body)
        else:
            new_post = Blog(title,body)
            db.session.add(new_post) 
            db.session.commit() 
            return redirect("/?id=" + str(new_post.id)) 

@app.route('/addblogpost', methods=['POST', 'GET'])
def addblogpost():

    return render_template('addblogpost.html')

if __name__ == '__main__':
    app.run()