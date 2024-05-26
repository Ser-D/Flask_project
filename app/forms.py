from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, Group


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    group = SelectField('Group', choices=[
        ('Customer1', 'Customer 1'),
        ('Customer2', 'Customer 2'),
        ('Customer3', 'Customer 3')], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    # def validate_group(self, group):
    #     if group.data not in ['Customer1', 'Customer2', 'Customer3']:
    #         raise ValidationError('Invalid group selected')


class TicketForm(FlaskForm):
    note = TextAreaField('Note', validators=[DataRequired()])
    submit = SubmitField('Submit')


class TicketAdminForm(FlaskForm):
    note = TextAreaField('Note', validators=[DataRequired()])
    group = SelectField('Group', choices=[
        ('Customer1', 'Customer 1'),
        ('Customer2', 'Customer 2'),
        ('Customer3', 'Customer 3')], validators=[DataRequired()])
    submit = SubmitField('Submit')
