from flask import render_template,request,flash,redirect,url_for
from fyyur import app,db,format_datetime
from fyyur.forms import *
from fyyur.models import *
from fyyur.routes.general_routes import *
import os


# show Shows
#------------------------------------------------------------------------------
@app.route('/shows')
def shows():
    shows = Show.query.order_by(Show.start_time.desc()).all()
    for show in shows:
        venue = Venue.query.get_or_404(show.venue_id)
        artist = Artist.query.get_or_404(show.artist_id)
        show.artist_image_link= artist.image_link
        show.venue_name= venue.name
        show.artist_name= artist.name
    return render_template('pages/shows.html', shows=shows)


# create show
#-----------------------------------------------------------------


@app.route('/shows/create', methods=['GET','POST'])
def create_shows():
    form = ShowForm()
    if form.validate_on_submit():
        try:
            new_show = Show(
                artist_id=form.artist_id.data,
                venue_id=form.venue_id.data,
                start_time=form.start_time.data
            )
            db.session.add(new_show)
            db.session.commit()
            flash('Show was successfully listed!')         
            return redirect(url_for('shows'))
        except :  
            flash('An error occurred. Show could not be listed.')  
    # print(form.errors)      
    return render_template('forms/new_show.html', form=form)


