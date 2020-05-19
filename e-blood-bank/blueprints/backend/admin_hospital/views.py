from flask import Blueprint, render_template, url_for, redirect, request, current_app, jsonify, flash
from flask_login import login_required, current_user
from sqlalchemy import or_, and_, func
from datetime import datetime
from blueprints.backend.backend.models import blood_resource, blood_center
from blueprints.backend.admin_hospital.forms import HospitalInventoryForm, Search_Inventory, Select_Filter
from extensions import db
from flask_wtf import form
import os, pygal

admin_hospital = Blueprint('admin_hospital', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@admin_hospital.before_request
def before_request():
	if current_user.is_authenticated and not current_user.is_anonymous:
		if current_user.role_id != 2:
			if current_user.role_id == 1:
				return redirect('/backend')
			if current_user.role_id == 3:
				return redirect('/home')
			if current_user.role_id == 4 or current_user.role_id == 5 or current_user.role_id == 6:
				return redirect('/onevent')

#------------------------- ADMIN_HOSPITAL START -------------------------

@admin_hospital.route('/hospital')
@login_required
def dashboard():
	query = db.session.query(
		blood_resource.blood_group, 
		func.count(blood_resource.blood_group)
		).group_by(
		blood_resource.blood_group
		).filter(
		blood_resource.center_id==current_user.user_id).all()

	pie_chart = pygal.Pie(inner_radius=.50)
	pie_chart.title = 'Blood Inventory'

	for blood_group in query:
		pie_chart.add(blood_group.blood_group, blood_group[1])

	pie_chart.render_response()

	return render_template('admin_hospital/index.html', title='Hospital', pie_chart=pie_chart, query=query)


@admin_hospital.route('/hospital/inventory/<filter>/<search>', methods=['GET', 'POST'])
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
				).filter(
				blood_resource.center_id==current_user.user_id
				).all()
		else:
			query = blood_resource.query.join(
				blood_center
				).add_columns(
				blood_resource.id, 
				blood_resource.blood_group, 
				blood_resource.bag_type, 
				blood_center.name, 
				blood_resource.extraction_date,
				blood_resource.center_id
				).filter(
					or_(
						blood_resource.id.like('%'+search+'%'), 
						blood_resource.bag_type.like('%'+search+'%'), 
						blood_center.name.like('%'+search+'%'),
						and_(blood_resource.center_id==current_user.user_id)
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
			blood_resource.blood_group==search,
			blood_resource.center_id==current_user.user_id
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
			blood_resource.bag_type==search,
			blood_resource.center_id==current_user.user_id,
			).all()

	if form.validate_on_submit():

		search = form.search.data
		
		if not search:
			search = '#'
		return redirect(url_for('admin_hospital.inventory', filter=filter, search=search))

	return render_template('admin_hospital/inventory/index.html', title='Hospital', form = form, query = query, count = len(query), filter = filter, search = search)

@admin_hospital.route('/hospital/inventory/show/<inventory_id>', methods=['GET', 'POST'])
@login_required
def inventory_show(inventory_id):

	inventory_id = blood_resource.query.get(inventory_id)

	return render_template('admin_hospital/inventory/show.html', title='Inventory | Inventory Information', inventory=inventory_id)

@admin_hospital.route('/hospital/inventory/add', methods=['GET', 'POST'])
@login_required
def inventory_add():

	form = HospitalInventoryForm()

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

	return render_template('admin_hospital/inventory/add.html', title='Hospital | Inventory | Add', forms=form)


@admin_hospital.route('/hospital/prcc')
@login_required
def prcc():

    #for profile
    user = current_user.user_id

    return render_template('admin_hospital/prcc.html', title='PRC-C', user=user)

@admin_hospital.route('/hospital/help')
@login_required
def help():

    #for profile
    user = current_user.user_id

    return render_template('admin_hospital/help.html', title='Help', user=user)

#------------------------- ADMIN_HOSPITAL END -------------------------