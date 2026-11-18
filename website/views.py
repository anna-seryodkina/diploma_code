from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import RecyclingPoint, Info, Entry, Material, User
from geopy.geocoders import Nominatim
from geopy import distance
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import numpy as np
import json
from datetime import datetime
from datetime import time


views = Blueprint('views', __name__)

@views.route('/',  methods = ['GET', 'POST'])
@login_required
def home():
    

    materials = Material.query.all()
    
    
    infos = Info.query.all()

    loc = Nominatim(user_agent="website")
    locations_to_show = {}
    recycling_points = RecyclingPoint.query.all()
    
    user = User.query.filter_by(id = current_user.id).first()
    
    
    for point in recycling_points:
        m_list = []
        for m in materials:
            if m.recycling_point_id == point.id:
                m_list.append(m.name)
        delimiter = ", "
        point.materials = delimiter.join(m_list)
    
    
    
    locations = {}
    for point in recycling_points:
        getLoc = loc.geocode(point.location, timeout=10)
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
                    getLoc = loc.geocode(point.location, timeout=10)
                    mylocation = [getLoc.latitude, getLoc.longitude]
                    locs[point] = mylocation
            locations_to_show = locs


        if mylocation_input != '':
            getLoc = loc.geocode(point.location, timeout=10)
            mylocation = [getLoc.latitude, getLoc.longitude]
            # find nearest
            for point in recycling_points:
                getLoc = loc.geocode(point.location, timeout=10)
                point_location = [getLoc.latitude, getLoc.longitude]
                calculations = geodesic(mylocation, point_location).km
                mydistances[point] = round(calculations, 1)
            mydistances = dict(sorted(mydistances.items(), key=lambda item: item[1]))

        if material != 'Все':
            if city != 'Усі міста':
                locs = {}
                for m in materials:
                    if m.name == material:
                        for point in recycling_points:
                            if point.id == m.recycling_point_id and point.city == city:
                                getLoc = loc.geocode(point.location, timeout=10)
                                point_location = [getLoc.latitude, getLoc.longitude]
                                locs[point] = point_location
                locations_to_show = locs
            else:
                locs = {}
                for m in materials:
                    if m.name == material:
                        for point in recycling_points:
                            if point.id == m.recycling_point_id:
                                getLoc = loc.geocode(point.location, timeout=10)
                                point_location = [getLoc.latitude, getLoc.longitude]
                                locs[point] = point_location
                locations_to_show = locs

    for e in current_user.entries:
        user.total_points = user.total_points + e.points_earned
    
    
    for m in materials:
        if m.name not in user.stats.keys():
            all_points = 0
            for e in user.entries:
                if e.material_id == m.id:
                    all_points = all_points + e.points_earned
            user.stats[m.name] = all_points


    return render_template("home.html", user = current_user, recycling_points=recycling_points, locations=locations_to_show, distances = mydistances, infos = infos)


@views.route('/newpoint', methods = ['POST', 'GET'])
def new_point():
    if request.method == 'POST':
        address = request.form.get('address')
        city = request.form.get('city')
        works_from = request.form.get('works_from')
        wflist = works_from.split(':')
        wf = time(int(wflist[0]), int(wflist[1]))
        works_to = request.form.get('works_to')
        wtlist = works_to.split(':')
        wt = time(int(wtlist[0]), int(wtlist[1]))
        info = request.form.get('info')
        newpoint = RecyclingPoint(location = address, city = city, works_from=wf, works_to=wt, additional_info=info)
        db.session.add(newpoint)
        db.session.commit()
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


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    info = Info.query.get(noteId)
    if info:
        db.session.delete(info)
        db.session.commit()

    return jsonify({})


@views.route('/delete-point', methods=['POST'])
def delete_point():  
    point = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    pointId = point['pointId']
    point = RecyclingPoint.query.get(pointId)
    if point:
        db.session.delete(point)
        db.session.commit()

    return jsonify({})


@views.route('/editpoint', methods = ['POST', 'GET'])
def editpoint():
    if request.method == 'POST':
        id_data = request.form.get('id')
        address = request.form.get('address')
        city = request.form.get('city')
        works_from = request.form.get('works_from')
        wflist = works_from.split(':')
        wf = time(int(wflist[0]), int(wflist[1]))
        works_to = request.form.get('works_to')
        wtlist = works_to.split(':')
        wt = time(int(wtlist[0]), int(wtlist[1]))
        info = request.form.get('info')
        
        mypoint = RecyclingPoint.query.filter_by(id=id_data).first()
        mypoint.location = address
        mypoint.city = city
        mypoint.works_from = wf
        mypoint.works_to = wt
        mypoint.additional_info = info
        db.session.commit()
        flash('Edited successfully!', category='success')
    return redirect(url_for('views.home'))



@views.route('/editinfo', methods = ['POST', 'GET'])
def editinfo():
    if request.method == 'POST':
        id_data = int(request.form.get('id'))
        title = request.form.get('title')
        information = request.form.get('info')
        
        myinfo = Info.query.filter_by(id = id_data).first()
        myinfo.title = title
        myinfo.information = information
        db.session.commit()
        flash('Edited successfully!', category='success')
    return redirect(url_for('views.home'))