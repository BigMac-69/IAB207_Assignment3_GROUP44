from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from . import db

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    events = db.session.scalars(db.select(Event)).all()
    return render_template('index.html', events = events)

@mainbp.route('/search')
def search():
    if request.args['search'] and request.args['search'] != "":
        print(request.args['search'])
        query = "%" + request.args['search'] + "%"
        events = db.session.scalars(db.select(Event).where(Event.description.like(query)))
        return render_template('index.html', events=events, hide_about=True)
    else:
        return redirect(url_for('main.index'), hide_about=False)
    
@mainbp.route('/category/<category>', methods=['GET'])
def filter_by_category(category):
    # Query the database for events in the selected category
    events = Event.query.filter_by(category=category).all()
    
    # Render the same template, but pass in the filtered events
    return render_template('index.html', events=events, hide_about=True)
