from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import RecyclingPoint
from geopy.geocoders import Nominatim
from geopy import distance
from geopy.distance import geodesic


views = Blueprint('views', __name__)

@views.route('/',  methods = ['GET', 'POST'])
@login_required
def home():
    locations_to_show = []
    recycling_points = RecyclingPoint.query.all()
    locations = []
    for point in recycling_points:
        locations.append([eval(i) for i in point.location.split(',')])
    
    locations_to_show = locations
    
    # default thing
    mydistances = {}
    mydistances[recycling_points[0]] = 42
    
    if request.method == 'POST':
        city = request.form.get("city")
        mylocation_input = request.form.get("mylocation")
        
        if city == 'Усі міста':
            locations_to_show = locations
        else:
            locs = []
            for point in recycling_points:
                if point.city == city:
                    locs.append([eval(i) for i in point.location.split(',')])
            locations_to_show = locs


        if mylocation_input != '':
            loc = Nominatim(user_agent="website")
            getLoc = loc.geocode(mylocation_input)
            mylocation = [getLoc.latitude, getLoc.longitude]
            # find nearest
            mydistances = {}
            for point in recycling_points:
                mydistances[point] = geodesic(mylocation, point.location).km

    return render_template("home.html", user = current_user, recycling_points=recycling_points, locations=locations_to_show, distances = mydistances)

