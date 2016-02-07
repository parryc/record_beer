#!/usr/bin/env python
# coding: utf-8
from flask import Flask, render_template, request
from flask.ext.assets import Environment, Bundle
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.marshmallow import Marshmallow
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)
assets = Environment(app)
ma = Marshmallow(app)
csrf = CsrfProtect()
#add csrf protection across the board
csrf.init_app(app)


@app.route('/')
def index():
  from mod_beers.models import Beers
  beer_count = Beers.query.count()
  breweries_count = db.session.query(Beers.brewery).distinct()
  styles_count = db.session.query(Beers.style).distinct()
  countries_count = db.session.query(Beers.country).distinct()
  latest_list = Beers.query.filter(Beers.user==1).order_by(Beers.creation_datetime.desc()).limit(10)
  latest = latest_list[0]
  return render_template('index.html',beer_count=beer_count,breweries_count=breweries_count
                                     ,styles_count=styles_count,countries_count=countries_count
                                     ,latest=latest,latest_list=latest_list
                                     ,t='record.beer')

@app.errorhandler(404)
def not_found(error):
  return render_template('404.html'), 404

# Define static asset bundles to be minimized and deployed
bundles = {
  'css_lib': Bundle('css/lib/normalize.css'
               ,'css/lib/skeleton.css'
               ,'css/style.css'
               ,'css/fonts/ptsans/fonts.css'
               ,'css/lib/flag-icon.min.css'
               ,filters='cssmin',output='gen/packed.css'),

  # jQuery migrate is used to support older jQuery libraries that have been upgraded to 1.10
  'js_lib' : Bundle('js/lib/jquery-1.10.2.min.js'
               ,'js/lib/jquery-migrate-1.2.1.min.js'
               ,'js/lib/jquery-debounce-1.0.5.js'
               ,'js/lib/handlebars-runtime.js'
               ,'js/init.js'
               ,filters='jsmin',output='gen/packed.js'
          ),
  'search' : Bundle('js/search.js'
               ,'js/search-results.js' 
               ,filters='jsmin',output='gen/search.js'),
  'query' : Bundle('js/query.js'
               ,'js/query-results.js' 
               ,filters='jsmin',output='gen/query.js')
  }
assets.register(bundles) 


# Import a module / component using its blueprint handler variable
from mod_beers.controllers import mod_beers
app.register_blueprint(mod_beers)
from mod_users.controllers import mod_users
app.register_blueprint(mod_users) 
from mod_analysis.controllers import mod_analysis
app.register_blueprint(mod_analysis) 
# from mod_tags.controllers import mod_tags
# app.register_blueprint(mod_tags)
