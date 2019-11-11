from database import db
from datetime import datetime
from helper_db import commit_entry, delete_entry

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    uses_full_drink_date = db.Column(db.Boolean())
    beers = db.relationship('Beers', backref='users', lazy='joined')
    default_drink_location_city = db.Column(db.Text())
    default_drink_location_country = db.Column(db.Text())
    default_drink_date = db.Column(db.DateTime)
    creation_datetime = db.Column(db.DateTime)
    last_updated = db.Column(db.DateTime)

    def __init__(self, name, uses_full_drink_date, default_drink_location_city, 
                 default_drink_location_country, default_drink_date, 
                 creation_datetime=None, last_updated=None):
        self.name = name
        self.uses_full_drink_date = uses_full_drink_date
        self.default_drink_location_city = default_drink_location_city
        self.default_drink_location_country = default_drink_location_country
        self.default_drink_date = default_drink_date
        if creation_datetime is None:
            creation_datetime = datetime.utcnow()
        if last_updated is None:
            last_updated = datetime.utcnow()
        self.creation_datetime = creation_datetime
        self.last_updated = last_updated

    def __repr__(self):
        return '<User %s>' % (self.name)


###########
# GETTERS #
###########

def get_user(_id):
    return Users.query.get(_id)


###########
# SETTERS #
###########

def edit_user(_id, drink_city, drink_country, drink_date):
    user = get_user(_id)
    user.default_drink_location_city = drink_city
    user.default_drink_location_country = drink_country
    user.default_drink_date = drink_date
    return commit_entry(user)