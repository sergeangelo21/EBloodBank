from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, PasswordField, SubmitField, SelectField, DecimalField, DateField
from wtforms.validators import DataRequired, EqualTo, ValidationError, NumberRange, Email

class RegistrationForm(FlaskForm):
    surname = StringField('Surname', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    middle_name = StringField('Middle Name', validators=[DataRequired()])
    birth_date = StringField('Birthdate', validators=[DataRequired()])
    blood_group = StringField('Blood Group', validators=[DataRequired()])
    civil_status = StringField('Civil Status', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    nationality = StringField('Nationality', validators=[DataRequired()])
    religion = StringField('Religion', validators=[DataRequired()])
    education = StringField('Education', validators=[DataRequired()])
    occupation = StringField('Occupation', validators=[DataRequired()])
    house_no = StringField('House No.', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    barangay = StringField('Barangay', validators=[DataRequired()])
    town_municipality = StringField('Town/Municipality', validators=[DataRequired()])
    province_city = StringField('Province/City', validators=[DataRequired()])
    type = StringField('Address Type', validators=[DataRequired()])
    zip_code = StringField('Zip Code', validators=[DataRequired()])
    telephone_no = StringField('Telephone No.', validators=[DataRequired()])
    mobile_no = StringField('Mobile No.', validators=[DataRequired()])
    email_address = StringField('Email Address', validators=[DataRequired()])
    submit = SubmitField('Add')

class RegistrationForm_Update(FlaskForm):
    surname = StringField('Surname')
    first_name = StringField('First Name')
    middle_name = StringField('Middle Name')
    birth_date = StringField('Birthdate')
    blood_group = StringField('Blood Group')
    civil_status = StringField('Civil Status')
    gender = StringField('Gender')
    nationality = StringField('Nationality')
    religion = StringField('Religion')
    education = StringField('Education')
    occupation = StringField('Occupation')
    house_no = StringField('House No.')
    street = StringField('Street')
    barangay = StringField('Barangay')
    town_municipality = StringField('Town/Municipality')
    province_city = StringField('Province/City')
    type = StringField('Address Type')
    zip_code = StringField('Zip Code')
    telephone_no = StringField('Telephone No.')
    mobile_no = StringField('Mobile No.')
    email_address = StringField('Email Address')
    submit = SubmitField('Update')