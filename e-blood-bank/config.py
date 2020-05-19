import pymysql
import os

class Config(object):
	SECRET_KEY = 'random_string'
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/ebloodbank'
	SQLALCHEMY_TRACK_MODIFICATIONS = True