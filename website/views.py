from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import RecyclingPoint, Info, Entry, Material, User
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


@views.route('/newentry', methods = ['POST'])
def new_entry():
    if request.method == 'POST':
        # adding new entry
        user = User.query.filter_by(id=current_user.id).first()
        material = request.form.get('material')
        get_material = Material.query.filter_by(name = material).first()
        pointaddress = request.form.get('pointaddress')
        get_point = RecyclingPoint.query.filter_by(location = pointaddress).first()
        # points earned 
        my_points_earned = 0
        if get_material.id  == 1 or get_material.id  == 2:
            my_points_earned = 20
        elif get_material.id  == 3 or get_material.id  == 4:
            my_points_earned = 40
        elif get_material.id  == 5 or get_material.id  == 6:
            my_points_earned = 60
        else:
            my_points_earned = 100
        # reward
        reward = ""
        sum_of_points = my_points_earned
        for entry in user.entries:
            if entry.material_id == get_material.id:
                sum_of_points = sum_of_points + entry.points_earned
        
        if sum_of_points > 50:
            reward = "Мідь ( тип: " + get_material.name + " )"
        elif sum_of_points > 100:
            reward = "Срібло ( тип: " + get_material.name + " )"
        elif sum_of_points > 150:
            reward = "Золото ( тип: " + get_material.name + " )"

        new_entry = Entry(user_id = user.id, material_id = get_material.id, recycling_point_id = get_point.id, points_earned = my_points_earned, reward = reward)
        db.session.add(new_entry)
        db.session.commit()
        flash('Added successfully!', category='success')
        message_p = 'Points earned: ' + str(my_points_earned)
        flash(message_p, category='success')
        if reward != "":
            message_r = 'Reward: ' + str(reward)
            flash (message_r, category='success')
    return redirect(url_for('views.home'))