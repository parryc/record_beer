from flask_wtf import FlaskForm
from wtforms.fields import StringField


class UserForm(FlaskForm):
    default_drink_location_country = StringField("Drink Country")

    default_drink_location_city = StringField("Drink City")

    default_drink_date = StringField("Drink Date")
