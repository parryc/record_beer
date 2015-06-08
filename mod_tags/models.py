from app import db
from datetime import datetime
from helper_db import *

class Tags(db.Model):
  __tablename__ = 'tags'

  id = db.Column(db.Integer, primary_key=True)
  user = db.Column(db.Integer, db.ForeignKey('users.id'))
  beer = db.Column(db.Integer, db.ForeignKey('beers.id'))
  tag = db.Column(db.Text())

  def __init__(self, user, beer, tag):
    self.user = user
    self.beer = beer
    self.tag = tag

  def __repr__(self):
    return '<%r %r  - %r>' % (self.brewery, self.name, self.users.name)


##########
# CREATE #
##########

def add_tag(tag, beer, user):
  tag_entry = Tags(
    user=user,
    beer=beer,
    tag=tag
    )

  db.session.add(tag_entry)
  return commit_entry(tag_entry)

###########
# GETTERS #
###########

def get_tag(_id):
  return Tags.query.get(_id)

def get_tags_by_beer(beer_id):
  return Tags.query.filter_by(beer=beer_id).all()

def get_tags_by_user(user_id):
  return db.session.query(Tags.tag).distinct()


##########
# DELETE #
##########

def delete_tags_for_beer(beer_id):
  tags = get_tags_by_beer(beer_id)
  for tag in tags:
    delete_result = delete_entry(tag)

  return delete_result
