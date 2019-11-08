from fyyur import db
from datetime import datetime
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(120), default='default.jpeg')
    facebook_link = db.Column(db.String(120),nullable=True)
    genres = db.Column(db.ARRAY(db.String))
    website = db.Column(db.String(120),nullable=True)
    seeking_talent=db.Column(db.Boolean(),default=False)
    seeking_description=db.Column(db.String(500),nullable=True)


    def __repr__(self):
        return f'<Venue {self.name}>'


    def seperate_genres(self):
        genres= "".join(self.genres[1:-1]).split(",")
        return [genre if genre[0]!='"' else genre[1:-1] for genre in genres]
        
   

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(120), default='default.jpeg')
    facebook_link = db.Column(db.String(120),nullable=True)
    website=db.Column(db.String(120),nullable=True)
    seeking_venue=db.Column(db.Boolean(),default=False)
    seeking_description=db.Column(db.String(500),nullable=True)
    


    def __repr__(self):
        return f'<Artist {self.name}>'


    def seperate_genres(self):
        genres= "".join(self.genres[1:-1]).split(",")
        return [genre if genre[0]!='"' else genre[1:-1] for genre in genres]
       

# i did it in association object and not association table because i want to add start time field 
# like it write here : https://stackoverflow.com/questions/7417906/sqlalchemy-manytomany-secondary-table-with-additional-fields

class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime())
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
    artist = db.relationship('Artist', backref=db.backref('shows', cascade="all,delete"))
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
    venue = db.relationship('Venue', backref=db.backref('shows', cascade="all,delete"))
