from flask import Blueprint, render_template, redirect, Flask, jsonify, url_for, session, flash
from sqlalchemy import and_, or_
from datetime import datetime, timedelta
from flask_login import login_required, current_user
from blueprints.backend.backend.models import blood_request, event_information, user_personal, user_account, user_contact, user_address, event_participate, blood_center, blood_resource, blood_purchase
from blueprints.frontend.users.forms import RequestForm, UserForm_Update, PasswordForm_Update, IsDonor_Form 
from extensions import db
from flask_wtf import form
from wtforms import DateField
import json
import os

users = Blueprint('users', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@users.before_request
def before_request():
    if current_user.is_authenticated and not current_user.is_anonymous:
        if current_user.role_id != 3 and current_user.role_id == 1:
            return redirect('/backend')
        if current_user.role_id != 3 and current_user.role_id == 2:
            return redirect('/hospital')
        if current_user.role_id != 3 and current_user.role_id == 4 or current_user.role_id == 5:
            return redirect('/onevent')

@users.route('/home')
@login_required
def home():

    #for profile
    user = current_user.user_id

    return render_template('home.html', title='Home', user=user)

#------------------------- REQUEST START -------------------------

@users.route('/request', methods = ['GET', 'POST'])
@login_required
def request():

    hospitals = blood_center.query.all()
    
    #for profile
    user = current_user.user_id

    request = blood_center.query.all()
    all_request = blood_request.query.filter(and_(blood_request.user_id==user, blood_request.status!='N')).order_by(blood_request.date_created.desc()).all()

    if request:
        current_request = blood_request.query.filter(and_(blood_request.user_id==user, or_(blood_request.status=='N', blood_request.status=='A'))).order_by(blood_request.date_created.desc()).first()
        if current_request:
            purchase = blood_purchase.query.filter(and_(blood_purchase.request_id==current_request.id, blood_purchase.status=='U')).all()
    else:
        current_request=None
        purchase=None

    return render_template('request/request.html', title='Request', forms=form, all_request=all_request, current_request=current_request, user=user, hospitals=hospitals)

@users.route('/request/hospital/<center_id>', methods = ['GET', 'POST'])
@login_required
def request_center(center_id):

    center = blood_center.query.get(center_id)
    user = current_user.user_id

    stocks = blood_resource.query.filter(and_(blood_resource.center_id==center_id, blood_resource.status=='A')).all() 
    
    total = blood_request.query.filter(blood_request.hospital_id==center_id).all()
    granted = blood_request.query.filter(and_(blood_request.hospital_id==center_id, blood_request.status== 'A')).all()

    if len(total)!=0:
        accept = len(granted)/len(total) * 100
    else:
        accept = 0.00   

    return render_template('request/hospital_profile.html', title='Request | Hospital Profile', user=user, hospital=center, stocks = len(stocks), accept=accept)

@users.route('/request/<action>', methods=['GET','POST'])
@login_required
def request_action(action):

    if action == 'Append':
        return 'Append'
    elif action == 'Cancel':
        request = blood_request.query.filter(
            blood_request.user_id==current_user.user_id and blood_request.status=='N'
            ).order_by(
            blood_request.date_created.desc()
            ).first()
        request.status =  'C'
        db.session.commit()

        return redirect(url_for('users.request')) 

@users.route('/request/form/<center_id>', methods=['GET', 'POST'])
@login_required
def request_form(center_id):  

    form = RequestForm()
    center = blood_center.query.get(center_id)

    if form.validate_on_submit():

        total = blood_request.query.all()
        id = len(total)+1

        values = blood_request(
            id = id,
            user_id = current_user.user_id,
            hospital_id = center_id,
            patient = form.patient.data,
            quantity = form.quantity.data,
            blood_group  = form.blood_group.data,
            purpose = form.purpose.data,
            date_created  = datetime.now(),
            date_processed = None,
            remarks = None,
            status = 'N'
            )

        db.session.add(values)
        db.session.commit()

        return redirect(url_for('users.request'))

    return render_template('request/request_form.html', title='Request | Request Form', form=form, center=center)



#------------------------- REQUEST END -------------------------

#------------------------- EVENTS START -------------------------
 
@users.route('/events', methods=['GET','POST'])
@login_required
def events():

    #for profile
    user = current_user.user_id

    events = event_information.query.all()

    return render_template('events/events.html', title='Events', events=events, user=user)

@users.route('/events/show/<event_id>')
@login_required
def events_show(event_id):

    event_info = event_information.query.get(event_id)

    return render_template('events/eventshow.html', title='Events | Event Information', event=event_info)

@users.route('/events/<event_id>', methods=['GET','POST'])
@login_required
def events_join(event_id):
    
    event = event_participate.query.get(event_id)

    event_check = event_participate.query.filter(
        event_participate.event_id==event_id, event_participate.user_id==current_user.id
        ).first()

    if event_check:
        return 'Already joined event.'

    else:

        participate_id = event_participate.query.all()
        participate_id = len(participate_id) + 1

        values = event_participate(
            id = participate_id, 
            event_id = event_id,
            user_id = current_user.id,
            type = 'S',
            status = 'A'
            )   

        db.session.add(values)
        db.session.commit()
       
        return redirect(url_for('users.events')) 

#------------------------- EVENTS END -------------------------

@users.route('/prcc')
@login_required
def prcc():

    #for profile
    user = current_user.user_id

    return render_template('prcc.html', title='PRC-C', user=user)

@users.route('/help')
@login_required
def help():

    #for profile
    user = current_user.user_id

    return render_template('help.html', title='Help', user=user)

#------------------------- PROFILE START -------------------------

@users.route('/profile/personal/<user>')
@login_required
def profile(user):

    user = user_personal.query.join(
        user_contact, user_account
        ).add_columns(
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
        user_contact.is_donor,
        user_personal.blood_group, 
        user_account.status).filter_by(id=current_user.id).first()

    return render_template('profile/personal.html', title='Profile | Personal', user=user)

@users.route('/profile/location/<user>')
@login_required
def profile_location(user):

    user = user_personal.query.join(
        user_address, user_account, user_contact
        ).add_columns(
        user_personal.id,
        user_personal.first_name,
        user_personal.surname,
        user_personal.blood_group,
        user_contact.email_address,
        user_contact.is_donor,
        user_address.house_no,
        user_address.street,
        user_address.barangay,
        user_address.town_municipality,
        user_address.province_city,
        user_address.zip_code,
        user_account.status).filter_by(id=current_user.user_id).first()

    return render_template('profile/location.html', title='Profile | Location', user=user)

@users.route('/profile/education/<user>')
@login_required
def profile_education(user):

    user = user_personal.query.join(
        user_account, user_contact
        ).add_columns(
        user_personal.id,
        user_personal.first_name,
        user_personal.surname,
        user_personal.education,
        user_personal.occupation,
        user_contact.email_address,
        user_contact.is_donor,
        user_personal.blood_group,
        user_account.status).filter_by(id=current_user.user_id).first()

    return render_template('profile/education.html', title='Profile | Education', user=user)

@users.route('/profile/contact/<user>', methods=['GET', 'POST'])
@login_required
def profile_contact(user):

    user = user_personal.query.join(
        user_contact, user_account
        ).add_columns(
        user_personal.id,
        user_contact.telephone_no,
        user_contact.mobile_no,
        user_contact.email_address, 
        user_contact.is_donor,
        user_personal.first_name,
        user_personal.surname,
        user_personal.blood_group, 
        user_account.status).filter_by(id=current_user.id).first()

    return render_template('profile/contact.html', title='Profile | Contact', user=user)




#------------------------- PROFILE END -------------------------

#------------------------- DONORS START -------------------------

@users.route('/donors')
@login_required
def donors():

    donors = user_personal.query.join(
        user_contact, user_address
        ).add_columns(
        user_personal.id, 
        user_personal.first_name, 
        user_personal.surname, 
        user_contact.email_address,
        user_address.town_municipality, 
        user_address.province_city
        ).filter(
        user_contact.is_donor=='Y', user_account.role_id=='3'
        ).all()

    return render_template('donors.html', title='Donors', donors=donors)

#------------------------- DONORS END -------------------------



#------------------------- MESSAGE START -------------------------
@users.route('/messages')
@login_required
def messages():

    #for profile
    user = user_personal.query.first()

    return render_template('messages.html', title='Messages', user=user)


#------------------------- MESSAGE END -------------------------



#------------------------- SETTINGS START -------------------------
@users.route('/settings')
@login_required
def settings():

    #for profile
    user = user_personal.query.first()

    return render_template('settings.html', title='settings', user=user)




@users.route('/setting/settings/account/<user>',methods=['GET', 'POST'])
@login_required
def setting(user):

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
        user_contact.is_donor,
        user_account.username, 
        user_account.role_id,
        user_account.status).filter(and_(user_personal.id==current_user.user_id, user_account.role_id==session['role'])).first()

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
        user_update.user_personal.education = form.education.data
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

        db.session.commit()
        
        # return redirect(url_for('users.profile_settings_account'))

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
        form.education.data = user_update.education
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

    return render_template('setting/settings_account.html', title='setting | Settings | Account', user_update=user_update, form=form, user=user_update)




