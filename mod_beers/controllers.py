#!/usr/local/bin/python
# coding: utf-8
from flask import Blueprint, render_template, request, jsonify, redirect
from app import db, csrf
from mod_beers.models import *
from mod_beers.forms import *
from mod_users.models import *
import json
import datetime
import unicodedata
from ratebeer import RateBeer
from flask_wtf.csrf import CsrfProtect

mod_beers = Blueprint('beers', __name__, url_prefix='/beers')
rb = RateBeer()
#
# Routes
#


@mod_beers.route('/', methods=['GET'])
def index():
    # there's only my beer at the moment. 
    beers = Beers.query.all()
    print Beers.query.whoosh_search('IPA').all()
    print '-----'
    print Beers.query.whoosh_search('ipa').all()
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
        beer_entry = Beer(
            brewery=form.brewery.data
           ,name=form.brewer.name
           ,abv=form.brewery.abv
           ,style=form.brewery.style
           ,country=form.brewery.country
           ,rating=form.brewery.rating
           ,drink_country=form.brewrey.drink_country
           ,drink_city=form.brewery.drink_city
           ,drink_datetime=form.brewery.drink_datetime
           ,notes=form.brewery.notes)
        me.beers.append(beer_entry)
        db.session.add(beer_entry)
        db.session.commit()
        return redirect(url_for('add'))
    return render_template('beers/add.html',form=form)

@mod_beers.route('/duplicate', methods=['POST'])
def duplicate():
    query = request.json['query']
    results = Beers.query.whoosh_search(query).all()
    return jsonify({'results':results})

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
            except RateBeer.AliasedBeer:
                limit += 1
                pass
            top.append(hit)
        return jsonify({'results':top})
    else:
        return jsonify({'no_hits':True})

@mod_beers.route('/init', methods=['GET'])
def init():
    # there's only my beer at the moment. 
    me = Users.query.get(1)
    filename = 'beer.json'
    f = open(filename,'r')
    beers = json.load(f)
    for beer in beers:
      beer_entry = Beers(
        brewery=beer['brewery'],
        name=beer['name'],
        abv=float(beer['abv']),
        rating=float(beer['rating']),
        style=beer['style'],
        country=beer['country'],
        drink_country=beer['drinkLocationCountry'],
        drink_city=beer['drinkLocationCity'],
        drink_datetime=datetime.datetime(beer['drinkYear'],beer['drinkMonth'],1),
        notes=beer['notes']
        )
      db.session.add(beer_entry)
      me.beers.append(beer_entry)
    db.session.commit()
      # print beer.brewery + ' ' + beer.name
    return render_template('beers/index.html',beers=beers)