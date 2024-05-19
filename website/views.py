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
    loc = Nominatim(user_agent="website")
    locations_to_show = []
    recycling_points = RecyclingPoint.query.all()
    locations = []
    for point in recycling_points:
        getLoc = loc.geocode(point.location)
        mylocation = [getLoc.latitude, getLoc.longitude]
        locations.append(mylocation)
    
    locations_to_show = locations
    
    # default thing
    mydistances = {}
    mydistances[recycling_points[0]] = 42
    

    if request.method == 'POST':
        city = request.form.get("city")
        mylocation_input = request.form.get("mylocation")
        material = request.form.get("material")
        
        if city == 'Усі міста':
            locations_to_show = locations
        else:
            locs = []
            for point in recycling_points:
                if point.city == city:
                    getLoc = loc.geocode(point.location)
                    mylocation = [getLoc.latitude, getLoc.longitude]
                    locs.append(mylocation)
            locations_to_show = locs


        if mylocation_input != '':
            getLoc = loc.geocode(mylocation_input)
            mylocation = [getLoc.latitude, getLoc.longitude]
            # find nearest
            mydistances = mydistances.clear()
            for point in recycling_points:
                getLoc = loc.geocode(point.location)
                point_location = [getLoc.latitude, getLoc.longitude]
                mydistances[point] = geodesic(mylocation, point_location).km

        if material != '':
            # TO DO
            pass


    return render_template("home.html", user = current_user, recycling_points=recycling_points, locations=locations_to_show, distances = mydistances)


@views.route('/newpoint', methods = ['POST'])
def new_point():
    # add new point
    flash('Added successfully!', category='success')
    return redirect(url_for('views.home'))