import datetime
# import classes
from app.models.base_model import BaseModel
from app.models import db


class Event(db.Model, BaseModel):
	# table name
	__tablename__ = 'events'
	# displayed fields
	visible = ['id', 'information', 'user_id', 'type', 'title', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(
		db.String(40),
		db.ForeignKey('users.id'),
		nullable=True
	)
	user = db.relationship('User')
	information = db.Column(db.String)
	type = db.Column(db.String)
	title = db.Column(db.String)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
