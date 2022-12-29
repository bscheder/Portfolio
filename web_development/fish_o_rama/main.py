import datetime
from flask import Flask, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
year = datetime.date.today().year
selected_group = 'All Products'
searched_product  = ''
sort_by = 'Sort by'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    usr_type = db.Column(db.Integer)
    cart = db.relationship('Cart', backref='user')

    def get(user_id):
        return User.query.get(user_id)
    
    def is_active(self):
        return super().is_active

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prod_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    prod_group = db.Column(db.String(50))
    price = db.Column(db.String(10))
    description = db.Column(db.String(500))
    img_url = db.Column(db.String(500))

def get_all_product():
    global selected_group

    for product in db.session.query(Product).all():
        if selected_group == 'All Products' \
           or product.prod_group == selected_group:
            yield product

def get_searched_products():   
    for product in get_all_product():
        if searched_product.lower() in product.title.lower():
            yield product

def get_group_list():
    groups = set()

    for product in db.session.query(Product).all():
        groups.add(product.prod_group)

    for group in sorted(groups):
        yield group

def get_card_content():
    class CartElem:
        def __init__(self,image,price, quantity):
            self.image = image
            self.price = price
            self.quantity = quantity

    cart_dict = {}

    for elem in current_user.cart:
        product = Product.query.filter_by(id=elem.prod_id).first()
        
        if product.title not in cart_dict:
            cart_dict[product.title] = CartElem(product.img_url,product.price,1)
        else:
            cart_dict[product.title].quantity += 1

    for a in cart_dict:
        print(cart_dict[a].image)

    return cart_dict


@app.route('/')
def home():
    return render_template("index.html",groups=get_group_list(),products=get_searched_products(),year=year,selected_group=selected_group,searched=searched_product,sort_by=sort_by)

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        hashed_pwd = generate_password_hash(password=request.form.get('password'),method='pbkdf2:sha256',salt_length=8)  
        new_entry = User(email=request.form.get('email'),password=hashed_pwd,usr_type=0,
                         name=request.form.get('name'))
        db.session.add(new_entry)
        db.session.commit()
        return redirect('/')

    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user is None:
            flash('This email does not exist, please try again.')          
            return redirect('login')

        if check_password_hash(pwhash=user.password, password=password):
            login_user(user)
            return redirect('/')

    return render_template("login.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/<group>/select')
def select_group(group):
    global selected_group
    global searched_product
    global sort_by
    selected_group = group
    searched_product = ''
    sort_by = 'Sort by'

    return redirect('/')

@app.route('/sort', methods=['GET', 'POST'])
def sort():
    global sort_by
    sort_by = request.form.get('product-filter')
    products = []
    
    if sort_by == '↑Price':
        products = sorted(get_searched_products(), key=lambda x: float(x.price), reverse=False)
    elif sort_by == '↓Price':
        products = sorted(get_searched_products(), key=lambda x: float(x.price), reverse=True)
    elif sort_by == '↑Name':
        products = sorted(get_searched_products(), key=lambda x: x.title, reverse=False)
    elif sort_by == '↓Name':
        products = sorted(get_searched_products(), key=lambda x: x.title, reverse=True)
       
    
    return render_template("index.html",groups=get_group_list(),products=products,year=year,selected_group=selected_group,searched=searched_product,sort_by=sort_by)

@app.route('/search', methods=['GET', 'POST'])
def search():
    global searched_product
    global sort_by
    sort_by = 'Sort by'
    searched_product = request.form.get('searched')
    

    return redirect('/')

@app.route('/modal')
def modal():
    return render_template('modal.html',groups=get_group_list(),products=get_searched_products(),year=year,selected_group=selected_group,searched=searched_product,sort_by=sort_by)

@app.route('/cart')
def cart():
    return render_template('cart.html',cart=get_card_content())

@app.route('/<product_id>/add_to_cart')
def add_to_cart(product_id):
    
    if current_user.is_active == False:
        return redirect('/modal')
    
    Cart(prod_id=product_id,user=current_user)
    db.session.commit()
    
    return redirect('/')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    login_manager.init_app(app)
    app.run(debug=True)
