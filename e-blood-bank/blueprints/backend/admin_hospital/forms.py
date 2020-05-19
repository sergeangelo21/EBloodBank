from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, PasswordField, SubmitField, SelectField, DecimalField, DateField
from wtforms.validators import DataRequired, EqualTo, ValidationError, NumberRange, Email

class HospitalInventoryForm(FlaskForm):
    blood_group = StringField('Blood Group', validators=[DataRequired()])
    bag_type = StringField('Bag Type', validators=[DataRequired()])
    extraction_date = StringField('Extraction Date', validators=[DataRequired()])
    cost = StringField('Cost', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Search_Inventory(FlaskForm):
    search = StringField('Search for')
    submit = SubmitField('Go')

class Select_Filter(FlaskForm):
    search = SelectField('Search for')
    submit = SubmitField('Go')