from flask import render_template, redirect, url_for, request, abort
from flask.helpers import flash
from flask_login import login_user
from flask_login.utils import login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_admin.contrib.sqla import ModelView


from package import app, db, manager, admin
from package.models import Post, User

class Controller(ModelView):
    def is_accessible(self):
        if current_user.is_admin == True:
            return current_user.is_authenticated
        else:
            return abort(404)
    def not_auth(self):
        return "You are not authorized to use the admin dashboard"

admin.add_view(Controller(User, db.session))
admin.add_view(Controller(Post, db.session))


@app.route('/')
def index():
    posts = Post.query.order_by(Post.date.desc()).all()
    return render_template('index.html', posts=posts)


@app.route('/posts/<int:id>')
def post_detail(id):
    post = Post.query.get(id)
    return render_template('post_detail.html', post=post)

@app.route('/posts/<int:id>/delete')
@login_required
def post_delete(id):
    post = Post.query.get_or_404(id)

    try:
        db.session.delete(post)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error'

@app.route('/add_post', methods=['POST', 'GET'])
@login_required
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        intro = text[:75]+'...'
        author = current_user.login
        
        post = Post(title=title, intro=intro, text=text, author=author)
        
        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except:
            return "Error"
    else:   
        return render_template('add_post.html')
    

@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    post = Post.query.get(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.text = request.form['text']
        post.intro = request.form['text'][:75]+'...'
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Error'
    else:
        return render_template('post_update.html', post=post)


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')
    
    
    if login and password:
        user = User.query.filter_by(login=login).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            
            return redirect('/')
        else:
            flash('Невірний логін або пароль!')
    elif login and password and request.method == 'POST':
        flash('Заповніть будь ласка обтдва поля!')
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    print(login, password)
    
    if request.method == 'POST':
        if not(login or password or password2):
            flash('Заповніть будьласка усі поля')
        elif password != password2:
            flash('Паролі не співпадають')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()
            
            return redirect('/login')
        
    return render_template('register.html')



@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/search', methods=['POST', 'GET'])
def search():
    search_posts = []
    search_val = request.form.get('search')
    posts = Post.query.all()
    if request.method == 'POST':
        for post in posts:
            if search_val in post.title or search_val in post.text:
                search_posts.append(post)
        return render_template('index.html', posts=search_posts)
    return redirect('/')