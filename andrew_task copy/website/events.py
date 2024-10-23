from flask import Blueprint, render_template, redirect, url_for
from .models import Event, Comment, Booking
from .forms import EventForm, CommentForm, BookingForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

destbp = Blueprint('event', __name__, url_prefix = '/events')

@destbp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    # create the comment form
    cform = CommentForm() 
    return render_template('events/show.html', event = event, form=cform)

@destbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  form = EventForm()
  if form.validate_on_submit():
        event_time = form.time.data.strftime('%H:%M')  # Convert time object to string
        event_etime = form.etime.data.strftime('%H:%M')  # Convert end time object to string
        db_file_path = check_upload_file(form)
        event = Event(name=form.name.data,
        description=form.description.data,
        category=form.category.data,
        image=db_file_path,
        date=form.date.data,  # This can remain as a date object
        time=event_time,      # Store time as a string (HH:MM)
        etime=event_etime,
        location=form.location.data,
        status=form.status.data,
        quantity=form.quantity.data,
        user_id=current_user.id
        )
        # add the object to the db session
        db.session.add(event)
        # commit to the database
        db.session.commit()
        print('Successfully created new event', 'success')
        return redirect(url_for('event.create'))
  return render_template('events/create.html', form=form)

def check_upload_file(form):
      # get file data from form  
  fp = form.image.data
  filename = fp.filename
  # get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  # upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH,'static/image',secure_filename(filename))
  # store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/image/' + secure_filename(filename)
  # save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path

@destbp.route('/<id>/comment', methods = ['GET', 'POST'])
@login_required
def comment(id):
  # here the form is created  form = CommentForm()
  form = CommentForm()
  if form.validate_on_submit():	#this is true only in case of POST method
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    comment = Comment(text=form.text.data, event=event, user=current_user)
    db.session.add(comment) 
    db.session.commit()
    print(f"The following comment has been posted: {form.text.data}")
  # notice the signature of url_for
  return redirect(url_for('event.show', id=id))

@destbp.route('/booking', methods=['GET', 'POST'])
def book():
    form = BookingForm()
    if form.validate_on_submit():
        # Create a new Booking instance
        new_booking = Booking(
            name=form.name.data,
            phone=form.phone.data,
            billing_address=form.billing_address.data,
            payment_method=form.payment_method.data,
            card_number=form.card_number.data,
            expiry_date=form.expiry_date.data,
            cvv=form.cvv.data
        )
        # Add the booking to the database
        db.session.add(new_booking)
        db.session.commit()
        
        print('Payment successful!', 'success')
        return redirect(url_for('success'))  # Redirect to a success page
    # Help Lou
    return render_template('events/booking.html', form=form) 

