from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, SelectField, IntegerField
from wtforms.validators import NumberRange, Optional, InputRequired
from mod_tags.models import *


class BeerForm(FlaskForm):
    brewery = StringField("Brewery", [InputRequired(message="Must provide a brewery.")])
    name = StringField("Beer name")

    abv = DecimalField(
        "ABV",
        [
            InputRequired(
                message="Must provide an ABV - if you don't know, just guess!"
            ),
            NumberRange(0, 50),
        ],
    )

    rating = DecimalField(
        "Rating", [InputRequired(message="Must provide a rating"), NumberRange(0, 5)]
    )

    style = StringField(
        "Style",
        [
            InputRequired(
                message="Must provide a style - if you don't know, just guess!"
            )
        ],
    )

    country = StringField(
        "Country",
        [
            InputRequired(
                message="Must provide a country - if you don't know, just guess!"
            )
        ],
    )

    drink_country = StringField("Drink Country")

    drink_city = StringField("Drink City")

    drink_datetime = StringField(
        "Drink Date",
        [
            InputRequired(
                message="Must provide a drink date - if you don't know, just guess!"
            )
        ],
    )

    notes = TextAreaField("Notes")

    brew_year = IntegerField(
        "Brew Year (Vintage)", [NumberRange(1900, 3000), Optional()]
    )

    brew_with = StringField("Brew With (Collaboration)")

    tags = StringField("Tags (Comma delimited)")
