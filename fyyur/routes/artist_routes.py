from flask import render_template,request,flash,redirect,url_for
from fyyur import app,db,format_datetime
from fyyur.forms import *
from fyyur.models import *
from fyyur.routes.general_routes import *
import os



#  Artists
#  ----------------------------------------------------------------

# show artists
# -------------------------------------------------------------------

@app.route('/artists')
def artists():
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)



#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET','POST'])
def create_artist_form():
    form = ArtistForm()
    if request.method=='POST':
        try:
            new_artist = Artist(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                phone=form.phone.data,
                genres=form.genres.data,
                facebook_link=form.facebook_link.data,
                image_link=form.image_link.data,
                website=form.website.data,
                seeking_description=form.seeking_description.data
            )
            if new_artist.seeking_description:
                new_artist.seeking_venue=True
            
            if new_artist.image_link:
                new_artist.image_link = save_picture(form.image_link.data,"artists")
            db.session.add(new_artist)
            db.session.commit()
            flash('Artist ' + request.form['name'] + ' was successfully listed!')
            return redirect(url_for('index'))
        except ValueError:
            flash('An error occurred. Artist ' + form.name +' could not be listed.')
    return render_template('forms/new_artist.html', form=form)



# search artist
# --------------------------------------------------------------------------

@app.route('/artists/search', methods=['POST'])
def search_artists():
    search = request.form.get('search_term', '')
    artists = Artist.query.filter(Artist.name.ilike("%" + search + "%")).all()
    response = {
        "count": len(artists),
        "data": [
            artist for artist in artists
        ]
    }
    return render_template(
        'pages/search_artists.html',results=response,search_term=search)


# show artist
# ----------------------------------------------------------------------------

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    artist.genres=artist.seperate_genres()

    # query artist past shows , add them as property
    artist.past_shows= db.session.query(Show).filter(
        Show.start_time < datetime.now(),
        Show.artist_id == artist_id).all()
    artist.past_shows_count=len(artist.past_shows)

    # query artist coming shows , add them as property
    artist.upcoming_shows=db.session.query(Show).filter(
        Show.start_time > datetime.now(),
        Show.artist_id == artist_id).all()
    artist.upcoming_shows_count=len(artist.upcoming_shows)

    # add to every show in the artist past/upcoming shows 
    # venue_image and venue name

    for show in artist.past_shows + artist.upcoming_shows :
        v=Venue.query.get_or_404(show.venue_id)
        show.venue_image_link=v.image_link
        show.venue_name=v.name
    return render_template('pages/show_artist.html', artist=artist)


# delete artist 
# ---------------------------------------------------------------------

@app.route('/artist/<int:artist_id>/delete', methods=['POST'])
def delete_artist(artist_id):
    try:
        artist = Artist.query.get_or_404(artist_id)
        # to remove the image file if it different from the default :
        if artist.image_link and artist.image_link!='default_artist.jpeg':
            os.remove(os.path.join("fyyur/static/img/artists/",artist.image_link))
        db.session.delete(artist)
        db.session.commit()
        flash('The artist has been removed.')
        return redirect(url_for('index'))
    except ValueError:
        flash('It was not possible to delete this Artist')
    return None



#  Update Artist 
#  ----------------------------------------------------------------

@app.route('/artists/<int:artist_id>/edit', methods=['GET','POST'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get_or_404(artist_id)
    if request.method=='POST':
        if form.validate_on_submit():
            try:
                artist.name=form.name.data
                artist.city = form.city.data
                artist.phone = form.phone.data
                artist.state = form.state.data
                artist.genres = form.genres.data
                artist.facebook_link = form.facebook_link.data
                artist.website = form.website.data

                if form.seeking_description.data:
                    artist.seeking_description = form.seeking_description.data
                artist.seeking_venue=False if artist.seeking_description=="" else True

                if form.image_link.data :
                    if artist.image_link!="default.jpeg":
                        os.remove(os.path.join("static/img/artists/",artist.image_link))
                    artist.image_link = form.image_link.data   
                # if the type is str it's mean that in that form 
                # there wasn't link.
                if artist.image_link and type(artist.image_link)!=str:
                    artist.image_link = save_picture(artist.image_link,"artists")
                db.session.commit()

                flash('Artist ' + form.name.data + ' was successfully edited!')
                return redirect(url_for('show_artist', artist_id=artist_id))   
            except ValueError:  
                db.session.rollup()
                return redirect(url_for('show_artist', artist_id=artist_id))
                flash('An error occurred. Artist ' + form.name +' could not be listed.')        
    # print(form.errors)
    return render_template('forms/edit_artist.html', form=form, artist=artist)