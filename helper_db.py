# Don't delete record_beer from here.
# If you do, everything breaks, I don't know why.
# I have spent too long trying to fix it, so just leave it as is,
# unless you know how to fix what it breaks.
import sys

# Gandi hack, to get things to load
if sys.platform == "darwin":
    from record_beer.database import db
else:
    from database import db


def commit_entry(entry):
    try:
        db.session.commit()
        return {"status": True, "message": "Success", "entry": entry}
    except Exception as e:
        error = str(e).split(".")[0]
        return {"status": False, "message": "Error: %s" % error, "entry": None}


def delete_entry(entry):
    try:
        db.session.delete(entry)
        db.session.commit()
        return {"status": True, "message": "Success", "entry": entry.id}
    except Exception as e:
        error = str(e).split(".")[0]
        return {"status": False, "message": "Error: %s" % error, "entry": entry.id}


def get_counts(field):
    """ 
    Get count by field passed as input
    Ex. get_counts(Supersource.source_property)
    returns a list of tuples that are (field, count)
    e.g [(1, 14), (2, 3)] 
    (14 sources of property type 1, etc.)
  """
    return db.session.query(field, db.func.count(field)).group_by(field).all()
