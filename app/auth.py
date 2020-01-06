from flask import redirect, render_template, flash, Blueprint, request, url_for
from flask_login import login_required, logout_user, current_user, login_user
from werkzeug.security import generate_password_hash
from app.forms import LoginForm, SignupForm
from app.models import User,db
from app import login_manager


auth_bp = Blueprint('auth_bp',__name__,static_folder='static')

@auth_bp.route("/logout")
@login_required
def logout_page():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login_page'))




@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login_page'))


# @login_manager.request_loader
# def load_user(request):
#     a=1

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None :
        return User.query.get(user_id)
    return None

@auth_bp.route('/login',methods=['GET','POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.dashboard'))
    login_form=LoginForm(request.form)

    if request.method =='POST':
        if login_form.validate():
            # Get Form Fields
            email = request.form.get('email')
            password = request.form.get('password')
            # Validate Login Attempt
            user = User.query.filter_by(email=email).first()
            if user:
                if user.check_password(password=password):
                    login_user(user)
                    next = request.args.get('next')
                    return redirect(next or url_for('main_bp.dashboard'))
        flash('Invalid username/password combination')
        return redirect(url_for('auth_bp.login_page'))

    return render_template('login.html',form=LoginForm(),title='Login',body='Login')

@auth_bp.route('/testdata',methods=['GET','POST'])
def testdata():
    f=open('E:\jsondata.json')
    a=f.read()
    c= bytes(a,encoding='utf-8')
    import zlib
    b=zlib.compress(c)
    return b

@auth_bp.route('/sign_up',methods=['GET','POST'])
def signup_page():
    signup_form=SignupForm(request.form)

    if request.method=='POST':
        if signup_form.validate():
            name=request.form.get('name')
            email=request.form.get('email')
            pwd = request.form.get('password')
            existing_user= User.query.filter_by(email=email).first()
            if existing_user is None:
                user = User(name=name,
                            email=email,
                            password=generate_password_hash(pwd, method='sha256'),
                            )
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('auth_bp.login_page'))

    return render_template('signup.html',title='Create an Account | Flask-Login Tutorial.',
                           form=SignupForm(),
                           template='signup-page',
                           body="Sign up for a user account.")


