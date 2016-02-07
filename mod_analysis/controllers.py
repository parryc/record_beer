#!/usr/bin/env python
# coding: utf-8
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app import db, ma, csrf
from mod_beers.models import *
from mod_users.models import *
from sqlalchemy import or_, and_
from marshmallow import fields
import calendar
from itertools import groupby

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
def show_brewery(brewery):
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

@mod_analysis.route('/year/<int:year>', methods=['GET'])
def show_year(year):
  beers = get_beers_by_year(year)
  count = len(beers)

  #########
  # TL;DR #
  #########

  avg_abv = round(sum([beer.abv for beer in beers])/float(count),2)
  avg_rating = round(sum([beer.rating for beer in beers])/float(count),2)
  top_three = sorted(beers, key=lambda x: x.rating, reverse=True)[:3]
  bottom_three = sorted(beers, key=lambda x: x.rating)[:3]

  tldr_data = {
    'avg_abv':avg_abv,
    'avg_rating':avg_rating,
    'top_three':top_three,
    'bottom_three':bottom_three
  }

  ##########
  # MONTHS #
  ##########

  # Not all months are necessarily filled
  month_totals = [0] * 12
  month_ratings = [0] * 12
  month_abvs = [0] * 12
  for key, group in groupby(beers,key=lambda x: x.drink_datetime):
    month_idx               = key.month - 1
    month_beers             = [g for g in group]
    month_totals[month_idx] = len(month_beers)
    month_ratings[month_idx]= calc_avg(month_beers,'rating')
    month_abvs[month_idx]   = (calc_avg(month_beers,'abv'))

  month_data = {
    'average':round(sum(month_totals)/float(len(month_totals)),2),
    'most':    (month(month_totals.index(max(month_totals))),max(month_totals)),
    'least':   (month(month_totals.index(min(month_totals))),min(month_totals)),
    'best':    (month(month_ratings.index(max(month_ratings))),max(month_ratings)),
    'worst':   (month(month_ratings.index(min(month_ratings))),min(month_ratings)),
    'booziest':(month(month_abvs.index(max(month_abvs))),max(month_abvs)),
    'soberest':(month(month_abvs.index(min(month_abvs))),min(month_abvs))
  }

  ##########
  # PLACES #
  ##########

  city_data = calculate_data(beers,'drink_city')
  country_data = calculate_data(beers,'drink_country')
  brewery_country_data = calculate_data(beers,'country')

  ##########
  # STYLES #
  ##########

  style_data = calculate_data(beers, 'style')

  ########
  # ABVS #
  ########

  abv_top_three = sorted(beers, key=lambda x: x.abv, reverse=True)[:3]
  abv_bottom_three = sorted(beers, key=lambda x: x.abv)[:3]
  abv_data = {'top':abv_top_three, 'bottom':abv_bottom_three}

  #############
  # BREWERIES #
  #############
  if year == 2011:
    brewery_data = calculate_data(beers,'brewery',override=True)
  else:
    brewery_data = calculate_data(beers,'brewery',override=False)

  return render_template('analysis/year.html'
                          ,year=year
                          ,beers=beers
                          ,tldr_data=tldr_data
                          ,month_data=month_data
                          ,city_data=city_data
                          ,country_data=country_data
                          ,brewery_country_data=brewery_country_data
                          ,style_data=style_data
                          ,abv_data=abv_data
                          ,brewery_data=brewery_data
                          )


###########
# HELPERS #
###########

def calc_avg(beers,attr):
  count = len(beers)
  return round(sum([getattr(beer,attr) for beer in beers])/float(count),2)

def month(idx):
  return calendar.month_name[idx+1]

def calculate_data(beers, attribute, override=False):
  keys = []
  totals = []
  ratings = []
  abvs = []
  count = 0
  beers.sort(key=lambda x: getattr(x,attribute))
  for key, group in groupby(beers,key=lambda x: getattr(x,attribute)):
    beers = [g for g in group]
    count += 1
    if len(beers) < 5 and not override:
      continue
    keys.append(key)
    totals.append(len(beers))
    ratings.append(calc_avg(beers,'rating'))
    abvs.append(calc_avg(beers,'abv'))

  return {
    'count':count, 
    'most':    (keys[totals.index(max(totals))],max(totals)),
    'least':   (keys[totals.index(min(totals))],min(totals)),
    'best':    (keys[ratings.index(max(ratings))],max(ratings)),
    'worst':   (keys[ratings.index(min(ratings))],min(ratings)),
    'booziest':(keys[abvs.index(max(abvs))],max(abvs)),
    'soberest':(keys[abvs.index(min(abvs))],min(abvs))
  }