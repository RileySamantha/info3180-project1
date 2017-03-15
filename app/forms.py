
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired
from wtforms import TextField, RadioField, DateField, FileField
from wtforms.validators import DataRequired, Required, InputRequired
from wtforms import validators
from flask_wtf.file import FileField, FileAllowed, FileRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class Userprofile(FlaskForm):
    firstname = StringField('Firstname', validators=[InputRequired()])
    lastname = StringField('Lastname', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    age = DateField('Age', format='%Y-%m-%d', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[('Male','Male'), ('Female', 'Female')], validators=[InputRequired()])
    biography = StringField('Biography', validators=[InputRequired()])
    image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])