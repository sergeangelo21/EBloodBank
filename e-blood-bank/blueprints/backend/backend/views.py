from flask import Blueprint, render_template, url_for, redirect, request, current_app, jsonify, flash
from flask_login import login_required, current_user
from sqlalchemy import or_, and_, func
from datetime import datetime
from blueprints.backend.backend.models import user_account, user_role, user_personal, user_contact, user_address, blood_center, blood_request, blood_resource, event_information, blood_purchase
from blueprints.backend.backend.forms import HospitalForm, HospitalForm_Update, EventForm, EventForm_Update, InventoryForm, PhlebotomistForm, PhlebotomistForm_Update, Search_Inventory, Select_Filter, Request_RemarksForm
from extensions import db
from flask_wtf import form
import os, pygal

backend = Blueprint('backend', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@backend.before_request
def before_request():
	if current_user.is_authenticated and not current_user.is_anonymous:
		if current_user.role_id != 1:
			if current_user.role_id == 2:
				return redirect('/hospital')
			if current_user.role_id == 3:
				return redirect('/home')
			if current_user.role_id == 4 or current_user.role_id == 5 or current_user.role_id == 6:
				return redirect('/onevent')

#------------------------- DASHBOARD START -------------------------

@backend.route('/backend')
@login_required
def dashboard():

	query = db.session.query(
		blood_resource.blood_group, 
		func.count(blood_resource.blood_group)
		).group_by(
		blood_resource.blood_group
		).all()

	pie_chart = pygal.Pie(inner_radius=.50)
	pie_chart.title = 'Blood Inventory'

	for blood_group in query:
		pie_chart.add(blood_group.blood_group, blood_group[1])

	pie_chart.render_response()



	return render_template('index.html', title='Dashboard', pie_chart=pie_chart, query=query)

#------------------------- DASHBOARD END -------------------------

#------------------------- REQUEST START -------------------------

@backend.route('/backend/request/<filter>/<search>', methods=['GET','POST'])
@login_required
def request(filter, search):
	
	form = Search_Inventory()

	if filter=='all':
		status= '#'
	elif filter=='new':
		status = 'N'
	elif filter=='pending':
		status = 'P'
	elif filter=='approved':
		status = 'A'
	elif filter=='declined':
		status = 'D'

	if filter=='all' and search=='#':
		query = blood_request.query.join(
			user_account, user_personal
			).add_columns(
			blood_request.id, 
			user_personal.surname, 
			user_personal.first_name, 
			user_personal.surname, 
			blood_request.patient, 
			blood_request.quantity, 
			blood_request.blood_group, 
			blood_request.purpose, 
			blood_request.date_created, 
			blood_request.date_processed, 
			blood_request.status, 
			blood_request.hospital_id
			).all()
	elif filter=='all' and search!='#':
		query = blood_request.query.join(
			user_account, user_personal
			).add_columns(
			blood_request.id, 
			user_personal.surname, 
			user_personal.first_name, 
			user_personal.surname, 
			blood_request.patient, 
			blood_request.quantity, 
			blood_request.blood_group, 
			blood_request.purpose, 
			blood_request.date_created, 
			blood_request.date_processed, 
			blood_request.status, 
			blood_request.hospital_id
			).filter(
			or_(
				blood_request.id.like('%'+search+'%'), 
				blood_request.blood_group.like('%'+search+'%'), 
				blood_request.patient.like('%'+search+'%'), 
				user_personal.surname.like('%'+search+'%'), 
				user_personal.first_name.like('%'+search+'%')
				)
			).all()		
	elif search=='#':
		query = blood_request.query.join(
			user_account, user_personal
			).add_columns(
			blood_request.id, 
			user_personal.surname, 
			user_personal.first_name, 
			user_personal.surname, 
			blood_request.patient, 
			blood_request.quantity, 
			blood_request.blood_group, 
			blood_request.purpose, 
			blood_request.date_created, 
			blood_request.date_processed, 
			blood_request.status, 
			blood_request.hospital_id
			).filter(
			and_(
				blood_request.hospital_id==current_user.id, 
				blood_request.status==status)
			).all()
	else:
		query = blood_request.query.join(
			user_account, user_personal
			).add_columns(
			blood_request.id, 
			user_personal.surname, 
			user_personal.first_name, 
			user_personal.surname, 
			blood_request.patient, 
			blood_request.quantity, 
			blood_request.blood_group, 
			blood_request.purpose, 
			blood_request.date_created, 
			blood_request.date_processed, 
			blood_request.status, 
			blood_request.hospital_id
			).filter(
			and_(
				blood_request.hospital_id==current_user.id,
				blood_request.status==status,
				or_(
					blood_request.id.like('%'+search+'%'), 
					blood_request.blood_group.like('%'+search+'%'), 
					blood_request.patient.like('%'+search+'%'), 
					user_personal.surname.like('%'+search+'%'), 
					user_personal.first_name.like('%'+search+'%')
					)
				)
			).order_by(
			blood_request.id.asc()
			).all()

	if form.validate_on_submit():
		search = form.search.data
		if not search:
			search = '#'
		return redirect(url_for('backend.request', filter=filter, search=search))

	return render_template('request/index.html', title='Request', status_count = len(query), status=status, request = query, form=form, filter=filter, search=search)

@backend.route('/backend/request/show/<request_id>', methods = ['GET','POST'] )
@login_required
def request_show(request_id):

	request = blood_request.query.filter(blood_request.id==request_id).first()

	blood = blood_resource.query.filter(and_(blood_resource.center_id==request.hospital_id, blood_resource.blood_group==request.blood_group, blood_resource.status=='A')).all()

	form = Request_RemarksForm()


	form.action.choices = [('A','Approve'),('P','Hold'),('D','Decline')]
	form.reason.choices = [('Spoilage','Spoilage'),('Outage','Outage')]

	if form.validate_on_submit():

		if form.action.data == 'A':

			if blood:

				if len(blood)<request.quantity:
					request.status = 'P'
					request.date_processed = datetime.now()
					db.session.commit()
					return 'Insufficient resources. Request was placed on pending.'

				else:

					limit=0
					#Add request for purchasing
					purchase = blood_purchase.query.all()
					purchase_id = len(purchase) + 1

					for b in blood:

						values = blood_purchase(
							id = purchase_id,
							blood_id = b.id,
							request_id = request.id,
							seller_id = b.center_id,
							date_purchased = None,
							status = 'U'
							)

						db.session.add(values)
						db.session.commit()

						b.status = 'U'
						db.session.commit()

						limit+=1
						purchase_id+=1

						if limit==request.quantity:
							break

					request.status = 'A'

				request.date_processed = datetime.now()
				db.session.commit()

			else:

				request.status = 'P'
				request.remarks = 'Outage'
				request.date_processed = datetime.now()

				db.session.commit()	
				return 'No more available resource! Request was placed on pending.'
		
		elif form.action.data=='P':

			request.status = form.action.data
			request.date_processed = datetime.now()

			db.session.commit()		

		else:

			#Update Request Info
			request.status = form.action.data
			request.remarks = form.reason.data
			request.date_processed = datetime.now()

			db.session.commit()		

	return render_template('request/show.html', title='Request | Request Information', avail = len(blood), request=request, form=form)

#------------------------- REQUEST END -------------------------

#------------------------- DONORS START -------------------------

@backend.route('/backend/donors')
@login_required
def donors():

	query = user_personal.query.join(
		user_contact, user_address, user_account
		).add_columns(
		user_personal.id, 
		user_personal.first_name, 
		user_personal.surname, 
		user_contact.email_address, 
		user_address.province_city, 
		user_personal.blood_group, 
		user_account.status
		).filter(
		user_contact.is_donor=='Y', user_account.role_id=='3'
		).all()

	return render_template('donors/index.html', title='Donors', donors=query)

@backend.route('/backend/donors/show/<donors_id>')
@login_required
def donors_show(donors_id):

	donors_id = user_personal.query.join(
		user_contact, user_address
		).add_columns(
		user_personal.id, 
		user_personal.first_name, 
		user_personal.surname, 
		user_contact.email_address, 
		user_address.house_no, 
		user_address.street, 
		user_address.barangay, 
		user_address.town_municipality, 
		user_address.province_city, 
		user_address.zip_code, 
		user_personal.blood_group, 
		user_personal.gender, 
		user_personal.civil_status, 
		user_personal.birth_date, 
		user_contact.mobile_no, 
		user_personal.nationality, 
		user_personal.occupation
		).filter(
		user_personal.id==donors_id
		).first()

	return render_template('donors/show.html', title='Donors | Donors Information', donors=donors_id)

@backend.route('/backend/donors/enable/<donors_id>')
@login_required
def donors_enable(donors_id):

	donor = user_account.query.filter(user_account.user_id==donors_id).first()
	donor.status = 'A'
	db.session.commit()

	return redirect (url_for('backend.donors'))

@backend.route('/backend/donors/disable/<donors_id>')
@login_required
def donors_disable(donors_id):

	donor = user_account.query.filter(user_account.user_id==donors_id).first()
	donor.status = 'D'
	db.session.commit()

	return redirect (url_for('backend.donors'))
	
#------------------------- DONORS END -------------------------

#------------------------- HOSPITALS START -------------------------

@backend.route('/backend/hospitals', methods=['GET', 'POST'])
@login_required
def hospitals():

	hospitals = blood_center.query.filter(blood_center.id!=1).all()

	return render_template('hospitals/index.html', title='Hospitals', hospitals=hospitals)

@backend.route('/backend/hospitals/show/<hospitals_id>')
@login_required
def hospitals_show(hospitals_id):

	hospitals = blood_center.query.filter(
		blood_center.id==hospitals_id
		).first()

	return render_template('hospitals/show.html', title='Hospitals | Hospital Information', hospitals=hospitals)

@backend.route('/backend/hospitals/add', methods=['GET', 'POST'])
@login_required
def hospitals_add():

	form = HospitalForm()

	if form.validate_on_submit():

		center = blood_center.query.join(
				user_account
				).add_columns(
				user_account.username,
				user_account.password
				).filter(
				user_account.username==form.username.data
				).first()

		if center:
			return "Hospital already exists!"

		else:

			user_id = blood_center.query.all()
			user_id = len(user_id) + 1
			center_id = blood_center.query.all()
			center_id = len(center_id) + 1
			account_id = user_account.query.all()
			account_id = len(account_id) + 1

			values = blood_center(
				id = center_id, 
				account_id = account_id,
				name = form.name.data, 
				address = form.address.data,
				email_address = form.email.data,
				telephone_number = form.telephone.data,
				)

			db.session.add(values)
			db.session.commit()

			values = user_account(
				id = account_id,
				user_id = user_id,
				role_id = '2',
				username = form.username.data,
				password = form.password.data,
				date_created = datetime.now(),
				last_active = datetime.now(),
				status = 'A'
				)

			db.session.add(values)
			db.session.commit()

			return "Hospital Added!"

	return render_template('hospitals/add.html', title='Hospitals | Add', forms=form)

@backend.route('/backend/hospitals/edit/<hospitals_id>', methods=['GET', 'POST'])
@login_required
def hospitals_edit(hospitals_id):

	hospital = blood_center.query.join(
		user_account
		).add_columns(
		blood_center.name,
		blood_center.address,
		blood_center.email_address,
		blood_center.telephone_number,
		user_account.username,
		user_account.password
		).filter(
		blood_center.id==hospitals_id
		).first()

	form = HospitalForm_Update()

	if form.validate_on_submit():

		testname = blood_center.query.filter_by(name=form.name.data).first()

		if testname is not None and not testname.name==hospital.name:
			flash('Hospital name is already taken.')
			return redirect(url_for('backend.hospitals_edit', hospitals=testname.id))

		hospital = blood_center.query.filter(
			blood_center.id==hospitals_id
			).first()

		hospital.name = form.name.data
		hospital.address = form.address.data
		hospital.email_address = form.email.data
		hospital.telephone_number = form.telephone.data

		db.session.commit()

		hospital = user_account.query.join(
			blood_center
			).add_columns(
			blood_center.id
			).filter(
			blood_center.id==hospitals_id
			).first()

		hospital.user_account.username = form.username.data
		hospital.user_account.password = form.password.data

		db.session.commit()
		
		return redirect(url_for('backend.hospitals'))

	else:

		form.name.data = hospital.name
		form.address.data = hospital.address
		form.email.data = hospital.email_address
		form.telephone.data = hospital.telephone_number
		form.username.data = hospital.username
		form.password.data = hospital.password

	return render_template('hospitals/edit.html', title='Hospitals | Edit', form=form)

#------------------------- HOSPITALS END -------------------------

#------------------------- EVENTS START -------------------------

@backend.route('/backend/events')
@login_required
def events():

	events = event_information.query.all()

	return render_template('events/index.html', title='Events', events=events)

@backend.route('/backend/events/show/<events_id>')
@login_required
def events_show(events_id):

	events_id = event_information.query.get(events_id)

	return render_template('events/show.html', title='Events | Event Information', events=events_id)

@backend.route('/backend/events/add', methods=['GET', 'POST'])
@login_required
def events_add():

	form = EventForm()

	if form.validate_on_submit():

		event = event_information.query.filter(
				event_information.name==form.name.data
				).first()

		if event:
			return "Event already exists!"

		else:

			event_id = event_information.query.all()
			event_id = len(event_id) + 1

			account_id = user_account.query.all()
			account_id = len(account_id) + 1

			value = event_information(
				id = event_id, 
				name = form.name.data, 
				description = form.description.data,
				venue = form.venue.data,
				organizer = form.organizer.data,
				event_date = form.event_date.data,
				)

			db.session.add(value)
			db.session.commit()

			value = user_account(
				id = account_id, 
				user_id = event_id, 
				role_id = '6',
				username = form.username.data,
				password = form.password.data,
				date_created = datetime.now(),
				last_active = datetime.now(),
				status = 'A'
				)

			db.session.add(value)
			db.session.commit()

			return redirect(url_for('backend.events'))

	return render_template('events/add.html', title='Events | Add', forms=form)

@backend.route('/backend/events/edit/<events_id>', methods=['GET', 'POST'])
@login_required
def events_edit(events_id):

	event = event_information.query.get(events_id)

	form = EventForm_Update()

	if form.validate_on_submit():

		testname = event_information.query.filter_by(name=form.name.data).first()

		if testname is not None and not testname.name==event.name:
			flash('Event name is already taken.')
			return redirect(url_for('backend.events_edit', events=testname.id))

		event.name = form.name.data
		event.description = form.description.data
		event.venue = form.venue.data
		event.organizer = form.venue.data
		event.event_date = form.event_date.data

		db.session.commit()
		
		return redirect(url_for('backend.events'))

	else:

		form.name.data = event.name
		form.description.data = event.description
		form.venue.data = event.venue
		form.organizer.data = event.organizer
		form.event_date.data = event.event_date
	
	return render_template('events/edit.html', title='Events | Edit', form=form)

#------------------------- EVENTS END -------------------------

#------------------------- INVENTORY START -------------------------

@backend.route('/backend/inventory/<filter>/<search>', methods=['GET', 'POST'])
@login_required
def inventory(filter,search):

	if filter=='all':
		form = Search_Inventory()
		if search=='#':
			query = blood_resource.query.join(
				blood_center
				).add_columns(
				blood_resource.id, 
				blood_resource.blood_group, 
				blood_resource.bag_type, 
				blood_center.name, 
				blood_resource.extraction_date
				).all()
		else:
			query = blood_resource.query.join(
				blood_center
				).add_columns(
				blood_resource.id, 
				blood_resource.blood_group, 
				blood_resource.bag_type, 
				blood_center.name, 
				blood_resource.extraction_date
				).filter(
				or_(
					blood_resource.id.like('%'+search+'%'), 
					blood_resource.bag_type.like('%'+search+'%'), 
					blood_center.name.like('%'+search+'%')
					)
				).order_by(
				blood_resource.id.asc()
				).all()

	elif filter=='blood_group':

		form = Select_Filter()

		type = blood_resource.query.group_by(
			blood_resource.blood_group
			).order_by(
			blood_resource.blood_group.asc()
			)

		form.search.choices = [(g.blood_group, g.blood_group) for g in type]

		query = blood_resource.query.join(
			blood_center
			).add_columns(
			blood_resource.id, 
			blood_resource.blood_group, 
			blood_resource.bag_type, 
			blood_center.name, 
			blood_resource.extraction_date
			).filter(
			blood_resource.blood_group==search
			).all()

	elif filter=='hospital':

		form = Select_Filter()

		center = blood_center.query.order_by(
			blood_center.name.asc()
			)

		form.search.choices = [(c.name, c.name) for c in center]

		query = blood_resource.query.join(
			blood_center
			).add_columns(
			blood_resource.id, 
			blood_resource.blood_group, 
			blood_resource.bag_type, 
			blood_center.name, 
			blood_resource.extraction_date
			).filter(
			blood_center.name==search
			).all()

	elif filter=='blood_bag':

		form = Select_Filter()

		bag = blood_resource.query.group_by(
			blood_resource.bag_type
			).order_by(
			blood_resource.bag_type.asc()
			)

		form.search.choices = [(b.bag_type, b.bag_type) for b in bag]

		query = blood_resource.query.join(
			blood_center
			).add_columns(
			blood_resource.id, 
			blood_resource.blood_group, 
			blood_resource.bag_type, 
			blood_center.name, 
			blood_resource.extraction_date
			).filter(
			blood_resource.bag_type==search
			).all()

	if form.validate_on_submit():

		search = form.search.data
		
		if not search:
			search = '#'
		return redirect(url_for('backend.inventory', filter=filter, search=search))

	return render_template('inventory/index.html', title='Inventory', form = form, query = query, count = len(query), filter = filter, search = search)

@backend.route('/backend/inventory/show/<inventory_id>', methods=['GET', 'POST'])
@login_required
def inventory_show(inventory_id):

	inventory_id = blood_resource.query.get(inventory_id)

	return render_template('inventory/show.html', title='Inventory | Inventory Information', inventory=inventory_id)

@backend.route('/backend/inventory/add', methods=['GET','POST'])
@login_required
def inventory_add():

	form = InventoryForm()

	if form.validate_on_submit():

		resource_id = blood_resource.query.all()
		resource_id = len(resource_id) + 1

		value = blood_resource(
			id = resource_id, 
			blood_group = form.blood_group.data, 
			bag_type = form.bag_type.data,
			event_id = '1',
			center_id = current_user.user_id,
			extraction_date = form.extraction_date.data,
			cost = form.cost.data,
			status = 'A'
			)

		db.session.add(value)
		db.session.commit()

		return "Resource Added!"

	return render_template('inventory/add.html', title='Inventory | Add', forms=form)

#------------------------- INVENTORY END -------------------------

#------------------------- PHLEBOTOMIST START -------------------------

@backend.route('/backend/phlebotomist')
@login_required
def phlebotomist():

	phlebotomist = user_personal.query.join(
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
		user_contact.email_address
		).filter(
		user_account.role_id=='4'
		).all()

	return render_template('phlebotomist/index.html', title='Phlebotomist', phlebotomist=phlebotomist)

@backend.route('/backend/phlebotomist/show/<phlebotomist_id>')
@login_required
def phlebotomist_show(phlebotomist_id):

	phlebotomist_id = user_personal.query.join(
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
		user_contact.email_address
		).filter(
		user_personal.id==phlebotomist_id
		).first()

	return render_template('phlebotomist/show.html', title='Phlebotomist | Phlebotomist Information', phlebotomist=phlebotomist_id)

@backend.route('/backend/phlebotomist/add', methods=['GET','POST'])
@login_required
def phlebotomist_add():

	form = PhlebotomistForm()

	if form.validate_on_submit():

		user = user_personal.query.join(
			user_account, user_contact
			).add_columns(
			user_account.username, 
			user_contact.email_address
			).filter(
			user_account.username==form.username.data and user_contact.email_address==form.email_address.data
			).first()

		if user:
			return 'Account already exists!'
		else:

			#Setting Primary Keys (PS Manual for now T.T)
			user_id = user_personal.query.all()
			user_id = len(user_id) + 1
			account_id = user_account.query.all()
			account_id = len(account_id) + 1
			contact_id = user_contact.query.all()
			contact_id = len(contact_id) + 1
			address_id = user_address.query.all()
			address_id = len(address_id) + 1

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
				is_donor = 'N'
				)
			db.session.add(values)
			db.session.commit()

			#Insert into user_contact table
			values = user_account(
				id = account_id, 
				user_id = user_id, 
				role_id = '4', 
				username = form.username.data, 
				password = form.password.data, 
				date_created = datetime.now(), 
				last_active = datetime.now(), 
				status = 'A'
				)
			db.session.add(values)
			db.session.commit()

			return redirect(url_for('backend.phlebotomist'))

	return render_template('phlebotomist/add.html', title='Phlebotomist | Add', forms=form)

