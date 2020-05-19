from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length

usertpyes = [('admin','admin'),('nurse','nurse'),('user','user')]

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SignupForm(FlaskForm):
    surname = StringField('Surname', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    middle_name = StringField('Middle Name', validators=[DataRequired()])
    birth_date = StringField('Birthdate',validators=[DataRequired()])
    blood_group = SelectField('Blood Group', choices=[("", "---"),('O','O'),('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),('AB+','AB+'),('AB-','AB-')], validators=[DataRequired()])
    civil_status = SelectField('Civil Status', choices=[("", "---"),('S','Single'),('M','Married'),('W','Widowed')], validators=[DataRequired()])
    gender = SelectField('Gender', choices=[("",'Type'),('M','Male'),('F','Female')], validators=[DataRequired()])
    nationality = StringField('Nationality', validators=[DataRequired()])
    religion = StringField('Religion', validators=[DataRequired()])
    education = StringField('Education', validators=[DataRequired()])
    occupation = StringField('Occupation', validators=[DataRequired()])
    house_no = StringField('House No.', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    barangay = StringField('Barangay', validators=[DataRequired()])
    town_municipality = StringField('Town/Municipality', validators=[DataRequired()])
    province_city = StringField('Province/City', validators=[DataRequired()])
    type = SelectField('Address Type', choices=[("", "---"),('H','Home'),('O','Office')], validators=[DataRequired()])
    zip_code = StringField('Zip Code', validators=[DataRequired()])
    telephone_no = StringField('Telephone No.', validators=[DataRequired()])
    mobile_no = StringField('Mobile No.', validators=[DataRequired()])
    email_address = StringField('Email Address', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(max=30)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=30)])
    submit = SubmitField('Create')