#!/usr/bin/env python
# coding: utf-8
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app import db, ma, csrf
from mod_beers.models import *
from mod_users.models import *
from sqlalchemy import or_, and_
from marshmallow import fields

mod_analysis = Blueprint('details', __name__, url_prefix='/details')


##########
# Routes #
##########


# @mod_analysis.route('/', methods=['GET'])
# def index():
#     # there's only my beer at the moment. 
#     beers = Beers.query.all()
#     return render_template('beers/index.html',beers=beers)

@mod_analysis.route('/brewery/<brewery>', methods=['GET'])
def show(brewery):
    beers = get_beers_by_brewery(brewery)
    favorite_beer = beers[0]
    ratings = [beer.rating for beer in beers]
    average_rating = round(sum(ratings)/float(len(ratings)),2)
    abvs = [beer.abv for beer in beers]
    average_abv = round(sum(abvs)/float(len(abvs)),2)

    styles = {}
    for beer in beers:
        if beer.style not in styles:
            styles[beer.style] = (beer.rating, 1)
        else:
            _curr = styles[beer.style]
            styles[beer.style] = (_curr[0]+beer.rating,int(_curr[1])+1)

    favorite_style = ''
    favorite_style_rating = 0
    most_common_style = ''
    most_common_count = 0
    most_common_rating = 0
    for style in styles:
        _data = styles[style]
        rating = _data[0]/float(_data[1])
        if _data[1] > most_common_count:
            most_common_style = style
            most_common_count = _data[1]

        if rating > favorite_style_rating:
            favorite_style_rating = rating
            favorite_style = style

    return render_template('analysis/brewery.html'
                           ,brewery=brewery
                           ,beers=beers
                           ,favorite_beer=favorite_beer
                           ,favorite_style=favorite_style
                           ,favorite_style_rating=favorite_style_rating
                           ,most_common_style=most_common_style
                           ,most_common_count=most_common_count
                           ,average_rating=average_rating
                           ,average_abv=average_abv
                        )
