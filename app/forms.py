from flask import g
from flask_pagedown.fields import PageDownField
from flask_security.utils import verify_password
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])


class NewUserForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])


class EditProfileForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone')
    city = StringField('City')
    zipcode = StringField('Zipcode')
    address = StringField('Address & House Nr.')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current password', validators=[DataRequired()])
    new_password = PasswordField('New password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('new_password')])

    def validate_current_password(self, field):
        if not verify_password(field.data, g.user.password):
            raise ValidationError('Invalid password!')


class EditPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = PageDownField('Body', validators=[DataRequired()])


class EditEventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    description = PageDownField('Description', validators=[DataRequired()])
    start = DateTimeField('Starts on', validators=[DataRequired()], format='%d-%m-%Y %H:%M')
    end = DateTimeField('Ends on', validators=[DataRequired()], format='%d-%m-%Y %H:%M')
