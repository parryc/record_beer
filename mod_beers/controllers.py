#!/usr/bin/env python
# coding: utf-8
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app import db, ma, csrf
from mod_beers.models import *
from mod_beers.forms import *
from mod_users.models import *
import json
import datetime
import unicodedata
import pycountry
import unicodecsv
from ratebeer import RateBeer
from ratebeer import rb_exceptions
from flask_wtf.csrf import CsrfProtect

mod_beers = Blueprint('beers', __name__, url_prefix='/beers')
rb = RateBeer()

##################
# Object schemas #
##################

class BeerSchema(ma.Schema):
  class Meta:
    fields = ('brewery', 'name', 'rating', 'style', 'country', 'country_iso', 'drink_datetime', 'abv')




##########
# Routes #
##########


@mod_beers.route('/', methods=['GET'])
def index():
    # there's only my beer at the moment. 
    beers = Beers.query.all()
    print Beers.query.whoosh_search(u'IPA').all()
    print '-----'
    print Beers.query.whoosh_search(u'ipa').all()
    return render_template('beers/index.html',beers=beers)

@mod_beers.route('/<int:_id>', methods=['GET'])
def show(_id):
    beer = get_beer(_id)
    return render_template('beers/show.html',beer=beer)

@mod_beers.route('/add', methods=['GET','POST'])
def add():
    form = BeerForm()
    if form.validate_on_submit():
        me = Users.query.get(1)
        country_name = form.country.data
        country_iso = iso_code(country_name)
        beer_entry = Beers(
            brewery=form.brewery.data
           ,name=form.name.data
           ,abv=form.abv.data
           ,style=form.style.data
           ,country=country_name
           ,country_iso=country_iso
           ,rating=form.rating.data
           ,drink_country=form.drink_country.data
           ,drink_city=form.drink_city.data
           ,drink_datetime=form.drink_datetime.data
           ,notes=form.notes.data)
        me.beers.append(beer_entry)
        db.session.add(beer_entry)
        db.session.commit()
        return redirect(url_for('.add'))
    return render_template('beers/add.html',form=form)

@mod_beers.route('/edit/<int:_id>', methods=['GET','POST'])
def edit(_id):
    beer = get_beer(_id)
    form = BeerForm(request.form,beer)
    if form.validate_on_submit():
        beer.brewery = form.brewery.data
        beer.name = form.name.data
        beer.abv = form.abv.data
        beer.style = form.style.data
        country_name = form.country.data
        beer.country = country_name
        beer.country_iso = iso_code(country_name)
        beer.rating = form.rating.data
        beer.drink_country = form.drink_country.data
        beer.drink_city = form.drink_city.data
        beer.drink_datetime = form.drink_datetime.data
        beer.notes = form.notes.data
        db.session.commit()
        flash(u'Save successful!')
        return redirect(url_for('.edit',_id=str(_id)))
    return render_template('beers/edit.html',form=form)


@mod_beers.route('/query', methods=['POST'])
def query():
    query = request.json['query']
    query_results = Beers.query.whoosh_search(query).all()
    results = BeerSchema(many=True).dump(query_results)
    return jsonify({'results':results.data})

@mod_beers.route('/search', methods=['POST'])
def search():
    def _dirtystrip(line):
        """
            Returns a RateBeer appropriate search string. Normalizes to get accents as
            individual characters and then strips them. ord < 256 allows characters like
            ø and ð to remain.            
        """
        line = unicodedata.normalize('NFKD',line)
        return ''.join([x for x in line if ord(x) < 256])
    def _closeness(search, result):
        """
            Quick function to try to get a representation of "closeness" to the search result,
            since ratebeer's results suck.
        """
        return len(set(search) ^ set(result))
    query = _dirtystrip(request.json['query'])
    print '***' + query + '***'
    results = rb.search(query)
    results = sorted(results['beers'],key=lambda beer: _closeness(query,beer['name']))
    top = []
    limit = 3
    if len(results) < 3:
        limit = len(results)
    if len(results) > 0:
        for idx in xrange(0,limit):
            result = results[idx]
            try:
                hit = rb.beer(result['url'])
            except rb_exceptions.AliasedBeer:
                limit += 1
                print 'AliasedBeer'
                continue
            top.append(hit)
        return jsonify({'results':top})
    else:
        return jsonify({'no_hits':True})

@mod_beers.route('/init', methods=['GET'])
def init():
    # there's only my beer at the moment. 
    me = Users.query.get(1)
    # filename = 'beer.json'
    # f = open(filename,'r')
    # beers = json.load(f)
    beers = list(unicodecsv.DictReader(open('export.csv', 'r')))
    for beer in beers:
        country_alpha2 = iso_code(beer['country'])
        beer_entry = Beers(
            brewery=beer['brewery'],
            name=beer['name'],
            abv=float(beer['abv']),
            rating=float(beer['rating']),
            style=beer['style'],
            country=beer['country'],
            country_iso=country_alpha2,
            drink_country=beer['drink_country'],
            drink_city=beer['drink_city'],
            drink_datetime=beer['drink_datetime'],
            notes=beer['notes']
        )
        db.session.add(beer_entry)
        me.beers.append(beer_entry)
    db.session.commit()
      # print beer.brewery + ' ' + beer.name
    return render_template('beers/index.html',beers=beers)


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