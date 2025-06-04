from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, TimeField, PasswordField
from wtforms.validators import DataRequired, Optional, Email, Length, EqualTo
from wtforms.widgets import ColorInput, CheckboxInput, ListWidget



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.')
    ])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(), EqualTo('new_password', message='Passwords must match')
    ])


class GoalForm(FlaskForm):
    name = StringField('Goal Name', validators=[DataRequired()])
    days = SelectMultipleField(
        'Days',
        choices=[('Mon', 'Mon'), ('Tue', 'Tue'), ('Wed', 'Wed'), 
                 ('Thu', 'Thu'), ('Fri', 'Fri'), ('Sat', 'Sat'), ('Sun', 'Sun')],
        option_widget=CheckboxInput(),
        widget=ListWidget(prefix_label=False)
    )
    start_time = TimeField('Start Time (optional)', format='%H:%M', render_kw={"placeholder": "HH:MM"}, default=None, validators=[Optional()])
    end_time = TimeField('End Time (optional)', format='%H:%M', render_kw={"placeholder": "HH:MM"}, default=None, validators=[Optional()])
    color = StringField('Color', widget=ColorInput(), default='#44aaff')
