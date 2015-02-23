from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, DecimalField, SelectField
from wtforms.validators import Required, NumberRange

class BeerForm(Form):
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

    drink_datetime = TextField('Drink Date')

    notes = TextAreaField('Notes')
