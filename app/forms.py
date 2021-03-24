
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed, FileField, FileRequired

class PropertyForm(FlaskForm):
    title = StringField("Title Property", validators = [DataRequired()])
    number_of_bedrooms = StringField("Number of Bedroom", validators = [DataRequired()])
    number_of_bathrooms = StringField("Number of Bathrooms", validators = [DataRequired()])
    location = StringField("Location of Property", validators = [DataRequired()])
    price = StringField("Price of Property", validators = [DataRequired()])
    typeHA = SelectField("House or Apartment", choices = [("House", "House"), ("Apartment","Apartment")])
    description = TextAreaField("Description of Property", validators = [DataRequired()])
    photo = FileField("Photo of Property", validators = [FileRequired(),
                                                        FileAllowed(["jpg","png","jpeg"], "Images Only!")])
                                                        