from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from . import db

mainbp = Blueprint('main', __name__)

# Home Page (List Events)
@mainbp.route('/')
def index():
    events = db.session.scalars(db.select(Event)).all()  # Fetch all events
    return render_template('index_home.html', events=events)

# Search for Events
@mainbp.route('/search')
def search():
    if request.args.get('search') and request.args['search'] != "":
        query = "%" + request.args['search'] + "%"
        events = db.session.scalars(db.select(Event).where(Event.name.like(query)))
        return render_template('index_home.html', events=events)
    else:
        return redirect(url_for('main.index'))
