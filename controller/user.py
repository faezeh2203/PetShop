from flask import current_app as app
from extensions.extensions import db

from extensions.utility import allow_extension

from werkzeug.utils import secure_filename
from models.User import Users
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from validators.Auth import EditProfile, ChangePassword
import os
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)

class Account:

    def __init__(self, *args, **kwargs):
        pass

    @login_required
    def account(self):
        return render_template('/account/index.html')
    
    @login_required
    def account_info(self):
        return render_template('/account/info.html')
    
    @login_required
    def account_password(self):
        form = ChangePassword()
        if request.method == 'POST':
            if form.validate_on_submit():
                old_password = form.oldPassword.data  # استفاده از form.oldPassword.data
                new_password = form.newPassword.data  # استفاده از form.newPassword.data
                try:
                    user = Users.query.filter_by(email=current_user.email).one()  # استفاده از Users
                    if not user.IsOriginalPassword(old_password):
                        flash('Old Password is Incorrect', 'danger')
                        return redirect(url_for('account_password'))
                    user.passwd = new_password
                    db.session.commit()  # ذخیره تغییرات
                    flash('Password Changed Successfully', 'success')
                    return redirect(url_for('account_password'))
                except NoResultFound:
                    flash('User Not Found', 'danger')
                    return redirect(url_for('account_password'))
        return render_template('/account/changepassword.html', form=form)
    
    @login_required
    def account_avatar(self):
        if request.method == 'POST' and 'avatar' in request.files:
            avatar = request.files['avatar']
            filename = avatar.filename
            file_secure = secure_filename(filename)
            if not allow_extension(filename):
                flash('Extension File is Not Allowed', 'danger')
                return redirect(url_for('account_avatar'))
            file_path = os.path.join(app.config['UPLOAD_DIR'], file_secure)
            avatar.save(file_path)
            try:
                user = Users.query.filter_by(email=current_user.email).one()  # استفاده از Users
                user.avatar = f'uploads/{filename}'
                db.session.commit()  # ذخیره تغییرات
                flash('Uploaded Picture Successfully', 'success')
                return redirect(url_for('account_avatar'))
            except NoResultFound:
                flash('User Not Found', 'danger')
                return redirect(url_for('account_avatar'))
        return render_template('/account/avatar.html')
    
    @login_required
    def account_edit(self):
        form = EditProfile()
        if request.method == 'POST':
            if form.validate_on_submit():
                name = form.name.data  # استفاده از form.name.data
                email = form.email.data  # استفاده از form.email.data
                phone = form.phone.data  # استفاده از form.phone.data
                try:
                    user = Users.query.filter_by(email=current_user.email).one()  # استفاده از Users
                    user.name = name
                    user.email = email
                    user.phone = phone
                    db.session.commit()  # ذخیره تغییرات
                    flash('Profile Updated Successfully', 'success')
                    return redirect(url_for('account_info'))
                except NoResultFound:
                    flash('User Not Found', 'danger')
                    return redirect(url_for('account_edit'))
        return render_template('/account/edit.html', form=form)