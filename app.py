from flask import Flask , render_template , request , redirect , url_for , flash , abort
from werkzeug.utils import secure_filename
from extensions.extensions import db  # ایمپورت صحیح db
from validators.Auth import Login , Reqister , EditProfile , ChangePassword
from flask_login import LoginManager , login_user , current_user , logout_user , login_required
import os
from models import Users, Breed, Cart, Order
from controller import home , user , auth , admin, cart

app = Flask(__name__)

app.secret_key = 'e033dd67b1b6314a8fa42806e268382f'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'static', 'uploads')

from extensions.utility import allow_extension

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_DIR'] = UPLOAD_DIR

# مقداردهی اولیه SQLAlchemy
db.init_app(app)

login = LoginManager()
login.login_view = 'SignIn'
login.login_message_category = 'info'
login.init_app(app)

homeController = home.Home()
userController = user.Account()
authController = auth.Authentication()
adminController = admin.Admin()
cartController = cart.CartController()

@login.user_loader
def userLoader(user_id):
    return Users.query.get(user_id)

# تعریف مسیرها (Routes)
app.add_url_rule('/' , 'main' , homeController.main)
app.add_url_rule('/account' , 'account' , userController.account)
app.add_url_rule('/account/info' , 'account_info' , userController.account_info)
app.add_url_rule('/account/chengepassword' , 'account_password' , userController.account_password , methods = ['GET' , 'POST'])
app.add_url_rule('/account/avatar' , 'account_avatar' , userController.account_avatar , methods = ['GET' , 'POST'])
app.add_url_rule('/account/edit' , 'account_edit' , userController.account_edit , methods = ['GET' , 'POST'])

app.add_url_rule('/signout' , 'SignOut' , authController.SignOut , methods = ['GET' , 'POST'])
app.add_url_rule('/signup' , 'SignUp' , authController.SignUp , methods = ['GET' , 'POST'])
app.add_url_rule('/signin' , 'SignIn' , authController.SignIn , methods = ['GET' , 'POST'])

app.add_url_rule('/admin' , 'index' , adminController.index )
app.add_url_rule('/admin/user' , 'get_all_users' , adminController.get_all_users )
app.add_url_rule('/admin/user/create' , 'create_user' , adminController.create_user , methods=('GET' , 'POST') )
app.add_url_rule('/admin/user/edit' , 'edit_user' , adminController.edit_user , methods=('GET' , 'POST') )
app.add_url_rule('/admin/info' , 'admin_account_info' , adminController.admin_account_info )
app.add_url_rule('/admin/edit' , 'admin_account_edit' , adminController.admin_account_edit , methods = ['GET' , 'POST'])
app.add_url_rule('/admin/changepassword' , 'admin_account_password' , adminController.admin_account_password , methods = ['GET' , 'POST'] )
app.add_url_rule('/admin/avatar' , 'admin_account_avatar' , adminController.admin_account_avatar , methods=('GET' , 'POST') )

app.add_url_rule('/cart', 'view_cart', cartController.view_cart)
app.add_url_rule('/cart/add/<string:breed_id>', 'add_to_cart', cartController.add_to_cart, methods=['POST'])
app.add_url_rule('/cart/remove/<string:cart_item_id>', 'remove_from_cart', cartController.remove_from_cart, methods=['POST'])
app.add_url_rule('/cart/checkout', 'checkout', cartController.checkout, methods=['POST'])

if __name__ == '__main__':
    with app.app_context():  # اطمینان از مقداردهی دیتابیس در محیط اپلیکیشن
        db.create_all()
    app.run(port=8080, debug=True)
