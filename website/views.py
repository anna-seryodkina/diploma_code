from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import RecyclingPoint, Info
from geopy.geocoders import Nominatim
from geopy import distance
from geopy.distance import geodesic


views = Blueprint('views', __name__)

@views.route('/',  methods = ['GET', 'POST'])
@login_required
def home():
    infos = Info.query.all()

    loc = Nominatim(user_agent="website")
    locations_to_show = {}
    recycling_points = RecyclingPoint.query.all()
    locations = {}
    for point in recycling_points:
        getLoc = loc.geocode(point.location)
        mylocation = [getLoc.latitude, getLoc.longitude]
        locations[point] = mylocation
    
    locations_to_show = locations
    
    # default thing
    mydistances = {}
    for point in recycling_points:
        mydistances[point] = 'x'

    if request.method == 'POST':
        city = request.form.get("city")
        mylocation_input = request.form.get("mylocation")
        material = request.form.get("material")
        
        if city == 'Усі міста':
            locations_to_show = locations
        else:
            locs = {}
            for point in recycling_points:
                if point.city == city:
                    getLoc = loc.geocode(point.location)
                    mylocation = [getLoc.latitude, getLoc.longitude]
                    locs[point] = mylocation
            locations_to_show = locs


        if mylocation_input != '':
            getLoc = loc.geocode(mylocation_input)
            mylocation = [getLoc.latitude, getLoc.longitude]
            # find nearest
            for point in recycling_points:
                getLoc = loc.geocode(point.location)
                point_location = [getLoc.latitude, getLoc.longitude]
                calculations = geodesic(mylocation, point_location).km
                mydistances[point] = round(calculations, 1)
            mydistances = dict(sorted(mydistances.items(), key=lambda item: item[1]))

        if material != '':
            # TO DO
            pass


    return render_template("home.html", user = current_user, recycling_points=recycling_points, locations=locations_to_show, distances = mydistances, infos = infos)


@views.route('/newpoint', methods = ['POST'])
def new_point():
    # TO DO: add new point
    flash('Added successfully!', category='success')
    return redirect(url_for('views.home'))


@views.route('/addinfo', methods = ['POST'])
def new_info():
    if request.method == 'POST':
        title = request.form.get('title')
        information = request.form.get('info')
        newinfo = Info(title = title, information = information)
        db.session.add(newinfo)
        db.session.commit()
        flash('Added successfully!', category='success')
    return redirect(url_for('views.home'))