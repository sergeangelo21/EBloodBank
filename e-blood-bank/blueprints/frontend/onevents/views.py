from flask import Blueprint, render_template, url_for, redirect, request, current_app, jsonify, flash
from blueprints.backend.backend.models import user_account, user_role, user_personal, user_contact, user_address, blood_center, blood_request, blood_resource, event_information, event_participate, event_interview
from blueprints.frontend.onevents.forms import RegistrationForm
from flask_login import login_required, current_user
from extensions import db
import os

onevents = Blueprint('onevents', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@onevents.before_request
def before_request():
	if current_user.is_authenticated and not current_user.is_anonymous:
		if current_user.role_id != 4 or current_user.role_id != 5 or current_user.role_id != 6:
			if current_user.role_id == 1:
				return redirect('/backend')
			if current_user.role_id == 2:
				return redirect('/hospital')
			if current_user.role_id == 3:
				return redirect('/home')

#------------------------- ROSTER START -------------------------

@onevents.route('/onevent')
@login_required
def onevent():

	showevents = event_information.query.all()

	return render_template('home/index.html', title='Home', showevents=showevents)
	
@onevents.route('/onevent/show/<events_id>')
@login_required
def onevent_show(events_id):

	showevents_id = event_information.query.get(events_id)

	return render_template('home/show.html', title='Events | Event Information', events=showevents_id)

@onevents.route('/onevent/roster')
@login_required
def roster():

	roster = event_participate.query.join(
		user_account, user_personal, user_contact, user_address
		).add_columns(
		event_participate.user_id,
		user_account.user_id,
		user_personal.surname, 
		user_personal.first_name, 
		user_contact.email_address, 
		user_address.house_no, 
		user_address.street, 
		user_address.barangay, 
		user_address.town_municipality, 
		user_address.province_city, 
		event_participate.type, 
		event_participate.event_id
		).filter(
		event_participate.event_id
		).order_by(
		user_personal.surname.asc()
		).all()

	return render_template('roster/index.html', title='Roster', roster=roster)

@onevents.route('/onevent/roster/show/<events_id>')
@login_required
def roster_show(events_id):

	roster_id = user_personal.query.join(
		user_address, user_contact, user_account
		).add_columns(
		user_account.user_id, 
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
		user_contact.email_address
		).filter(
		user_account.user_id==events_id
		).first()

	return render_template('roster/show.html', title='Roster | Donor Information', roster=roster_id)

@onevents.route('/onevent/register', methods = ['GET', 'POST'])
@login_required
def register():

	form = RegistrationForm()

	if form.validate_on_submit():

		user = user_personal.query.join(
			user_contact
			).add_columns(
			user_contact.email_address
			).filter(
			user_contact.email_address==form.email_address.data
			).first()

		if user:
			return 'Account already exists!'
		else:

			#Setting Primary Keys (PS Manual for now T.T)
			user_id = user_personal.query.all()
			user_id = len(user_id) + 1
			contact_id = user_contact.query.all()
			contact_id = len(contact_id) + 1
			address_id = user_address.query.all()
			address_id = len(address_id) + 1
			event_id = event_participate.query.all()
			event_id = len(event_id) + 1

			#Insert into user_personal table            
			values = user_personal(
				id = user_id, 
				surname = form.surname.data, 
				first_name = form.first_name.data, 
				middle_name = form.middle_name.data, 
				birth_date = form.birth_date.data, 
				blood_group = form.blood_group.data, 
				civil_status = form.civil_status.data, 
				gender = form.gender.data, 
				nationality = form.nationality.data, 
				religion = form.religion.data, 
				education = form.education.data, 
				occupation = form.occupation.data
				)
			db.session.add(values)
			db.session.commit()

			#Insert into user_address table
			values = user_address(
				id = address_id, 
				user_id = user_id, 
				house_no = form.house_no.data, 
				street = form.street.data, 
				barangay = form.barangay.data, 
				town_municipality = form.town_municipality.data, 
				province_city = form.province_city.data, 
				zip_code = form.zip_code.data, 
				type = form.type.data
				)
			db.session.add(values)
			db.session.commit()

			#Insert into user_contact table
			values = user_contact(
				id = contact_id, 
				user_id = user_id, 
				telephone_no = form.telephone_no.data, 
				mobile_no = form.mobile_no.data, 
				email_address = form.email_address.data, 
				is_donor = 'Y'
				)
			db.session.add(values)
			db.session.commit()

			#Insert into event_participate table
			values = event_participate(
				id = event_id, 
				event_id = current_user.user_id,
				user_id = user_id, 
				status = 'A',
				type = 'W'
				)
			db.session.add(values)
			db.session.commit()

			return redirect(url_for('onevents.roster'))

	return render_template('register.html', title='Register', form=form)

@onevents.route('/onevent/interview', methods = ['GET', 'POST'])
@login_required
def interview():

	query = event_interview.query.all()

	categories = event_interview.query.group_by(event_interview.header).order_by(event_interview.id.asc())

	return render_template('interview.html', title='Interview', questions = query, categories = categories)


#------------------------- ROSTER END -------------------------