from fyyur import app,db,format_datetime
from flask import render_template,request,flash,redirect,url_for
from fyyur.models import *
from fyyur.forms import *
from PIL import Image
import os
import secrets
from datetime import datetime


# ------------------------------------------------------------------------
# helpers:
# ------------------------------------------------------------------------

# function to save img in the 'static/img/
# hash the file name, 
# and reduce the size
def save_picture(form_picture,artist_or_venue):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img/',artist_or_venue ,picture_fn)
    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
  return render_template('pages/home.html')



@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500
