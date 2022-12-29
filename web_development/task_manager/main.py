from flask import Flask, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager,current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    selected_table_name =  db.Column(db.String(1000))
    tables = db.relationship('Table', backref='user')

    def get(user_id):
        return User.query.get(user_id)
    
    def is_active(self):
        return super().is_active

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    column_id = db.Column(db.Integer, db.ForeignKey('column.id'))

class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    columns = db.relationship('Column', backref='table')

class Column(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    tasks = db.relationship('Task', backref='column')

@app.route('/')
def index():
  if current_user.is_active == False:
    return render_template('index.html')
  else:
    return redirect('home')  

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_pwd = generate_password_hash(password=request.form.get('password'),method='pbkdf2:sha256',salt_length=8)  
        new_entry = User(email=request.form.get('email'),password=hashed_pwd,
                         name=request.form.get('name'))
        db.session.add(new_entry)
        db.session.commit()
        return redirect('home')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user is None:
            flash('This email does not exist, please try again.')          
            return redirect('login')

        if check_password_hash(pwhash=user.password, password=password):
            login_user(user)
            return redirect('home')

    return render_template('login.html')

@app.route('/home')
def home():
    usr_table = None
    if current_user.is_active == False:
        return render_template('index.html')
        
    for table in get_tables_list():
        if table.title == current_user.selected_table_name and table.user_id == current_user.id:
            usr_table = table

    return render_template('home.html',table=usr_table,columns_list=get_columns_list())

@app.route('/<user>/profile')
def profile(user):
    return render_template('user.html', user=current_user,tables_list=get_tables_list())

@app.route('/<object>/<name>/edit', methods=['GET','POST'])
def edit_form(object,name):
    obj = None
    description = None

    if object == 'task':
        obj = Task.query.filter_by(id=get_task_id(title=name)).first()
        description = obj.description
    elif object == 'table':
        obj = Table.query.filter_by(title=current_user.selected_table_name).first()
    elif object == 'column':
        obj = Column.query.filter_by(id=get_column_id(title=name,table_id=Table.query.filter_by(title=current_user.selected_table_name).first().id)).first()
    
    if request.method == 'POST':
        if object == 'task':
            obj.description = request.form.get('description')
            for column in db.session.query(Column).all():
                if column.title == request.form.get('selected-column') and column.table_id == Table.query.filter_by(title=current_user.selected_table_name).first().id:
                    obj.column_id = column.id
        elif object == 'table':
            current_user.selected_table_name = request.form.get('name')

        obj.title = request.form.get('name')
        db.session.commit()
        return redirect('/home')
    
    return render_template('edit.html',object=object,name=name,description=description,columns_list=get_columns_list())

@app.route('/<object>/<name>/delete', methods=['GET','POST'])
def delete_entry(object,name):
    if object == 'task':
        Task.query.filter_by(id=get_task_id(title=name)).delete()
    elif object == 'table':
        Table.query.filter_by(title=current_user.selected_table_name).delete()
        try:
            table = get_tables_list()
            current_user.selected_table_name = table[0]
        except:
            current_user.selected_table_name = None
    elif object == 'column':
        Column.query.filter_by(id=get_column_id(title=name,table_id=Table.query.filter_by(title=current_user.selected_table_name).first().id)).delete()
    
    db.session.commit()
    
    return redirect('/home')

@app.route('/<user>/edit_user', methods=['GET','POST'])
def edit_user(user):
    user = User.query.filter_by(name=user).first()
    user.name = request.form.get('name')
    user.selected_table_name = request.form.get('selected-table')
    db.session.commit()

    return redirect('/home')

@app.route('/create_table', methods=['GET','POST'])
def create_table():
    table_title = request.form.get('table-title')

    for table in db.session.query(Table).all():
        if table.title == table_title and table.user_id == current_user.id:
            flash('This table name is exist, please try again.')
            return redirect('/home')
    
    current_user.selected_table_name = table_title
    Table(title=table_title,user=current_user)
    db.session.commit()
    
    return redirect('/home')

@app.route('/<table_id>/create_column', methods=['GET','POST'])
def create_column(table_id):
    column_title = request.form.get('column-title')
    table = Table.query.filter_by(id=table_id).first()

    for column in db.session.query(Column).all():
        if column.title == column_title and column.table_id == int(table_id):
            flash('This column name is exist, please try again.')
            return redirect('/home')

    Column(title=column_title,table=table)
    db.session.commit()

    return redirect('/home')

@app.route('/<column_id>/create_task', methods=['GET','POST'])
def create_task(column_id):
    task_title = request.form.get('task-title')
    column = Column.query.filter_by(id=column_id).first()

    for task in db.session.query(Task).all():
        if task.column_id == int(column_id) and task.title == task_title:
            flash('This task name is exist, please try again.')
            return redirect('/home')

    Task(title=task_title,column=column)
    db.session.commit()

    return redirect('/home')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def get_table_id(title):
    for table in db.session.query(Table).all():
        if table.title == title and table.user_id == current_user.id:
            return table.id

def get_column_id(title,table_id):
    for column in db.session.query(Column).all():
        if column.title == title and column.table_id == table_id:
            return column.id

def get_task_id(title):
    column_id_list = []
    for column in get_columns_list():
        column_id_list.append(column['column'].id)
    
    for task in db.session.query(Task).all():
        if task.title == title and task.column_id in column_id_list:
            return task.id

def get_tables_list():
    table_list = []
    for table in db.session.query(Table).all():
        if table.user_id == current_user.id:
            table_list.append(table)
    
    for table in table_list:
        yield table

def get_tasks_list(column_id):  
    tasks = []
    for task in db.session.query(Task).all():
        if task.column_id == column_id:
            tasks.append(task)
    
    return tasks

def get_columns_list():  
    columns = Column.query.filter_by(table_id=get_table_id(current_user.selected_table_name)).all()
    
    for column in columns:
        yield {'column':column,'tasks':get_tasks_list(column.id)}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    login_manager.init_app(app)
    app.run(debug=True)
