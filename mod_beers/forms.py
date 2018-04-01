from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, DecimalField, SelectField, IntegerField
from wtforms.validators import Required, NumberRange, Optional
from mod_tags.models import * 

class BeerForm(FlaskForm):
    brewery    = TextField('Brewery', [
                Required(message='Must provide a brewery.')])
    name = TextField('Beer name')

    abv = DecimalField('ABV',
            [Required(message='Must provide an ABV - if you don\'t know, just guess!'),
             NumberRange(0,50)])

    rating = DecimalField('Rating',
            [Required(message='Must provide a rating'),
             NumberRange(0,5)])

    style = TextField('Style',
            [Required(message='Must provide a style - if you don\'t know, just guess!')])

    country = TextField('Country',
            [Required(message='Must provide a country - if you don\'t know, just guess!')])

    drink_country = TextField('Drink Country')

    drink_city = TextField('Drink City')

    drink_datetime = TextField('Drink Date',
            [Required(message='Must provide a drink date - if you don\'t know, just guess!')])

    notes = TextAreaField('Notes')

    brew_year = IntegerField('Brew Year (Vintage)', [NumberRange(1900,3000), Optional()])

    brew_with = TextField('Brew With (Collaboration)')

    tags = TextField('Tags (Comma delimited)')