from flask import Blueprint, render_template, redirect, Flask, jsonify, url_for
from datetime import datetime, timedelta
from flask_login import login_required, current_user
from blueprints.backend.models import blood_request, event_information, user_personal, user_account, user_contact, user_address
from blueprints.frontend.users.forms import RequestForm, UserForm_Update
from extensions import db
from flask_wtf import form
from wtforms import DateField
import json
import os

users = Blueprint('users', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@users.route('/home')
@login_required
def home():

    #for profile
    user = user_personal.query.first()

    return render_template('home.html', title='Home', user=user)

@users.route('/request', methods = ['GET', 'POST'])
@login_required
def request():
    
    #for profile
    user = user_personal.query.first()

    request = blood_request.query.filter(blood_request.user_id==current_user.id or blood_request.status=='N').first()

    form = RequestForm()

    if request:
        message = 'Your current request.'
    else:
        message = ''    

    if form.validate_on_submit():

        #Retrieve current PK Pointer
        request_id = blood_request.query.all()
        request_id = len(request_id) + 1

        value = blood_request(
                id = request_id, 
                user_id = current_user.id, 
                hospital_id = '1', 
                patient = form.patient.data, 
                quantity = form.quantity.data, 
                blood_group = form.blood_group.data, 
                purpose = form.purpose.data, 
                date_created = datetime.now(), 
                date_processed = '', 
                status = 'N')

        db.session.add(value)
        db.session.commit()
        return redirect(url_for('users.request')) 

    return render_template('request.html', title='Request', forms=form, message=message, request=request, user=user)

@users.route('/request/<action>', methods=['GET','POST'])
@login_required
def request_action(action):

    if action == 'Append':
        return 'Append'
    elif action == 'Cancel':
        request = blood_request.query.filter(
            blood_request.user_id==current_user.id or blood_request.status=='N'
            ).order_by(
            blood_request.date_created.desc()
            ).first()
        request.status =  'C'
        db.session.commit()
        return redirect(url_for('users.request')) 
 
@users.route('/events', methods=['GET','POST'])
@login_required
def events():

    #for profile
    user = user_personal.query.first()

    events = event_information.query.all()

    return render_template('events/events.html', title='Events', events=events, user=user)

@users.route('/prcc')
@login_required
def prcc():

    #for profile
    user = user_personal.query.first()

    return render_template('prcc.html', title='PRC-C', user=user)

@users.route('/help')
@login_required
def help():

    #for profile
    user = user_personal.query.first()

    return render_template('help.html', title='Help', user=user)

@users.route('/profile/personal')
@login_required
def profile():

    user = user_personal.query.join(
        user_contact, user_account).add_columns(
        user_personal.id, 
        user_personal.first_name,
        user_personal.middle_name, 
        user_personal.surname, 
        user_personal.gender, 
        user_personal.birth_date,
        user_personal.nationality,
        user_personal.civil_status,
        user_personal.religion,
        user_contact.email_address, 
        user_personal.blood_group, 
        user_account.status).filter_by(id=current_user.id).first()

    return render_template('profile/personal.html', title='Profile | Personal', user=user)

@users.route('/profile/location/<user_id>')
@login_required
def profile_location(user_id):

    user_id = user_personal.query.join(
        user_address, user_account, user_contact).add_columns(
        user_personal.id,
        user_personal.first_name,
        user_personal.surname,
        user_personal.blood_group,
        user_contact.email_address,
        user_address.house_no,
        user_address.street,
        user_address.barangay,
        user_address.town_municipality,
        user_address.province_city,
        user_address.zip_code,
        user_account.status).filter_by(id=current_user.id).first()

    return render_template('profile/location.html', title='Profile | Location', user=user_id)

@users.route('/profile/education/<user_id>')
@login_required
def profile_education(user_id):

    user_id = user_personal.query.join(
        user_account, user_contact).add_columns(
        user_personal.id,
        user_personal.first_name,
        user_personal.surname,
        user_personal.education,
        user_personal.occupation,
        user_contact.email_address,
        user_personal.blood_group,
        user_account.status).filter_by(id=current_user.id).first()

    return render_template('profile/education.html', title='Profile | Education', user=user_id)

@users.route('/profile/contact/<user_id>',methods=['GET', 'POST'])
@login_required
def profile_contact(user_id):

    user_id = user_personal.query.join(
        user_contact, user_account).add_columns(
        user_personal.id,
        user_contact.telephone_no,
        user_contact.mobile_no,
        user_contact.email_address, 
        user_personal.first_name,
        user_personal.surname,
        user_personal.blood_group, 
        user_account.status).filter_by(id=current_user.id).first()

    return render_template('profile/contact.html', title='Profile | Contact', user=user_id)

@users.route('/profile/settings/account/<user_id>'  )
@login_required
def profile_settings_account(user_id):

    user_update = user_personal.query.join(
        user_address, user_contact, user_account
        ).add_columns(
        user_personal.id, 
        user_personal.surname, 
        user_personal.first_name, 
        user_personal.middle_name, 
        user_personal.birth_date, 
        user_personal.blood_group, 
        user_personal.civil_status, 
        user_personal.gender, 
        user_personal.nationality, 
        user_personal.religion, 
        user_personal.education, 
        user_personal.occupation, 
        user_address.house_no, 
        user_address.street, 
        user_address.barangay, 
        user_address.town_municipality, 
        user_address.province_city, 
        user_address.zip_code, 
        user_address.type, 
        user_contact.telephone_no, 
        user_contact.mobile_no, 
        user_contact.email_address, 
        user_account.username, 
        user_account.password
        ).filter(
        user_personal.id==user
        ).first()

    form = UserForm_Update()

    if form.validate_on_submit():

        # testname = blood_center.query.filter_by(name=form.name.data).first()

        # if testname is not None and not testname.name==hospital.name:
        #   flash('Hospital name is already taken.')
        #   return redirect(url_for('backend.phlebotomist_edit', phlebotomist=testname.id))

        user_update.user_personal.surname = form.surname.data
        user_update.user_personal.first_name = form.first_name.data
        user_update.user_personal.middle_name = form.middle_name.data
        user_update.user_personal.birth_date = form.birth_date.data
        user_update.user_personal.blood_group = form.blood_group.data
        user_update.user_personal.civil_status = form.civil_status.data
        user_update.user_personal.gender = form.gender.data
        user_update.user_personal.nationality = form.nationality.data
        user_update.user_personal.religion = form.religion.data
        user_update.user_personal.occupation = form.occupation.data
        user_update.user_personal.house_no = form.house_no.data
        user_update.user_personal.street = form.street.data
        user_update.user_personal.barangay = form.barangay.data
        user_update.user_personal.town_municipality = form.town_municipality.data
        user_update.user_personal.province_city = form.province_city.data
        user_update.user_personal.type = form.type.data
        user_update.user_personal.zip_code = form.zip_code.data
        user_update.user_personal.telephone_no = form.telephone_no.data
        user_update.user_personal.mobile_no = form.mobile_no.data
        user_update.user_personal.email_address = form.email_address.data
        user_update.user_personal.username = form.username.data
        user_update.user_personal.password = form.password.data

        db.session.commit()
        
        return redirect(url_for('users.profile_settings_account'))

    else:

        form.surname.data = user_update.surname
        form.first_name.data = user_update.first_name
        form.middle_name.data = user_update.middle_name
        form.birth_date.data = user_update.birth_date
        form.blood_group.data = user_update.blood_group
        form.civil_status.data = user_update.civil_status
        form.gender.data = user_update.gender
        form.nationality.data = user_update.nationality
        form.religion.data = user_update.religion
        form.occupation.data = user_update.occupation
        form.house_no.data = user_update.house_no
        form.street.data = user_update.street
        form.barangay.data = user_update.barangay
        form.town_municipality.data = user_update.town_municipality
        form.province_city.data = user_update.province_city
        form.type.data = user_update.type
        form.zip_code.data = user_update.zip_code
        form.telephone_no.data = user_update.telephone_no
        form.mobile_no.data = user_update.mobile_no
        form.email_address.data = user_update.email_address
        form.username.data = user_update.username
        form.password.data = user_update.password

    #for profile
    user = user_personal.query.first()

    return render_template('profile/settings_account.html', title='Profile | Settings | Account', user=user_id)


@users.route('/messages')
@login_required
def messages():

    #for profile
    user = user_personal.query.first()

    return render_template('messages.html', title='Messages', user=user)