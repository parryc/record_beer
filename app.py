from flask import Flask, render_template, request
from flask.ext.assets import Environment, Bundle
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.marshmallow import Marshmallow
from flask_wtf.csrf import CsrfProtect

import flask.ext.whooshalchemy as whooshalchemy
import os

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
  return render_template('index.html')

@app.errorhandler(404)
def not_found(error):
  return render_template('404.html'), 404

# Define static asset bundles to be minimized and deployed
bundles = {
  # jQuery migrate is used to support older jQuery libraries that have been upgraded to 1.10
  'js_lib' : Bundle('js/lib/jquery-1.10.2.min.js'
               ,'js/lib/jquery-migrate-1.2.1.min.js'
               ,'js/lib/jquery-debounce-1.0.5.js'
               ,'js/lib/handlebars-runtime.js'
               ,filters='jsmin',output='gen/packed.js'
          ),
  'mod_beers' : Bundle('js/search.js'
               ,'js/search-results.js' 
               ,filters='jsmin',output='gen/search.js')
  }
assets.register(bundles)  


# Import a module / component using its blueprint handler variable
from mod_beers.controllers import mod_beers
app.register_blueprint(mod_beers)
from mod_users.controllers import mod_users
app.register_blueprint(mod_users)
