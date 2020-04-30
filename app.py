from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    author = db.Column(db.String(20), nullable = False, default = 'N/A') 
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.datetime.utcnow())
    

    def __repr__(self):
        return 'Blog post ' + str(self.id)
     

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts', methods=['GET', 'POST'])    
def posts():

     if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPosts(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
     else:
        all_posts = BlogPosts.query.order_by(BlogPosts.date_posted).all()
        return render_template('posts.html', posts=all_posts)

@app.route('/home/users/<string:name>/posts/<int:id>')

def hello(name, id):
    return "Hello, " + name + ",your id is: " + str(id)

@app.route('/onlyget', methods=['GET', 'POST'])
def get_req():
    return "You can only get this webpage."


@app.route('/posts/delete/<int:id>') 
def delete(id):  
    post = BlogPosts.query.get_or_404(id)
    db.session.delete(post) 
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods = ['GET', 'POST'])
def edit(id):
    post = BlogPosts.query.get_or_404(id)

    if request.method == 'POST':
      
      post.title = request.form['title']
      post.author = request.form['author']
      post.content = request.form['content']
      db.session.commit()
      return redirect('/posts')
    else:
      return render_template('edit.html', post=post)  


@app.route('/posts/new', methods=['GET', 'POST']) 
def new_post():
    if request.method == 'POST':
          
      posts.title = request.form['title']
      posts.author = request.form['author']
      posts.content = request.form['content']
      new_post = BlogPosts(title=post.title, content=post.content, author=post.author)
      db.session.add(new_post)
      db.session.commit()
      return redirect('/posts')
    else:
      return render_template('new_post.html')

@app.route('/about')
def about():
    return 'Visit My YOUTUBE !!!!'      

if __name__ == "__main__":
    app.run(debug=True)    
 