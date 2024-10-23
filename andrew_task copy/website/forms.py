from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, StringField, SubmitField, PasswordField, SelectField, DateField, TimeField
from wtforms.validators import InputRequired, Email, EqualTo, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

#User event_create
class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[InputRequired()])
    description = TextAreaField('Event Description', validators=[InputRequired()])
    category = SelectField('Category', choices=[('Cuisine', 'Cuisine'), ('Beverages', 'Beverages'), ('Workshop', 'Workshop'), ('Sourvenir', 'Sourvenir')], validators=[InputRequired()])
    image = FileField('Event Poster', validators=[
        FileRequired(message = 'Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])
    date = DateField('Date', format='%Y-%m-%d', validators=[InputRequired()])
    time = TimeField('Start Time', format='%H:%M', validators=[InputRequired()])
    etime = TimeField('End Time', format='%H:%M', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    status = SelectField('Status', choices=[('Open', 'Open'), ('Inactive', 'Inactive'), ('Cancelled', 'Cancelled'), ('Sold Out', 'Sold Out')], validators=[InputRequired()])
    quantity = StringField('Ticket Quantity', validators=[InputRequired()])
    submit = SubmitField("Create")

class BookingForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=1, max=100, message="Name is required and cannot exceed 100 characters.")])
    phone = StringField('Phone', validators=[InputRequired(), Length(min=10, max=15, message="Phone number must be between 10 to 15 digits.")])
    billing_address = TextAreaField('Billing Address', validators=[InputRequired(), Length(max=250, message="Billing address cannot exceed 250 characters.")])
    payment_method = SelectField('Payment Method', choices=[('visa', 'Visa'),('credit', 'Credit Card')], validators=[InputRequired()])
    card_number = StringField('Card Number', validators=[InputRequired(), Length(min=16, max=16, message="Card number must be exactly 16 digits.")])
    expiry_date = StringField('Expiry Date (MM/YY)', validators=[InputRequired(), Length(min=5, max=5, message="Expiry date must be in the format MM/YY.")])
    cvv = StringField('CVV', validators=[InputRequired(), Length(min=3, max=3, message="CVV must be exactly 3 digits.")])
    submit = SubmitField('Pay Now')


#User login
class LoginForm(FlaskForm):
    user_name = StringField("First Name (It's your username)", validators=[InputRequired('Enter your first (user) name')])
    password = PasswordField("Password", validators=[InputRequired('Enter your password')])
    submit = SubmitField("Login")

#User register
class RegisterForm(FlaskForm):
    user_name = StringField("First Name (It's your username)", validators=[InputRequired()])
    sur_name = StringField("Surname", validators=[InputRequired('Enter sur name')])
    number = StringField("Your Phone Number", validators=[InputRequired('Enter your phone number')])
    address = StringField("Your Address", validators=[InputRequired('Enter your address')])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    
    #linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    #submit button
    submit = SubmitField("Register")

#User comment
class CommentForm(FlaskForm):
    text = TextAreaField('Comment', [InputRequired()])
    submit = SubmitField('Create')