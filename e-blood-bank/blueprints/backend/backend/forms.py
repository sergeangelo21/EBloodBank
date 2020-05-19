from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, PasswordField, SubmitField, SelectField, DecimalField, DateField
from wtforms.validators import DataRequired, EqualTo, ValidationError, NumberRange, Email

class HospitalForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired()])
    address = StringField('Address', validators = [DataRequired()])
    email = StringField('Email Address', validators = [DataRequired()])
    telephone = StringField('Telephone No', validators = [DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Add')

class HospitalForm_Update(FlaskForm):
    name = StringField('Name')
    address = StringField('Address')
    email = StringField('Email Address')
    telephone = StringField('Telephone No')
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Update')

class EventForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired()])
    description = StringField('Description', validators = [DataRequired()])
    venue = StringField('Venue', validators = [DataRequired()])
    organizer = StringField('Organizer', validators = [DataRequired()])
    event_date = StringField('Event Date', validators = [DataRequired()])
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Add')

class EventForm_Update(FlaskForm):
    name = StringField('Name')
    description = StringField('Description')
    venue = StringField('Venue')
    organizer = StringField('Organizer')
    event_date = StringField('Event Date')
    submit = SubmitField('Update')

class InventoryForm(FlaskForm):
    blood_group = SelectField('Blood Group', choices=[("", "---"),('O','O'),('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),('AB+','AB+'),('AB-','AB-')], validators=[DataRequired()])
    bag_type = StringField('Bag Type', validators=[DataRequired()])
    extraction_date = StringField('Extraction Date', validators=[DataRequired()])
    cost = StringField('Cost', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PhlebotomistForm(FlaskForm):
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
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Add')

class PhlebotomistForm_Update(FlaskForm):
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
    password = PasswordField('Password')
    submit = SubmitField('Update')

class Search_Inventory(FlaskForm):
    search = StringField('Search for')
    submit = SubmitField('Go')

class Select_Filter(FlaskForm):
    search = SelectField('Search for')
    submit = SubmitField('Go')

class Request_RemarksForm(FlaskForm):
    action = SelectField('Status')
    reason = SelectField('Reason')
    #center = SelectField('Center')
    submit = SubmitField('Submit')