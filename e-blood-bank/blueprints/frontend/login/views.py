from flask import Blueprint, render_template, url_for, redirect, flash, session
from blueprints.frontend.login.forms import SignupForm, LoginForm
from blueprints.backend.backend.models import user_account, user_role, user_personal, user_contact, user_address
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from extensions import db

login = Blueprint('login', __name__, template_folder="templates")
   
@login.route('/', methods=['GET', 'POST'])
def log_in():

    if current_user.is_authenticated and not current_user.is_anonymous:
        return redirect(url_for('backend.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        
        user = user_account.query.filter(user_account.username==form.username.data).first()

        if user is None or user.password!=form.password.data:

            flash('Invalid username or password')
            return redirect(url_for('login.log_in'))

        else:
            
            role = user_role.query.filter(user_role.id==user.role_id).first()
            session['role']=role.id

        login_user(user, remember=form.remember_me.data)

        if session['role']==1:
            return redirect(url_for('backend.dashboard'))
        elif session['role']==2:
            return redirect(url_for('admin_hospital.dashboard'))
        elif session['role']==6:
            return redirect(url_for('onevents.onevent'))
        else:
            return redirect(url_for('users.home'))

    return render_template('login.html', title='Sign In', form=form)

@login.route('/signup', methods=['GET', 'POST'])
def signup():

    form = SignupForm()
    
    if form.validate_on_submit():

        user = user_personal.query.join(user_account, user_contact).add_columns(user_account.username, user_contact.email_address).filter(user_account.username==form.username.data and user_contact.email_address==form.email_address.data).first()
        
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
                role_id = '3', 
                username = form.username.data, 
                password = form.password.data, 
                date_created = datetime.now(), 
                last_active = datetime.now(), 
                status = 'A'
                )
            db.session.add(values)
            db.session.commit()

            return redirect(url_for('login.log_in'))


    return render_template('signup.html', title='Sign Up', forms=form)

@login.route('/logout')
def logout():

    last_active = user_account.query.filter_by(id=current_user.id).first()
    last_active.last_active = datetime.now()

    db.session.commit()

    logout_user()
    session.pop('role')

    return redirect('/')