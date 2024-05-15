from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import RecyclingPoint
from geopy.geocoders import Nominatim


views = Blueprint('views', __name__)

@views.route('/',  methods = ['GET'])
@login_required
def home():
    recycling_points = RecyclingPoint.query.all()
    locations = []
    for point in recycling_points:
        locations.append([eval(i) for i in point.location.split(',')])



    if request.method == 'GET':
        if request.form.get("mylocation") != None:
            mylocation_input = request.form.get('mylocation')
            loc = Nominatim(user_agent="Geopy Library")
            getLoc = loc.geocode(mylocation_input)
            mylocation = [getLoc.latitude, getLoc.longitude]
            # find nearest locs to this



    locations_to_show = locations # for now

    return render_template("home.html", user = current_user, locations=locations_to_show)

