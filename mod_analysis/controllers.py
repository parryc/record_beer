from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    flash,
    abort,
)
from mod_beers.models import (
    get_beers_by_attribute,
    get_beers_by_brewery,
    get_beers_by_rating,
    get_beers_by_style,
    get_beers_by_year,
    Beers,
    get_beer,
)

from mod_tags.models import *
import calendar
from itertools import groupby

mod_analysis = Blueprint("details", __name__, url_prefix="/details")

title_map = {
    "brewery": "Breweries",
    "name": "Beer Names",
    "abv": "ABVs",
    "rating": "Ratings",
    "style": "Styles",
    "country": "Brewery Countries",
    "drink_country": "Drink Location – Countries",
    "drink_city": "Drink Location – Cities",
    "year": "Years",
    "drink_datetime": "Drink – Datetime",
    "brew_year": "Vintage",
    "brew_with": "Collaborations",
    "tag": "Tags",
}

##########
# Routes #
##########


@mod_analysis.route("/", methods=["GET"])
def index():
    return render_template("analysis/index.html")


@mod_analysis.route("/<attribute>", methods=["GET"])
def show_index(attribute):
    beers = Beers.query.all()
    aggregate_list = []

    if attribute == "year":
        grouping = groupby(
            sorted(beers, key=lambda x: x.drink_datetime.year),
            key=lambda x: x.drink_datetime.year,
        )
    else:
        grouping = groupby(
            sorted(beers, key=lambda x: getattr(x, attribute)),
            key=lambda x: getattr(x, attribute),
        )
    for key, group in grouping:
        beer_list = [g for g in group]
        sum_ratings = sum([b.rating for b in beer_list])
        average = round(sum_ratings / float(len(beer_list)), 2)
        aggregate_list.append(
            {"name": key, "count": len(beer_list), "average": average}
        )

    sort = request.args.get("sort")
    reverse = True
    if sort not in ["name", "count", "average"]:
        sort = "name"
        reverse = False
    aggregate_list = sorted(aggregate_list, key=lambda x: x[sort], reverse=reverse)

    return render_template(
        "analysis/list.html",
        list=aggregate_list,
        type=attribute,
        t=title_map[attribute],
    )


@mod_analysis.route("/brewery/<brewery>", methods=["GET"])
def show_brewery(brewery):
    beers = get_beers_by_brewery(brewery)
    if not beers:
        abort(404)

    favorite_beer = beers[0]
    ratings = [beer.rating for beer in beers]
    average_rating = round(sum(ratings) / float(len(ratings)), 2)
    abvs = [beer.abv for beer in beers]
    average_abv = round(sum(abvs) / float(len(abvs)), 2)

    styles = {}
    for beer in beers:
        if beer.style not in styles:
            styles[beer.style] = (beer.rating, 1)
        else:
            _curr = styles[beer.style]
            styles[beer.style] = (_curr[0] + beer.rating, int(_curr[1]) + 1)

    favorite_style = ""
    favorite_style_rating = 0
    most_common_style = ""
    most_common_count = 0
    most_common_rating = 0
    for style in styles:
        _data = styles[style]
        rating = _data[0] / float(_data[1])
        if _data[1] > most_common_count:
            most_common_style = style
            most_common_count = _data[1]

        if rating > favorite_style_rating:
            favorite_style_rating = rating
            favorite_style = style

    return render_template(
        "analysis/brewery.html",
        brewery=brewery,
        beers=beers,
        favorite_beer=favorite_beer,
        favorite_style=favorite_style,
        favorite_style_rating=favorite_style_rating,
        most_common_style=most_common_style,
        most_common_count=most_common_count,
        average_rating=average_rating,
        average_abv=average_abv,
        t="Brewery: " + brewery,
    )


@mod_analysis.route("/tag", methods=["GET"])
def show_tag_index():
    beers = Beers.query.all()
    tags = {}

    for beer in beers:
        if not beer.tags:
            continue

        for tag in beer.tags:
            if not tag.tag in tags:
                tags[tag.tag] = {"name": tag.tag, "beer_list": [beer]}
            else:
                tags[tag.tag]["beer_list"].append(beer)

    for tag in tags:
        beer_list = tags[tag]["beer_list"]
        tags[tag]["count"] = len(beer_list)
        sum_ratings = sum([b.rating for b in beer_list])
        average = round(sum_ratings / float(len(beer_list)), 2)
        tags[tag]["average"] = average

    sort = request.args.get("sort")
    reverse = True
    if sort not in ["name", "count", "average"]:
        sort = "name"
        reverse = False
    tag_list = sorted(
        [item[1] for item in tags.items()], key=lambda x: x[sort], reverse=reverse
    )
    return render_template("analysis/list.html", list=tag_list, type="tag", t="Tags")


