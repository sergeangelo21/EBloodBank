from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired

class RequestForm(FlaskForm):
    patient = StringField('Patient\'s Name', validators = [DataRequired()])
    blood_group = StringField('Blood Group', validators = [DataRequired()])
    quantity = StringField('Quantity', validators = [DataRequired()])
    purpose = StringField('Purpose', validators = [DataRequired()])
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')
    append = SubmitField('Append')

class UserForm_Update(FlaskForm):
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
    username = StringField('Username')
    submit = SubmitField('Update')

class PasswordForm_Update(FlaskForm):
    password =  PasswordField('Old Password')
    password_new = PasswordField('New Password')
    password_confirm = PasswordField('Confirm Password')
    submit = SubmitField('Update')

class IsDonor_Form(FlaskForm):
    action = SelectField('Is donor', choices=[("","---"),("Y","Yes"),("N","No")])
    submit = SubmitField('Submit')
    
        
    