from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp


class CreateUser(FlaskForm):
    name = StringField(
        label='Name',
        validators=[DataRequired('Name Field is Required')]
    )
    email = StringField(
        label='Email',
        validators=[
            DataRequired('Email Field is Required'),
            Email('Email is Invalid')
        ]
    )
    password = PasswordField(
        label='Password',
        validators=[
            DataRequired('Password Field Is Required!'),
            Length(min=8, message='Password Is Less Than 8 Characters')
        ]
    )
    confirm = PasswordField(
        label='Confirm Password',
        validators=[
            DataRequired('Confirm Password Field Is Required!'),
            Length(min=8, message='Password Is Less Than 8 Characters'),
            EqualTo('password', message='Confirm Does Not Match With Password')
        ]
    )
    admin = SelectField(
        label='Admin',
        choices=[('0', 'User'), ('1', 'Admin')],  # فقط 0 و 1 مجاز است
        validators=[DataRequired('Admin Field is Required')]
    )
    submit = SubmitField(label='Create User')


class EditUser(FlaskForm):
    name = StringField(
        label='Name',
        validators=[DataRequired('Name Field is Required')]
    )
    email = StringField(
        label='Email',
        validators=[
            DataRequired('Email Field is Required'),
            Email('Email is Invalid')
        ]
    )
    phone = StringField(
        label='Phone',
        validators=[
            DataRequired('Phone Field is Required'),
            Regexp(r'^\+?[0-9]{8,15}$', message='Phone Number is Invalid')
        ]
    )
    admin = SelectField(
        label='Admin',
        choices=[('0', 'User'), ('1', 'Admin')],  # فقط 0 و 1 مجاز است
        validators=[DataRequired('Admin Field is Required')]
    )
    submit = SubmitField('Update Account User')