@mod_analysis.route("/tag/<tag>", methods=["GET"])
def show_tag(tag):
    beers = sorted(
        [get_beer(beer) for beer in get_beer_ids_by_tag(tag)],
        key=lambda x: x.rating,
        reverse=True,
    )
    favorite_beer = beers[0]
    ratings = [beer.rating for beer in beers]
    average_rating = round(sum(ratings) / float(len(ratings)), 2)
    abvs = [beer.abv for beer in beers]
    average_abv = round(sum(abvs) / float(len(abvs)), 2)

    breweries = {}
    for beer in beers:
        if beer.brewery not in breweries:
            breweries[beer.brewery] = (beer.rating, 1)
        else:
            _curr = breweries[beer.brewery]
            breweries[beer.brewery] = (_curr[0] + beer.rating, int(_curr[1]) + 1)

    most_common_brewery = ""
    most_common_count = 0
    for brewery in breweries:
        _data = breweries[brewery]
        rating = _data[0] / float(_data[1])
        if _data[1] > most_common_count:
            most_common_brewery = brewery
            most_common_count = _data[1]

    return render_template(
        "analysis/tag.html",
        tag=tag,
        beers=beers,
        favorite_beer=favorite_beer,
        most_common_brewery=most_common_brewery,
        most_common_count=most_common_count,
        average_rating=average_rating,
        average_abv=average_abv,
        t="Tag: " + tag,
    )


@mod_analysis.route("/abv", methods=["GET"])
def show_abv_index():
    beers = Beers.query.all()
    abvs = {}

    for beer in beers:
        if not round(beer.abv) in abvs:
            abvs[round(beer.abv)] = {
                "name": "{}% abv".format(round(beer.abv)),
                "beer_list": [beer],
                "sort_name": round(beer.abv),
            }
        else:
            abvs[round(beer.abv)]["beer_list"].append(beer)

    for abv in abvs:
        beer_list = abvs[abv]["beer_list"]
        abvs[abv]["count"] = len(beer_list)
        sum_ratings = sum([b.rating for b in beer_list])
        average = round(sum_ratings / float(len(beer_list)), 2)
        abvs[abv]["average"] = average

    sort = request.args.get("sort")
    reverse = True
    if sort not in ["name", "count", "average"]:
        sort = "sort_name"  # numberic version without percentage sign
        reverse = False
    abv_list = sorted(
        [item[1] for item in abvs.items()], key=lambda x: x[sort], reverse=reverse
    )
    return render_template("analysis/list.html", list=abv_list, type="abv", t="ABVs")


@mod_analysis.route("/abv/<abv>", methods=["GET"])
def show_abv(abv):
    abv = abv.replace("% abv", "")
    # Use the actual sqlalchemy query and_(whatever).
    beers = sorted(
        [beer for beer in Beers.query.all() if round(beer.abv) == float(abv)],
        key=lambda x: x.rating,
        reverse=True,
    )
    favorite_beer = beers[0]
    ratings = [beer.rating for beer in beers]
    average_rating = round(sum(ratings) / float(len(ratings)), 2)
    abvs = [beer.abv for beer in beers]
    average_abv = round(sum(abvs) / float(len(abvs)), 2)

    breweries = {}
    for beer in beers:
        if beer.brewery not in breweries:
            breweries[beer.brewery] = (beer.rating, 1)
        else:
            _curr = breweries[beer.brewery]
            breweries[beer.brewery] = (_curr[0] + beer.rating, int(_curr[1]) + 1)

    most_common_brewery = ""
    most_common_count = 0
    for brewery in breweries:
        _data = breweries[brewery]
        rating = _data[0] / float(_data[1])
        if _data[1] > most_common_count:
            most_common_brewery = brewery
            most_common_count = _data[1]

    return render_template(
        "analysis/analysis.html",
        abv=abv,
        beers=beers,
        favorite_beer=favorite_beer,
        most_common_brewery=most_common_brewery,
        most_common_count=most_common_count,
        average_rating=average_rating,
        average_abv=average_abv,
        t="ABV: " + abv,
    )


