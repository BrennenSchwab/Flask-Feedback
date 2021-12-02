from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    """register form"""

    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=50)])
    email = StringField("Email", validators=[InputRequired(), Email(), Length(max=50)])
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])


class LoginForm(FlaskForm):
    """Login form"""

    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=50)])

class FeedbackForm(FlaskForm):
    """Add feedback form."""

    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = StringField("Content", validators=[InputRequired()])

class RemoveForm(FlaskForm):
    """used to remove form from page"""