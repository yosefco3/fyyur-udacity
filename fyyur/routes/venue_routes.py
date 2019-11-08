from flask import render_template,request,flash,redirect,url_for
from fyyur import app,db,format_datetime
from fyyur.forms import *
from fyyur.models import *
from fyyur.routes.general_routes import *
import os



#  Venues
#  ----------------------------------------------------------------


# show venues by the city and state
# --------------------------------------------------------------------------------

@app.route('/venues')
def venues():
    data=Venue.query.all()
    cities=sorted(list(set([(v.city,v.state) for v in data])),key=lambda x:x[1])
    areas=[{'city':city,'state':state,'venues':[]} for (city,state) in cities]
    for v in data:
        for area in areas:
            if v.city==area['city'] and v.state==area['state']:
                area['venues'].append({'name':v.name,'id':v.id})
    # the areas list has build in that stracture : 
    #
    # areas = [{
    #     city
    #     state 
    #     venues:{id:"",
    #             name:""}
    # },{
    #  ....
    # }]
    return render_template('pages/venues.html', areas=areas)


# search venues
# ------------------------------------------------------------------------

@app.route('/venues/search', methods=['POST'])
def search_venues(): 
    search = request.form.get('search_term', '')
    venues = Venue.query.filter(Venue.name.ilike("%" + search + "%")).all()
    response = {
        "count": len(venues),
        "data": [
            venue for venue in venues
        ]
    }
    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))

# show venue
# --------------------------------------------------------------------------------

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    venue.genres=venue.seperate_genres()

    # query venue past shows , add them as property
    venue.past_shows= db.session.query(Show).filter(
        Show.start_time < datetime.now(),
        Show.venue_id == venue_id).all()
    venue.past_shows_count=len(venue.past_shows)

    # query venue coming shows , add them as property
    venue.upcoming_shows=db.session.query(Show).filter(
        Show.start_time > datetime.now(),
        Show.venue_id == venue_id).all()
    venue.upcoming_shows_count=len(venue.upcoming_shows)

    # add to every show in the venue past/upcoming shows 
    # venue_image and venue name

    for show in venue.past_shows + venue.upcoming_shows :
        a=Artist.query.get_or_404(show.artist_id)
        show.artist_image_link=a.image_link
        show.artist_name=a.name

    return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET','POST'])
def create_venue_form():
    form = VenueForm()
    if request.method=='POST':
        try:
            new_venue = Venue(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                address=form.address.data,
                phone=form.phone.data,
                genres=form.genres.data,
                facebook_link=form.facebook_link.data,
                image_link=form.image_link.data,
                website=form.website.data,
                seeking_description=form.seeking_description.data
            )
            if new_venue.seeking_description:
                new_venue.seeking_talent=True

            if new_venue.image_link:
                new_venue.image_link = save_picture(form.image_link.data,"venues")
                
            db.session.add(new_venue)
            db.session.commit()
            flash('Venue ' + request.form['name'] + ' was successfully listed!')
            return redirect(url_for('index'))
        except ValueError:
            flash('Error occurred. Venue ' + form.name.data + ' could not be listed.')
    return render_template('forms/new_venue.html', form=form)

# delete venue
# ------------------------------------------------------------------

@app.route('/venues/<int:venue_id>/delete', methods=['POST'])
def delete_venue(venue_id):
    try:
        venue = Venue.query.get_or_404(venue_id)
        # to remove the image file if it different from the default :
        if venue.image_link and venue.image_link!='default.jpeg':
            os.remove(os.path.join("fyyur/static/img/venues/",venue.image_link))
        db.session.delete(venue)
        db.session.commit()
        flash('The venue has been removed together with all of its shows.')
        return redirect(url_for('index'))
    except ValueError:
        flash('It was not possible to delete this Venue')
    return None




# Update Venue
# --------------------------------------------------------------------------


@app.route('/venues/<int:venue_id>/edit', methods=['GET','POST'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get_or_404(venue_id)
    if request.method=='POST':
        if form.validate_on_submit():
            try:
                venue.name = form.name.data
                venue.genres = form.genres.data
                venue.address = form.address.data
                venue.city = form.city.data
                venue.phone = form.phone.data
                venue.state = form.state.data
                venue.facebook_link = form.facebook_link.data
                venue.website = form.website.data

                if form.seeking_description.data:
                    venue.seeking_description = form.seeking_description.data
                venue.seeking_talent=False if venue.seeking_description=="" else True

                if form.image_link.data :
                    if venue.image_link!="default.jpeg":
                        os.remove(os.path.join("static/img/venues/",venue.image_link))
                    venue.image_link = form.image_link.data
                # if the type is str it's mean that in that form 
                # there wasn't link.
                if venue.image_link and type(venue.image_link)!=str:
                    venue.image_link = save_picture(venue.image_link,"venues")
                db.session.commit()
                flash('Venue ' + form.name.data + ' was successfully edited!')
                return redirect(url_for('show_venue', venue_id=venue_id)) 

            except ValueError:  
                flash(
                    'An error occurred. Venue ' + form.name + ' could not be listed.')
    # print(form.errors)
    return render_template('forms/edit_venue.html', form=form, venue=venue)