@mod_analysis.route("/style/<style>", methods=["GET"])
def show_style(style):
    beers = get_beers_by_style(style, order_by="rating")
    favorite_beer = beers[0]
    ratings = [beer.rating for beer in beers]
    average_rating = round(sum(ratings) / float(len(ratings)), 2)
    abvs = [beer.abv for beer in beers]
    average_abv = round(sum(abvs) / float(len(abvs)), 2)

    breweries = {}
    for beer in beers:
        if beer.brewery not in breweries:
            breweries[beer.brewery] = (beer.rating, 1)
        else:
            _curr = breweries[beer.brewery]
            breweries[beer.brewery] = (_curr[0] + beer.rating, int(_curr[1]) + 1)

    most_common_brewery = ""
    most_common_count = 0
    for brewery in breweries:
        _data = breweries[brewery]
        rating = _data[0] / float(_data[1])
        if _data[1] > most_common_count:
            most_common_brewery = brewery
            most_common_count = _data[1]

    return render_template(
        "analysis/style.html",
        style=style,
        beers=beers,
        favorite_beer=favorite_beer,
        most_common_brewery=most_common_brewery,
        most_common_count=most_common_count,
        average_rating=average_rating,
        average_abv=average_abv,
        t="Style: " + style,
    )


@mod_analysis.route("/year/<int:year>", methods=["GET"])
def show_year(year):
    beers = get_beers_by_year(year)
    count = len(beers)

    #########
    # TL;DR #
    #########

    avg_abv = round(sum([beer.abv for beer in beers]) / float(count), 2)
    avg_rating = round(sum([beer.rating for beer in beers]) / float(count), 2)
    top_three = sorted(beers, key=lambda x: x.rating, reverse=True)[:3]
    bottom_three = sorted(beers, key=lambda x: x.rating)[:3]

    tldr_data = {
        "avg_abv": avg_abv,
        "avg_rating": avg_rating,
        "top_three": top_three,
        "bottom_three": bottom_three,
    }

    ##########
    # MONTHS #
    ##########

    # Not all months are necessarily filled
    month_totals = [0] * 12
    month_ratings = [0] * 12
    month_abvs = [0] * 12
    for key, group in groupby(beers, key=lambda x: x.drink_datetime):
        month_idx = key.month - 1
        month_beers = [g for g in group]
        month_totals[month_idx] = len(month_beers)
        month_ratings[month_idx] = calc_avg(month_beers, "rating")
        month_abvs[month_idx] = calc_avg(month_beers, "abv")

    month_data = {
        "average": round(sum(month_totals) / float(len(month_totals)), 2),
        "most": (month(month_totals.index(max(month_totals))), max(month_totals)),
        "least": (month(month_totals.index(min(month_totals))), min(month_totals)),
        "best": (month(month_ratings.index(max(month_ratings))), max(month_ratings)),
        "worst": (month(month_ratings.index(min(month_ratings))), min(month_ratings)),
        "booziest": (month(month_abvs.index(max(month_abvs))), max(month_abvs)),
        "soberest": (month(month_abvs.index(min(month_abvs))), min(month_abvs)),
    }

    ##########
    # PLACES #
    ##########

    city_data = calculate_data(beers, "drink_city")
    country_data = calculate_data(beers, "drink_country")
    brewery_country_data = calculate_data(beers, "country")

    ##########
    # STYLES #
    ##########

    style_data = calculate_data(beers, "style")

    ########
    # ABVS #
    ########

    abv_top_three = sorted(beers, key=lambda x: x.abv, reverse=True)[:3]
    abv_bottom_three = sorted(beers, key=lambda x: x.abv)[:3]
    abv_data = {"top": abv_top_three, "bottom": abv_bottom_three}

    #############
    # BREWERIES #
    #############
    if year == 2011:
        brewery_data = calculate_data(beers, "brewery", override=True)
    else:
        brewery_data = calculate_data(beers, "brewery", override=False)

    return render_template(
        "analysis/year.html",
        year=year,
        beers=beers,
        tldr_data=tldr_data,
        month_data=month_data,
        city_data=city_data,
        country_data=country_data,
        brewery_country_data=brewery_country_data,
        style_data=style_data,
        abv_data=abv_data,
        brewery_data=brewery_data,
        t="Year: " + str(year),
    )


