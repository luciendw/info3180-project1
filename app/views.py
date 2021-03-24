"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app , models
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from .forms import PropertyForm
from flask import send_from_directory

from app.models import PropertyInfo
from app import db

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Devante Williams")


@app.route('/property' , methods =['GET' ,'POST'])   
def propertyy():

    form = PropertyForm()

    if request.method == 'POST' and form.validate_on_submit():
        title = form.title.data
        number_of_bedrooms = form.number_of_bedrooms.data
        number_of_bathrooms = form.number_of_bathrooms.data
        location = form.location.data
        price = form.price.data
        typeHA= form.typeHA.data
        description = form.description.data
        photo = form.photo.data

        filename = secure_filename(photo.filename)

        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        property_info = PropertyInfo(title, number_of_bedrooms, number_of_bathrooms, location, price, typeHA, description, filename)
        
        db.session.add(property_info)
        db.session.commit()

        flash("Property was Successfully Added", "success")
        return redirect(url_for('properties'))
    return render_template("propertyform.html", form = form)
    
@app.route('/properties', methods = ['GET'])
def properties():
    properties = PropertyInfo.query.all()
    if request.method == 'GET':
        return render_template('properties.html', properties = properties)

@app.route('/property/<propertyid>', methods = ['GET'])
def propertyid(propertyid):
    proprecord = PropertyInfo.query.filter_by(id = propertyid).first()
    if request.method == 'GET':
        return render_template('propertyid.html', properties = proprecord)

@app.route('/upload/<filename>')
def get_image(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, app.config['UPLOAD_FOLDER']), filename)
###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
