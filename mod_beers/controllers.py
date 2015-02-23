#!/usr/local/bin/python
# coding: utf-8
from flask import Blueprint, render_template, request, jsonify
from app import db
from mod_beers.models import *
from mod_beers.forms import *
from mod_users.models import *
import json
import datetime
from ratebeer import RateBeer

mod_beers = Blueprint('beers', __name__, url_prefix='/beers')
rb = RateBeer()
#
# Routes
#


@mod_beers.route('/', methods=['GET'])
def index():
    # there's only my beer at the moment. 
    beers = Beers.query.all()
    return render_template('beers/index.html',beers=beers)

@mod_beers.route('/<int:_id>', methods=['GET'])
def show(_id):
    beer = get_beer(_id)
    return render_template('beers/show.html',beer=beer)

@mod_beers.route('/add', methods=['GET','POST'])
def add():
    form = BeerForm()
    if form.validate_on_submit():
        print 'success'
    return render_template('beers/add.html',form=form)

@mod_beers.route('/search', methods=['POST'])
def search():
    query = request.json['query']
    results = rb.search(query)
    if results['beers'] is not None:
        first_hit = results['beers'][0]
        hit = rb.beer(first_hit['url'])
        print hit
        return jsonify(hit)
    else:
        return jsonify({'success':False})

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