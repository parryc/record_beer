from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    flash,
    Markup,
)
from mod_beers.models import Beers, get_beer, edit_beer, add_beer
from mod_beers.forms import BeerForm
from mod_users.models import Users
from mod_tags.models import Tags
from ratebeer_fork import RateBeer
from ratebeer_fork import rb_exceptions
from sqlalchemy import or_, and_, desc
from marshmallow import fields, Schema

mod_beers = Blueprint("beers", __name__, url_prefix="/beers")
rb = RateBeer()

##################
# Object schemas #
##################


class TagSchema(Schema):
    tag = fields.Str()


class BeerSchema(Schema):
    class Meta:
        # model = Beers
        # json_module = simplejson
        additional = (
            "brewery",
            "name",
            "rating",
            "style",
            "country",
            "drink_country",
            "drink_city",
            "drink_datetime",
            "abv",
            "brew_with",
            "brew_year",
        )

    tags = fields.List(fields.Nested(TagSchema(only=("tag",), many=True)))


##########
# Routes #
##########


@mod_beers.route("/", methods=["GET"])
def index():
    # there's only my beer at the moment.
    beers = Beers.query.order_by(Beers.creation_datetime.desc()).all()
    return render_template("beers/index.html", beers=beers, t="record.beer")


@mod_beers.route("/<int:_id>", methods=["GET"])
def show(_id):
    beer = get_beer(_id)
    return render_template("beers/show.html", beer=beer, t=beer.name)


@mod_beers.route("/add", methods=["GET", "POST"])
def add():
    form = BeerForm()
    me = Users.query.get(1)
    if form.validate_on_submit():
        tags = form.tags.data.strip()

        if tags == u"":
            tags = []
        else:
            tags = tags.split(",")

        save_result = add_beer(
            form.brewery.data,
            form.name.data,
            form.abv.data,
            form.style.data,
            form.country.data,
            form.rating.data,
            form.drink_country.data,
            form.drink_city.data,
            form.drink_datetime.data,
            form.notes.data,
            form.brew_year.data,
            form.brew_with.data,
            tags,
            me,
        )
        if save_result["status"]:
            message = (
                'Added beer %s %s successfully! <a href="/beers/%s">(view)</a>'
                % (form.brewery.data, form.name.data, save_result["entry"].id)
            )
            flash(Markup(message))
            return redirect(url_for(".add"))
        else:
            flash("Could not add beer. %s" % save_result["message"])
    return render_template("beers/add.html", form=form, user=me, t="Add Beers")


@mod_beers.route("/edit/<int:_id>", methods=["GET", "POST"])
def edit(_id):
    def tags_to_csv(tags):
        _arr = [t.tag for t in tags]
        return ",".join(_arr)

    beer = get_beer(_id)
    form = BeerForm(obj=beer)
    if request.method != "POST":
        form.tags.data = tags_to_csv(beer.tags)
    if form.validate_on_submit():
        tags = form.tags.data.strip()

        if tags == u"":
            tags = []
        else:
            tags = tags.split(",")

        save_result = edit_beer(
            _id,
            form.brewery.data,
            form.name.data,
            form.abv.data,
            form.style.data,
            form.country.data,
            form.rating.data,
            form.drink_country.data,
            form.drink_city.data,
            form.drink_datetime.data,
            form.notes.data,
            form.brew_year.data,
            form.brew_with.data,
            tags,
        )
        if save_result["status"]:
            flash(
                "Updated beer %s %s successfully!" % (form.brewery.data, form.name.data)
            )
            return redirect(url_for(".edit", _id=str(_id)))
        else:
            flash("Could not update beer. Error: %s" % save_result["message"])

    return render_template("beers/edit.html", form=form, t="Edit Beers")


@mod_beers.route("/query", methods=["POST"])
def query():
    raw_query = request.json["query"]

    # print '***** query: %s *****' % raw_query

    if ":" in raw_query:
        parts = raw_query.split(":")
        prefix = parts[0].lower()
        search = parts[1]
        query = u"%{}%".format(search.strip())
    else:
        query = u"%{}%".format(raw_query.strip())

    user = request.json["user"]

    joined_results = []

    if ":" in raw_query:
        if prefix == "rating" or prefix == "abv":
            query_results = Beers.query.filter(Beers.user == user).filter(
                getattr(Beers, prefix) >= search
            )
        elif prefix == "tag":
            query_results = [
                get_beer(tag.beer)
                for tag in Tags.query.filter(Tags.user == user).filter(
                    Tags.tag.ilike(query)
                )
            ]
        else:
            query_results = Beers.query.filter(Beers.user == user).filter(
                getattr(Beers, prefix).ilike(query)
            )

    else:
        query_results = Beers.query.filter(
            and_(Beers.user == user, Beers.search_string.ilike(query))
        )

    results = BeerSchema(many=True).dump(query_results)
    # can't figure out how to get the new Marshmallow to return the data in
    # a flattened format for tags
    output = []
    for result in results:
        result["tags"] = [t["tag"] for t in result["tags"]]
        output.append(result)
    return jsonify({"results": output})


@mod_beers.route("/search", methods=["POST"])
def search():
    def _closeness(search, result):
        """
            Quick function to try to get a representation of "closeness" to the search result,
            since ratebeer's results suck.
        """
        return len(set(search) ^ set(result))

    query = request.json["query"]
    try:
        results = rb.search(query)
    except rb_exceptions.PageNotFound:
        return jsonify({"rate_limited": True})
    results = sorted(results["beers"], key=lambda beer: _closeness(query, beer.name))
    top = []
    limit = 3
    if len(results) < 3:
        limit = len(results)
    if len(results) > 0:
        for idx in range(0, limit):
            result = results[idx]
            try:
                hit = rb.beer(result.url)
            except rb_exceptions.AliasedBeer:
                limit += 1
                print("AliasedBeer")
                continue
            top.append(
                {
                    "name": hit["name"],
                    "abv": round(hit["abv"], 2),
                    "style": hit["style"],
                    "brewery_country": hit["brewery_country"],
                }
            )
        return jsonify({"results": top})
    else:
        return jsonify({"no_hits": True})


# @mod_beers.route('/init', methods=['GET'])
# def init():
#     # there's only my beer at the moment.
#     me = Users.query.get(1)
#     beers = list(unicodecsv.DictReader(open('beer_utf8.csv', 'r')))
#     for beer in beers:
#         if not beer['brew_year']:
#             beer['brew_year'] = None

#         tags = beer['tags'].strip()

#         if tags == u'':
#             tags = []
#         else:
#             tags = tags.split(';')

#         save_result = add_beer(
#             beer['brewery'],
#             beer['name'],
#             float(beer['abv']),
#             beer['style'],
#             beer['country'],
#             float(beer['rating']),
#             beer['drink_country'],
#             beer['drink_city'],
#             beer['drink_datetime'],
#             beer['notes'].replace('"',''),
#             beer['brew_year'],
#             beer['brew_with'],
#             tags,
#             me
#         )
#         if not save_result['status']:
#             print save_result['message']
#     return render_template('beers/index.html',beers=beers)
