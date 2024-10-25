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


@destbp.route('/events/<int:event_id>/book', methods=['GET', 'POST'])
@login_required
def book(event_id):
    event = Event.query.get_or_404(event_id)
    form = BookingForm()

    if form.validate_on_submit():
        try:
            existing_booking = Booking.query.filter_by(event_id=event_id, user_id=current_user.id).first()
            if existing_booking:
                print("You have already booked this event.", "warning")
            else:
                # Create a new booking
                new_booking = Booking(event_id=event_id, 
                                  user_id=current_user.id, 
                                  boname=form.boname.data,
                                  boemail=form.boemail.data,
                                  phone=form.phone.data,
                                  billing_address=form.billing_address.data,
                                  payment_method=form.payment_method.data,
                                  card_number=form.card_number.data,
                                  expiry_date=form.expiry_date.data,
                                  cvv=form.cvv.data,
                                  cost=form.cost.data,  # Capture the cost
                                  number_of_tickets=form.number_of_tickets.data
                                  )
                db.session.add(new_booking)
                db.session.commit()  # Make sure the commit is successful
                print("You have successfully booked this event!", "success")
                return redirect(url_for('event.history'))
            
        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            print(f"Error booking event: {str(e)}", "danger")
            return redirect(url_for('event.book', event_id=event_id))
    return render_template('events/booking.html', form=form, event=event)

# Updated for Lou from Andrew
@destbp.route('/bookings/history', methods=['GET'])
@login_required
def history():
    # Get all bookings for the logged-in user
    user_id = current_user.id
    booking = Booking.query.filter_by(user_id=current_user.id).all()

    # Check if bookings are retrieved successfully
    if not booking:
        print("You haven't booked any events yet.", "info")

    return render_template('events/history.html', booking=booking)