
    # from flask import Flask, make_response, render_template, request, redirect, url_for, flash ,abort
    # from flask_sqlalchemy import SQLAlchemy 
    # from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user , current_user , login_user  
    # from werkzeug.security import generate_password_hash, check_password_hash
    # import pymysql
    # pymysql.install_as_MySQLdb()




    # app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/db'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.secret_key = 'key'
    # db = SQLAlchemy(app)

    # login_manager = LoginManager()
    # login_manager.init_app(app)
    # login_manager.login_view = 'login'

    # class User(UserMixin, db.Model):
    #     id = db.Column(db.Integer, primary_key=True)
    #     name = db.Column(db.String(200))
    #     email = db.Column(db.String(200), unique=True)
    #     username = db.Column(db.String(200), unique=True)
    #     password = db.Column(db.String(200))
    #     todos = db.relationship('Todo', backref='user', lazy=True)

    # class Todo(db.Model):
    #     id = db.Column(db.Integer, primary_key=True)
    #     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #     title = db.Column(db.String(200), nullable=False)

    # with app.app_context():
    #     db.create_all()

    # @login_manager.user_loader
    # def load_user(user_id):
    #     return User.query.get(int(user_id))

    # @app.route('/login', methods=['GET', 'POST'])
    # def login():
    #     if request.method == 'POST':
    #         user = User.query.filter_by(username=request.form['username']).first()
    #         if user and check_password_hash(user.password, request.form['password']):
    #             login_user(user)
    #             return redirect(url_for('index'))
    #         else:
    #             flash('Invalid username or password')
    #     return render_template('login.html')



    # @app.route('/signup', methods=['GET', 'POST'])
    # def signup():
    #     if request.method == 'POST':
    #         hashed_password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
    #         new_user = User(username=request.form['username'], password=hashed_password)
    #         db.session.add(new_user)
    #         db.session.commit()
    #         return redirect(url_for('login'))
    #     return render_template('signup.html')

    # @app.route('/logout')
    # @login_required
    # def logout():
    #     logout_user()
    #     flash('You have been logged out.')
    #     return redirect(url_for('login'))

    # @app.route('/', methods=['GET', 'POST'])
    # @app.route('/<int:todo_id>', methods=['GET', 'POST'])
    # @login_required
    # def index(todo_id=None):
    #     if request.method == 'POST':
    #         title = request.form.get('title')
    #         if todo_id is None:
    #             todo = Todo(title=title, user_id=current_user.id)
    #             db.session.add(todo)
    #             db.session.commit()
    #             flash('Task added successfully','success')
    #         else:
    #             todo = Todo.query.get(todo_id)
    #             if todo and todo.user_id == current_user.id:
    #                 todo.title = title
    #                 db.session.commit()
    #                 flash('Task updated successfully','success')
    #             else:
    #                 flash('Task not found','danger')
    #     todos = Todo.query.filter_by(user_id=current_user.id).all()
    #     return render_template('index.html', todos=todos)

    #     todo = None
    #     if todo_id is not None:
    #         todo = Todo.query.get(todo_id)
    #     todos= Todo.query.order_by(Todo.id.desc()).all()
        
    #     return render_template('index.html',todos= todos,todo=todo)


    # @app.route('/todo-delete/<int:todo_id>',methods=["POST"])
    # def delete(todo_id):
    #     todo = Todo.query.get(todo_id)
    #     if todo:
    #         db.session.delete(todo)
    #         db.session.commit()
    #         flash('Your task deleted successfully','success')
        
    #     return redirect(url_for('index'))

    # @app.after_request
    # def after_request(response):
    #     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, post-check=0, pre-check=0, max-age=0"
    #     response.headers["Pragma"] = "no-cache"
    #     response.headers["Expires"] = "-1"
    #     return response


    # if __name__ == '__main__':
    #     app.run(debug=True)

from flask import Flask, make_response, render_template, request, redirect, url_for, flash ,abort
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user , current_user , login_user  
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb

app = Flask(__name__)
app.secret_key = 'key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


mysql_host = '127.0.0.1'
mysql_user = 'root'
mysql_password = 'root'
mysql_db = 'sampledb'


def connect_to_database():
    return MySQLdb.connect(host=mysql_host, user=mysql_user, passwd=mysql_password, db=mysql_db)



@login_manager.user_loader
def load_user(user_id):
    conn = connect_to_database()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if user:
        return User(str(user['id']), user['username'], user['password'])
    return None

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @property
    def is_active(self):
        return True
    
    @property
    def is_authenticated(self):
        return self.id is not None and self.username is not None and self.password is not None


@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = connect_to_database()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        cursor.execute("SELECT * FROM user WHERE username = %s", (request.form['username'],))
        user = cursor.fetchone()
        if user and check_password_hash(user['password'], request.form['password']):
            user_object = User(user['id'], user['username'], user['password'])
            login_user(user_object)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    
    cursor.close()
    conn.close()
    return render_template('login.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    conn = connect_to_database()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        hashed_password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        cursor.execute("INSERT INTO user (name, email, username, password) VALUES (%s, %s, %s, %s)", 
                       (request.form['name'], request.form['email'], request.form['username'], hashed_password))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('login'))
    cursor.close()
    conn.close()
    return render_template('signup.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
@app.route('/<int:todo_id>', methods=['GET', 'POST'])
@login_required
def index(todo_id=None):
    conn = connect_to_database()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        title = request.form.get('title')
        if todo_id is None:
            cursor.execute("INSERT INTO todo (title, user_id) VALUES (%s, %s)", (title, current_user.id))
            conn.commit()
            flash('Task added successfully','success')
        else:
            cursor.execute("SELECT * FROM todo WHERE id = %s AND user_id = %s", (todo_id, current_user.id))
            todo = cursor.fetchone()
            if todo:
                cursor.execute("UPDATE todo SET title = %s WHERE id = %s", (title, todo_id))
                conn.commit()
                flash('Task updated successfully','success')
            else:
                flash('Task not found','danger')
    cursor.execute("SELECT * FROM todo WHERE user_id = %s", (current_user.id,))
    todos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', todos=todos)



# @app.route('/edit_todo/<int:todo_id>', methods=['POST'])
# def edit_todo(todo_id):
#     new_title = request.form.get('title')
#     if new_title:
#         conn = connect_to_database()
#         cursor = conn.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute("UPDATE todo SET title = %s WHERE id = %s", (new_title, todo_id))
#         conn.commit()
#         cursor.close()
#         conn.close()
#     return redirect(url_for('index'))
    todo = None
    if todo_id is not None:
        conn = connect_to_database()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM todo WHERE id = %s", (todo_id,))
        todo = cursor.fetchone()
        cursor.close()
        conn.close()
    conn = connect_to_database()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM todo ORDER BY id DESC")
    todos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html',todos= todos,todo=todo)

@app.route('/todo-delete/<int:todo_id>',methods=["POST"])
def delete(todo_id):

    conn = connect_to_database()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM todo WHERE id = %s", (todo_id,))
    todo = cursor.fetchone()
    if todo:
        cursor.execute("DELETE FROM todo WHERE id = %s", (todo_id,))
        conn.commit()
        flash('Your task deleted successfully','success')
    cursor.close()
    conn.close()
    return redirect(url_for('index'))



@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "-1"
    return response

if __name__ == "__main__":
    app.run(debug=True,port=5000,host='0.0.0.0')