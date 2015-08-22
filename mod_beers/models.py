from app import db, app
from mod_tags.models import *
from datetime import datetime
from helper_db import *
import pycountry

class Beers(db.Model):
    __tablename__ = 'beers'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    brewery = db.Column(db.Text())
    name = db.Column(db.Text())
    abv = db.Column(db.Float())
    rating = db.Column(db.Float())
    # probably should be foreign key with a style table
    #db.Column(db.Integer, db.ForeignKey('styles.id'))
    style = db.Column(db.Text())
    country = db.Column(db.Text())
    country_iso = db.Column(db.Text())
    drink_country = db.Column(db.Text())
    drink_city = db.Column(db.Text())
    # will have flag in user preference to store real time or just month/year
    drink_datetime = db.Column(db.DateTime)
    notes = db.Column(db.Text())
    brew_year = db.Column(db.Integer)
    brew_with = db.Column(db.Text())
    creation_datetime = db.Column(db.DateTime)
    last_updated = db.Column(db.DateTime)
    search_string = db.Column(db.Text())
    tags = db.relationship('Tags', backref='tags', cascade="all,delete", lazy='joined')

    def __init__(self, brewery, name, abv, rating, style, country, country_iso, drink_country, drink_city, drink_datetime, notes='', brew_year=None, brew_with='', tags=[], creation_datetime=None, last_updated=None):
        self.brewery = brewery
        self.name = name
        self.abv = abv
        self.rating = rating
        self.style = style
        self.country = country
        self.country_iso = country_iso
        self.drink_country = drink_country
        self.drink_city = drink_city
        self.drink_datetime = drink_datetime
        self.notes = notes
        self.brew_year = brew_year
        self.brew_with = brew_with
        if creation_datetime is None:
            creation_datetime = datetime.utcnow()
        if last_updated is None:
            last_updated = datetime.utcnow()
        self.creation_datetime = creation_datetime
        self.last_updated = last_updated
        self.search_string = ' '.join([brewery,name,style,country,brew_with])
        self.tags = tags

    def __repr__(self):
        return '<%r %r  - %r>' % (self.brewery, self.name, self.users.name)

##########
# CREATE #
##########

def add_beer(brewery, name, abv, style, country_name, rating, drink_country, drink_city, drink_datetime, notes, brew_year, brew_with, tags, user):
    country_iso = iso_code(country_name)
    beer_entry = Beers(
        brewery        = brewery
       ,name           = name
       ,abv            = abv
       ,style          = style
       ,country        = country_name
       ,country_iso    = country_iso
       ,rating         = rating
       ,drink_country  = drink_country
       ,drink_city     = drink_city
       ,drink_datetime = drink_datetime
       ,notes          = notes
       ,brew_year      = brew_year
       ,brew_with      = brew_with
       ,tags           = [])
    
    user.beers.append(beer_entry)
    save_beer_result = commit_entry(beer_entry)
    beer = save_beer_result['entry']

    saved_tags = []
    if save_beer_result['status'] and len(tags) > 0:
        for tag in tags:
            save_tag_result = add_tag(tag, beer.id, user.id)
            if save_tag_result['status']:
                saved_tags.append(save_tag_result['entry'])

        beer.tags = saved_tags
        return commit_entry(beer)
    else:
        return save_beer_result



##########
# UPDATE #
##########

def edit_beer(_id, brewery, name, abv, style, country_name, rating, drink_country, drink_city, drink_datetime, notes, brew_year, brew_with, tags):
    beer = get_beer(_id)
    country_iso = iso_code(country_name)
    beer.brewery        = brewery
    beer.name           = name
    beer.abv            = abv
    beer.style          = style
    beer.country        = country_name
    beer.country_iso    = country_iso
    beer.rating         = rating
    beer.drink_country  = drink_country
    beer.drink_city     = drink_city
    beer.drink_datetime = drink_datetime
    beer.notes          = notes
    beer.brew_year      = brew_year
    beer.brew_with      = brew_with
    beer.tags           = []

    save_beer_result = commit_entry(beer)
    beer = save_beer_result['entry']

    saved_tags = []
    if save_beer_result['status'] and len(tags) > 0:
        delete_tags_for_beer(_id)
        for tag in tags:
            save_tag_result = add_tag(tag.strip(), beer.id, beer.user)
            if save_tag_result['status']:
                saved_tags.append(save_tag_result['entry'])

        beer.tags = saved_tags
        return commit_entry(beer)
    else:
        return save_beer_result

###########
# GETTERS #
###########

def get_beer(_id):
    return Beers.query.get(_id)

def get_beers_by_brewery(_brewery,order_by='rating'):
    query = Beers.query.filter_by(brewery=_brewery).order_by(getattr(Beers,order_by).desc())
    return query.all()


###########
# HELPERS #
###########

def iso_code(country_name):
    if country_name == 'USA':
        return 'us'
    elif country_name == 'Taiwan':
        return 'tw'
    elif country_name == 'Scotland'\
      or country_name == 'England'\
      or country_name == 'Wales'\
      or country_name == 'Northern Ireland':
        return 'gb'
    elif country_name == 'Vietnam':
        return 'vn'
    elif country_name == 'Russia':
        return 'ru'
    elif country_name == 'South Korea':
        return 'sk'
    elif country_name == 'Laos':
        return 'la'
    else:
        return pycountry.countries.get(name=country_name).alpha2.lower()