@users.route('/setting/settings/password/<user>',methods=['GET', 'POST'])
@login_required
def setting_settings_password(user):

    user_update = user_personal.query.join(
        user_address, user_contact, user_account
        ).add_columns(
        user_personal.id, 
        user_personal.surname, 
        user_personal.first_name, 
        user_personal.blood_group,
        user_contact.email_address, 
        user_account.username, 
        user_account.password,
        user_contact.is_donor,
        user_account.status).filter_by(id=current_user.id).first()

    form = PasswordForm_Update()

    if form.validate_on_submit():

        # testname = blood_center.query.filter_by(name=form.name.data).first()

        # if testname is not None and not testname.name==hospital.name:
        #   flash('Hospital name is already taken.')
        #   return redirect(url_for('backend.phlebotomist_edit', phlebotomist=testname.id))

        if user_update.user_account.password == form.password.data:
            if form.password_new.data == form.password_confirm.data:
                user_update.user_account.password = form.password_new.data

        return 'Password not updated'


        db.session.commit()


    return render_template('setting/settings_password.html', title='setting | Settings | Password', user_update=user_update, form=form, user=user_update)    


@users.route('/setting/settings/other/<user>',methods=['GET', 'POST'])
@login_required
def setting_settings_other(user):

    user = user_personal.query.join(
        user_contact, user_account
        ).add_columns(
        user_personal.id,
        user_contact.email_address, 
        user_personal.first_name,
        user_personal.surname,
        user_personal.blood_group, 
        user_contact.is_donor,
        user_account.status).filter_by(id=current_user.id).first()

    user_update = user_contact.query.filter_by(id=current_user.user_id).first()

    form = IsDonor_Form()
    
    if form.validate_on_submit():

        if form.action.data == 'Y':
            user_update.is_donor = form.action.data
        else:
            user_update.is_donor = form.action.data

        db.session.commit()

        return redirect(url_for('users.setting_settings_other', user=current_user.user_id))

    return render_template('setting/settings_other.html', title='setting| Settings | Other Settings ', user=user, form=form, user_update=user_update)    
#------------------------- SETTINGS END -------------------------