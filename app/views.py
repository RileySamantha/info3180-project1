"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash,jsonify
from flask_login import login_user, logout_user, current_user, login_required
from forms import Userprofile, LoginForm
from models import UserProfile

import time
import json
import randint

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
    return render_template('about.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = Userprofile.query.filter_by(username=username, password=password)\
        .first()
        
        if user is not None:
            login_user(user)

            flash('Logged in successfully.', 'success')
            next = request.args.get('next')
            return redirect(url_for('secure_page'))
        else:
            flash('Username or Password is incorrect.', 'danger')

    flash_errors(form)
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home'))
    
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))
    

###
# The functions below should be applicable to all Flask apps.
###


# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

#create profile
@app.route("/profile", methods=["GET", "POST"])
@login_required
def crtprof():
    form = Userprofile()
    if request.method == "POST" and form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        username = form.username.data
        gender = form.gender.data
        age = form.age.data
        biography = form.biography.data
        image=request.files['image']
        
        id= randint(00000000, 12345678)
        
        user = UserProfile(firstname, lastname, username, age, gender, biography, image)
        db.session.add(user)
        db.session.commit()
        

        flash('Created profile successfully.', 'success')
        return redirect(url_for('view_profile'))
    else:
            flash('Profile not created', 'danger')

    flash_errors(form)
    return render_template('profile.html', form =form)


# list profiles           
@app.route("/profiles", method=['GET', 'POST'])
@login_required
def profilelst():
    """Render a list of all profiles"""
    profiles = db.session.query(UserProfile).all()
    if request.method == "POST":
        plist = []
        for profile in profiles:
            plist.append({'id':profile.id, 'username':profile.user})
            return jsonify(profiles=plist)
    else:
        return render_template('profiles.html', profiles=profiles, tdate = timeinfo())
    
def timeinfo():
    #now = time.strftime("%c")
    return time.strftime(" %d %b %Y")


#view a profile
@app.route('/profile/<userid>', methods=['GET', 'POST'])
@login_required
def profileView(userid):
    view = db.session.query(UserProfile).filter_by(userid=userid)
    #if not user:
    #   flash('User not found', 'danger')
    #else
    if request.method == 'POST':
        return jsonify(
            'userid'= view.userid, 
            'username'= view.username, 
            'age'= view.age, 
            'gender'= view.gender, 
            'profile_add_on'= view.profile_add_on,
            'image'= view.image
            )
    return render_template('profileview.html', view=view)
    #return redirect(url_for())

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
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
