from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import Required, NumberRange, Optional
from mod_tags.models import * 

class UserForm(Form):
    default_drink_location_country = TextField('Drink Country')

    default_drink_location_city = TextField('Drink City')

    default_drink_date = TextField('Drink Date')