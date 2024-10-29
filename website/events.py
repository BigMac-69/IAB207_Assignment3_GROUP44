from flask import Blueprint, render_template, redirect, url_for
from .models import Event, Comment, Booking
from .forms import EventForm, CommentForm, BookingForm, UpdateEventForm, CancelEventForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from datetime import datetime  # Import to handle time conversion

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
        price=form.price.data,
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

@destbp.route('/<id>/update', methods=['GET', 'POST'])
@login_required
def update_event(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))

    # Check if the current user is the owner of the event (added functionality)
    if event.creator != current_user:
        print('You do not have permission to update this event.', 'danger')
        return redirect(url_for('event.show', id=id))

    form = UpdateEventForm()

    if form.validate_on_submit():
        # Update event details (added functionality)
        event.name = form.name.data
        event.description = form.description.data
        event.category = form.category.data
        event.date = form.date.data
        event.time = form.time.data.strftime('%H:%M')  # Convert time object to string
        event.etime = form.etime.data.strftime('%H:%M')  # Convert end time object to string
        event.location = form.location.data
        event.price = form.price.data
        event.quantity = form.quantity.data

        # If a new image is uploaded, update the event poster (added functionality)
        if form.image.data:
            db_file_path = check_upload_file(form)
            event.image = db_file_path

        db.session.commit()
        print('Event updated successfully!', 'success')
        return redirect(url_for('event.show', id=event.id))

    # Pre-populate the form with current event details (added functionality)
    form.name.data = event.name
    form.description.data = event.description
    form.category.data = event.category
    form.date.data = event.date

    # Convert the string time values to datetime objects before assigning to the form
    form.time.data = datetime.strptime(event.time, '%H:%M')  # Convert string to datetime
    form.etime.data = datetime.strptime(event.etime, '%H:%M')  # Convert string to datetime

    form.location.data = event.location
    form.price.data = event.price
    form.quantity.data = event.quantity

    return render_template('events/update.html', form=form, event=event)

# New route for canceling an event (added functionality)
@destbp.route('/<id>/cancel', methods=['POST'])
@login_required
def cancel_event(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))

    # Check if the current user is the owner of the event (added functionality)
    if event.creator != current_user:
        print('You do not have permission to cancel this event.', 'danger')
        return redirect(url_for('event.show', id=id))

    form = CancelEventForm()
    if form.validate_on_submit():
        # Mark the event as canceled (added functionality)
        event.status = 'canceled'  # Update status to 'canceled' (lowercase)
        db.session.commit()
        print('Event canceled successfully!', 'success')
        return redirect(url_for('event.show', id=event.id))

    return render_template('events/show.html', event=event, form=form)



@destbp.route('/events/<int:event_id>/book', methods=['GET', 'POST'])
@login_required
def book(event_id):
    event = Event.query.get_or_404(event_id)
    form = BookingForm()

    # Set total_cost to 0 initially
    total_cost = 0

    if form.validate_on_submit():
        # Calculate total cost if "Calculate Total" button is clicked
        if form.calculate_total.data:
            # Calculate total cost based on number_of_tickets
            total_cost = int(event.price) * int(form.number_of_tickets.data)
            print(f"Calculated Total Cost: {total_cost}")  # Debugging output

        # Proceed with booking if "Book Now" button is clicked
        elif form.submit.data:
            try:
                # Check if the user already booked this event
                existing_booking = Booking.query.filter_by(event_id=event_id, user_id=current_user.id).first()
                if existing_booking:
                    print("You have already booked this event.", "warning")
                else:
                    # Calculate the total cost for booking
                    total_cost = event.price * form.number_of_tickets.data
                    print(f"Booking Total Cost: {total_cost}")  # Debugging output

                    # Create and save a new booking
                    new_booking = Booking(
                        event_id=event_id,
                        user_id=current_user.id,
                        boname=form.boname.data,
                        boemail=form.boemail.data,
                        phone=form.phone.data,
                        billing_address=form.billing_address.data,
                        payment_method=form.payment_method.data,
                        card_number=form.card_number.data,
                        expiry_date=form.expiry_date.data,
                        cvv=form.cvv.data,
                        number_of_tickets=form.number_of_tickets.data
                    )
                    db.session.add(new_booking)
                    db.session.commit()
                    print("Booking successfully saved!", "success")
                    return redirect(url_for('event.history'))
            except Exception as e:
                db.session.rollback()
                print(f"Error booking event: {str(e)}", "danger")
                return redirect(url_for('event.book', event_id=event_id))

    # Render the booking page with total cost
    return render_template('events/booking.html', form=form, event=event, total_cost=total_cost)

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
