from flask import current_app as app
from extensions.extensions import db

from flask import Flask, render_template, request, redirect, url_for, flash, abort
from validators.Auth import Login, Reqister, EditProfile, ChangePassword
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from models.User import Users

class Authentication:

    def __init__(self, *args, **kwargs):
        pass

    def SignUp(self):
        if current_user.is_authenticated:
            return redirect(url_for('main'))

        form = Reqister()
        if request.method == 'POST':
            if form.validate_on_submit():  # اعتبارسنجی فرم
                name = form.name.data  # استفاده از form.name.data
                email = form.email.data  # استفاده از form.email.data
                password = form.password.data  # استفاده از form.password.data
                user = Users.query.filter_by(email=email).first()  # بررسی وجود کاربر
                if not user:
                    newUser = Users(name=name, email=email)
                    newUser.passwd = password  # تنظیم رمز عبور
                    db.session.add(newUser)
                    db.session.commit()  # ذخیره کاربر در دیتابیس
                    flash('User Created Successfully', 'success')
                    return redirect(url_for('SignUp'))
                else:
                    flash('User Exists, Please choose another email', 'error')
                    return redirect(url_for('SignUp'))
        return render_template('auth/signup.html', form=form)
    
    def SignIn(self):
        if current_user.is_authenticated:
            return redirect(url_for('main'))
        
        form = Login()
        if request.method == 'POST':
            if form.validate_on_submit():  # اعتبارسنجی فرم
                email = form.email.data  # استفاده از form.email.data
                password = form.password.data  # استفاده از form.password.data
                user = Users.query.filter_by(email=email).first()  # جستجوی کاربر
                if not user:
                    flash('User Not Exist, Please Try Again', 'warning')
                    return redirect(url_for('SignIn'))
                if user and user.IsOriginalPassword(password):  # بررسی رمز عبور
                    login_user(user)  # ورود کاربر
                    next_page = request.args.get('next')
                    return redirect(next_page) if next_page else redirect(url_for('main'))
        return render_template('/auth/signin.html', form=form)
    
    def SignOut(self):
        logout_user()  # خروج کاربر
        return redirect(url_for('main'))

    def EditProfile(self):
        if not current_user.is_authenticated:
            return redirect(url_for('SignIn'))

        form = EditProfile()
        if request.method == 'POST':
            if form.validate_on_submit():  # اعتبارسنجی فرم
                user = Users.query.filter_by(email=current_user.email).first()
                user.name = form.name.data  # استفاده از form.name.data
                user.email = form.email.data  # استفاده از form.email.data
                user.phone = form.phone.data  # استفاده از form.phone.data
                db.session.commit()  # ذخیره تغییرات
                flash('Profile Updated Successfully', 'success')
                return redirect(url_for('EditProfile'))
        return render_template('auth/editprofile.html', form=form)

    def ChangePassword(self):
        if not current_user.is_authenticated:
            return redirect(url_for('SignIn'))

        form = ChangePassword()
        if request.method == 'POST':
            if form.validate_on_submit():  # اعتبارسنجی فرم
                user = Users.query.filter_by(email=current_user.email).first()
                old_password = form.oldPassword.data  # استفاده از form.oldPassword.data
                new_password = form.newPassword.data  # استفاده از form.newPassword.data
                if not user.IsOriginalPassword(old_password):  # بررسی رمز عبور قدیمی
                    flash('Old Password is Incorrect', 'danger')
                    return redirect(url_for('ChangePassword'))
                user.passwd = new_password  # تنظیم رمز عبور جدید
                db.session.commit()  # ذخیره تغییرات
                flash('Password Changed Successfully', 'success')
                return redirect(url_for('ChangePassword'))
        return render_template('auth/changepassword.html', form=form)