@backend.route('/backend/phlebotomist/edit/<phlebotomist_id>', methods=['GET', 'POST'])
@login_required
def phlebotomist_edit(phlebotomist_id):

	phlebotomist = user_personal.query.join(
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
		user_personal.id==phlebotomist_id
		).first()

	form = PhlebotomistForm_Update()

	if form.validate_on_submit():

		# testname = blood_center.query.filter_by(name=form.name.data).first()

		# if testname is not None and not testname.name==hospital.name:
		# 	flash('Hospital name is already taken.')
		# 	return redirect(url_for('backend.phlebotomist_edit', phlebotomist=testname.id))

		phlebotomist = user_personal.query.filter(
			user_personal.id==phlebotomist_id
			).first()

		phlebotomist.surname = form.surname.data
		phlebotomist.first_name = form.first_name.data
		phlebotomist.middle_name = form.middle_name.data
		phlebotomist.birth_date = form.birth_date.data
		phlebotomist.blood_group = form.blood_group.data
		phlebotomist.civil_status = form.civil_status.data
		phlebotomist.gender = form.gender.data
		phlebotomist.nationality = form.nationality.data
		phlebotomist.religion = form.religion.data
		phlebotomist.education = form.education.data
		phlebotomist.occupation = form.occupation.data

		db.session.commit()

		phlebotomist = user_address.query.join(
			user_personal
			).add_columns(
			user_personal.id
			).filter(
			user_personal.id==phlebotomist_id
			).first()

		phlebotomist.user_address.house_no = form.house_no.data
		phlebotomist.user_address.street = form.street.data
		phlebotomist.user_address.barangay = form.barangay.data
		phlebotomist.user_address.town_municipality = form.town_municipality.data
		phlebotomist.user_address.province_city = form.province_city.data
		phlebotomist.user_address.type = form.type.data
		phlebotomist.user_address.zip_code = form.zip_code.data

		db.session.commit()

		phlebotomist = user_contact.query.join(
			user_personal
			).add_columns(
			user_personal.id
			).filter(
			user_personal.id==phlebotomist_id
			).first()

		phlebotomist.user_contact.telephone_no = form.telephone_no.data
		phlebotomist.user_contact.mobile_no = form.mobile_no.data
		phlebotomist.user_contact.email_address = form.email_address.data

		db.session.commit()

		phlebotomist = user_account.query.join(
			user_personal
			).add_columns(
			user_personal.id
			).filter(
			user_personal.id==phlebotomist_id
			).first()

		phlebotomist.user_account.username = form.username.data
		phlebotomist.user_account.password = form.password.data
		
		db.session.commit()

		return redirect(url_for('backend.phlebotomist'))

	else:

		form.surname.data = phlebotomist.surname
		form.first_name.data = phlebotomist.first_name
		form.middle_name.data = phlebotomist.middle_name
		form.birth_date.data = phlebotomist.birth_date
		form.blood_group.data = phlebotomist.blood_group
		form.civil_status.data = phlebotomist.civil_status
		form.gender.data = phlebotomist.gender
		form.nationality.data = phlebotomist.nationality
		form.religion.data = phlebotomist.religion
		form.education.data = phlebotomist.education
		form.occupation.data = phlebotomist.occupation
		form.house_no.data = phlebotomist.house_no
		form.street.data = phlebotomist.street
		form.barangay.data = phlebotomist.barangay
		form.town_municipality.data = phlebotomist.town_municipality
		form.province_city.data = phlebotomist.province_city
		form.type.data = phlebotomist.type
		form.zip_code.data = phlebotomist.zip_code
		form.telephone_no.data = phlebotomist.telephone_no
		form.mobile_no.data = phlebotomist.mobile_no
		form.email_address.data = phlebotomist.email_address
		form.username.data = phlebotomist.username
		form.password.data = phlebotomist.password

	return render_template('phlebotomist/edit.html', title='Phlebotomist | Edit', form=form, phlebotomist=phlebotomist_id)

#------------------------- PHLEBOTOMIST END -------------------------

#------------------------- MESSAGES START -------------------------
@backend.route('/messages')
@login_required
def messages():

    #for profile
    user = user_personal.query.first()

    return render_template('messages.html', title='Messages', user=user)

#------------------------- MESSAGES END -------------------------