@mod_analysis.route("/rating/<rating>", methods=["GET"])
def show_rating(rating):
    # Use the actual sqlalchemy query and_(whatever).
    beers = get_beers_by_rating(rating)
    favorite_beer = beers[0]
    average_rating = rating
    abvs = [beer.abv for beer in beers]
    average_abv = round(sum(abvs) / float(len(abvs)), 2)

    breweries = {}
    for beer in beers:
        if beer.brewery not in breweries:
            breweries[beer.brewery] = (beer.rating, 1)
        else:
            _curr = breweries[beer.brewery]
            breweries[beer.brewery] = (_curr[0] + beer.rating, int(_curr[1]) + 1)

    most_common_brewery = ""
    most_common_count = 0
    for brewery in breweries:
        _data = breweries[brewery]
        rating = _data[0] / float(_data[1])
        if _data[1] > most_common_count:
            most_common_brewery = brewery
            most_common_count = _data[1]

    return render_template(
        "analysis/analysis.html",
        beers=beers,
        favorite_beer=favorite_beer,
        most_common_brewery=most_common_brewery,
        most_common_count=most_common_count,
        average_rating=average_rating,
        average_abv=average_abv,
        t="Rating: " + str(rating),
    )


@mod_analysis.route("/<attribute>/<value>", methods=["GET"])
def show_generic(attribute, value):
    beers = get_beers_by_attribute(attribute, value, order_by="rating")
    favorite_beer = beers[0]
    ratings = [beer.rating for beer in beers]
    average_rating = round(sum(ratings) / float(len(ratings)), 2)
    abvs = [beer.abv for beer in beers]
    average_abv = round(sum(abvs) / float(len(abvs)), 2)
    title = title_map[attribute]

    breweries = {}
    for beer in beers:
        if beer.brewery not in breweries:
            breweries[beer.brewery] = (beer.rating, 1)
        else:
            _curr = breweries[beer.brewery]
            breweries[beer.brewery] = (_curr[0] + beer.rating, int(_curr[1]) + 1)

    styles = {}
    for beer in beers:
        if beer.style not in styles:
            styles[beer.style] = (beer.rating, 1)
        else:
            _curr = styles[beer.style]
            styles[beer.style] = (_curr[0] + beer.rating, int(_curr[1]) + 1)

    most_common_brewery = ""
    most_common_count = 0
    for brewery in breweries:
        _data = breweries[brewery]
        rating = _data[0] / float(_data[1])
        if _data[1] > most_common_count:
            most_common_brewery = brewery
            most_common_count = _data[1]

    most_common_style = ""
    most_common_style_count = 0
    for style in styles:
        _data = styles[style]
        rating = _data[0] / float(_data[1])
        if _data[1] > most_common_style_count:
            most_common_style = style
            most_common_style_count = _data[1]

    return render_template(
        "analysis/generic.html",
        attribute=attribute,
        beers=beers,
        favorite_beer=favorite_beer,
        most_common_brewery=most_common_brewery,
        most_common_count=most_common_count,
        most_common_style=most_common_style,
        most_common_style_count=most_common_style_count,
        average_rating=average_rating,
        average_abv=average_abv,
        t="{0}: {1}".format(title, value),
    )


###########
# HELPERS #
###########


def calc_avg(beers, attr):
    count = len(beers)
    return round(sum([getattr(beer, attr) for beer in beers]) / float(count), 2)


def month(idx):
    return calendar.month_name[idx + 1]


def calculate_data(beers, attribute, override=False):
    keys = []
    totals = []
    ratings = []
    abvs = []
    count = 0
    beers.sort(key=lambda x: getattr(x, attribute))
    for key, group in groupby(beers, key=lambda x: getattr(x, attribute)):
        beers = [g for g in group]
        count += 1
        if len(beers) < 5 and not override:
            continue
        keys.append(key)
        totals.append(len(beers))
        ratings.append(calc_avg(beers, "rating"))
        abvs.append(calc_avg(beers, "abv"))

    if not totals:
        return {
            "count": count,
            "most": (None, 0),
            "least": (None, 0),
            "best": (None, 0),
            "worst": (None, 0),
            "booziest": (None, 0),
            "soberest": (None, 0),
        }
    return {
        "count": count,
        "most": (keys[totals.index(max(totals))], max(totals)),
        "least": (keys[totals.index(min(totals))], min(totals)),
        "best": (keys[ratings.index(max(ratings))], max(ratings)),
        "worst": (keys[ratings.index(min(ratings))], min(ratings)),
        "booziest": (keys[abvs.index(max(abvs))], max(abvs)),
        "soberest": (keys[abvs.index(min(abvs))], min(abvs)),
    }
