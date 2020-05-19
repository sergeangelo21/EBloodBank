from flask_login import UserMixin
from extensions import db	
from extensions import flask_login as login

@login.user_loader
def load_user(id):
    return user_account.query.get((id))

class user_account(UserMixin, db.Model):

	__tablename__ = 'user_account'
	id = db.Column(db.Integer, primary_key=True)
	user_id	 = db.Column(db.Integer, db.ForeignKey('user_personal.id'), nullable = False)
	role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'), nullable = False)
	username = db.Column(db.String(30), nullable=False)
	password = db.Column(db.String(30), nullable=False)
	date_created = db.Column(db.DateTime, nullable=False)
	last_active = db.Column(db.DateTime, nullable=False)
	status = db.Column(db.String(1), nullable = False)

	user_account_id = db.relationship('blood_center', backref='user_account', lazy=True)	
	user_request_id = db.relationship('blood_request', backref='user_account', lazy=True)
	user_participate_id = db.relationship('event_participate', backref='user_account', lazy=True)

	def __repr__(self, active=True):
		return '<user_account {}>' .format(self.username)

class user_role(db.Model):
	__tablename__='user_role'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(15), nullable = False)
	
	#Relationship
	account_role = db.relationship('user_account', backref='user_role', lazy=True)

class user_personal(db.Model):

	__tablename__ = 'user_personal'
	id = db.Column(db.Integer, primary_key=True)
	surname = db.Column(db.String(20), nullable=False)
	first_name = db.Column(db.String(30), nullable=False)
	middle_name = db.Column(db.String(20))
	birth_date = db.Column(db.Date, nullable = False)
	blood_group = db.Column(db.String(3), nullable = False)
	civil_status = db.Column(db.String(1), nullable = False)
	gender = db.Column(db.String(1), nullable = False)
	nationality = db.Column(db.String(10), nullable = False)
	religion = db.Column(db.String(30))
	education = db.Column(db.String(30))
	occupation = db.Column(db.String(30))
	
	#Relationships
	user_address_id = db.relationship('user_address', backref='user_personal', lazy=True)	
	user_contact_id = db.relationship('user_contact', backref='user_personal', lazy=True)

	def __repr__(self, active=True):
		return '<user_personal {}>' .format(self.surname)

class user_contact(db.Model):

	__tablename__ = 'user_contact'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user_personal.id'), nullable = False)
	telephone_no = db.Column(db.String(20))
	mobile_no = db.Column(db.String(15))
	email_address = db.Column(db.String(50))
	is_donor = db.Column(db.String(1), nullable = False)
		
	def __repr__(self, active=True):
		return '<user_contact {}>' .format(self.email_address)

class user_address(db.Model):

	__tablename__ = 'user_address'
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('user_personal.id'), nullable = False)
	house_no = db.Column(db.Integer)
	street = db.Column(db.String(30))
	barangay = db.Column(db.String(30))
	town_municipality = db.Column(db.String(20))
	province_city = db.Column(db.String(20))
	zip_code = db.Column(db.Integer)
	type = db.Column(db.String(1))

	def __repr__(self, active=True):
		return '<user_address {}>' .format(self.house_no)

class blood_request(db.Model):

	__tablename__ = 'blood_request'
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable = False)
	hospital_id = db.Column(db.Integer)
	patient = db.Column(db.String(50))
	quantity = db.Column(db.Integer)
	blood_group = db.Column(db.String(3))
	purpose = db.Column(db.String(30))
	date_created = db.Column(db.DateTime)
	date_processed = db.Column(db.DateTime)
	remarks = db.Column(db.String(10))
	status = db.Column(db.String(1))

	def __repr__(self, active=True):
		return '<blood_request {}>' .format(self.id)

class blood_center(db.Model):

	__tablename__ = 'blood_center'
	id = db.Column(db.Integer, primary_key = True)
	account_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable = False)
	name = db.Column(db.String(50))
	address = db.Column(db.String(60))
	email_address = db.Column(db.String(50))
	telephone_number = db.Column(db.String(20))

	#Relationships
	blood_center_id = db.relationship('blood_resource', backref='blood_center', lazy=True)

	def __repr__(self, active=True):
		return '<blood_center {}>' .format(self.email_address)

class blood_resource(db.Model):

	__tablename__ = 'blood_resource'
	id = db.Column(db.Integer, primary_key = True)
	blood_group = db.Column(db.String(3))
	bag_type = db.Column(db.String(10))
	event_id = db.Column(db.Integer)
	center_id = db.Column(db.Integer, db.ForeignKey('blood_center.id'), nullable=False)
	extraction_date = db.Column(db.DateTime)
	cost = db.Column(db.Numeric(4,2))
	status = db.Column(db.String(1))

class blood_purchase(db.Model):

	__tablename__ = 'blood_purchase'
	id = db.Column(db.Integer, primary_key = True)
	blood_id = db.Column(db.Integer, db.ForeignKey('blood_resource.id'), nullable = False)
	request_id = db.Column(db.Integer, db.ForeignKey('blood_request.id'), nullable = False)
	seller_id = db.Column(db.Integer, db.ForeignKey('blood_center.id'), nullable = False)
	date_purchased = db.Column(db.Date)
	status = db.Column(db.String(1))

	
class event_information(db.Model):

	__tablename__ = 'event_information'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(30))
	description = db.Column(db.String(50))
	venue = db.Column(db.String(60))
	organizer = db.Column(db.String(60))
	event_date = db.Column(db.DateTime)

	event_information_id = db.relationship('event_participate', backref='event_information', lazy=True)

class event_participate(db.Model):

	__tablename__ = 'event_participate'
	id = db.Column(db.Integer, primary_key = True)
	event_id = db.Column(db.Integer, db.ForeignKey('event_information.id'), nullable = False)
	user_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable = False)
	type = db.Column(db.String(1))
	status = db.Column(db.String(1))


class event_interview(db.Model):

	__tablename__ = 'event_interview'
	id = db.Column(db.Integer, primary_key = True)
	question = db.Column(db.String(100))
	header = db.Column(db.String(30))
	answer = db.Column(db.String(1))
	control = db.Column(db.Integer)