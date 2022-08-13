#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import sys
from turtle import up
from typing import final
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from forms import *
from sqlalchemy import func
from models import *
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField ,Form, validators
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  data = []
  #get non dublicated area
  every_areas = Venue.query.with_entities(func.count(Venue.id), Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()

  for area in every_areas:
    venues_data = []

    #get list of venues for each distinct area
    area_venues = Venue.query.filter_by(state=area.state, city=area.city).all()
    for venue in area_venues:
      venues_data.append({
        "id": venue.id,
        "name": venue.name,
        #get the number of upcaming show for this venue
        "num_upcomming_shows":len(db.session.query(Show).filter(Show.venue_id==venue.id, Show.start_time>datetime.now()).all())
      })
    #populate the venues list for the current specic area
    data.append({
      "city": area.city,
      "state": area.state,
      "venues": venues_data
    })
  #num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  sterm = request.form.get('search_term','')
  venues = db.session.query(Venue).filter(Venue.name.ilike('%'+sterm+'%')).all()
  print(venues)
  data = []
  count = len(venues)
  for venue in venues:
    num_upcoming_shows=len(db.session.query(Show).filter(Show.venue_id==venue.id, Show.start_time>datetime.now()).all())
    data.append({
      "id": venue.id,
      "name":venue.name,
      "num_upcoming_shows":num_upcoming_shows
    })
  response={
    "count": count,
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data = []
  #get the venue with venue_id id
  venue = db.session.query(Venue).get(venue_id);
  #get past show info
  past_show = db.session.query(Artist, Show, Venue).filter(Artist.id==Show.artist_id, Venue.id==Show.venue_id, Show.venue_id==venue_id,Show.start_time<datetime.now()).all();
  #count of the past shows
  past_shows_count=len(past_show)
  #populate the list of past shows
  past_show_data=[]
  for artist, show, venue in past_show:
    past_show_data.append({
      "artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": str(show.start_time) 
    })


  #get upcoming show info
  upcoming_show = db.session.query(Artist, Show, Venue).filter(Artist.id==Show.artist_id, Venue.id==Show.venue_id, Show.venue_id==venue_id,Show.start_time>datetime.now()).all();
  #count of the upcoming shows
  upcoming_shows_count=len(upcoming_show)
  #populate the list of upcoming shows
  upcoming_show_data=[]
  for artist, show, venue in upcoming_show:
    upcoming_show_data.append({
      "artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": str(show.start_time) 
    })

  #prepare the data
  data={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_show_data,
    "upcoming_shows": upcoming_show_data,
    "past_shows_count": past_shows_count,
    "upcoming_shows_count": upcoming_shows_count,
  }

  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  error = False
  form = VenueForm(request.form)
  if form.validate():

    try:
      name = request.form['name']
      city = request.form['city']
      state = request.form['state']
      address = request.form['address']
      phone = request.form['phone']
      genres = request.form.getlist('genres')
      image_link = request.form['image_link']
      facebook_link = request.form['facebook_link']
      website = request.form['website_link']
      seeking_talent = True if 'seeking_talent' in request.form else False
      seeking_description = request.form['seeking_description']

      venue = Venue(name=name, city=city, state=state, address=address, phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link, website=website, seeking_talent=seeking_talent, seeking_description=seeking_description)
      db.session.add(venue)
      db.session.commit()
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
    finally:
      db.session.close()
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    if not error:
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    if error:
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')
  else:
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  #return the list of artists
  data = db.session.query(Artist).all()

   
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  sterm = request.form.get('search_term','')
  artists = db.session.query(Artist).filter(Artist.name.ilike('%'+sterm+'%')).all()
  print(artists)
  data = []
  count = len(artists)
  for artist in artists:
    num_upcoming_shows=len(db.session.query(Show).filter(Show.artist_id==artist.id, Show.start_time>datetime.now()).all())
    data.append({
      "id": artist.id,
      "name":artist.name,
      "num_upcoming_shows":num_upcoming_shows
    })
  response={
    "count": count,
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  data = []
  #get the artist with artist_id id
  artist = db.session.query(Artist).get(artist_id)
  #get past show info
  past_show = db.session.query(Artist, Show, Venue).filter(Artist.id==Show.artist_id, Venue.id==Show.venue_id, Show.artist_id==artist_id,Show.start_time<datetime.now()).all();
  #count of the past shows
  past_shows_count=len(past_show)
  #populate the list of past shows
  past_show_data=[]
  for art, show, venue in past_show:
    past_show_data.append({
      "venue_id": venue.id,
      "venue_name": venue.name,
      "venue_image_link": venue.image_link,
      "start_time": str(show.start_time) 
    })


  #get upcoming show info
  upcoming_show = db.session.query(Artist, Show, Venue).filter(Artist.id==Show.artist_id, Venue.id==Show.venue_id, Show.artist_id==artist_id,Show.start_time>datetime.now()).all();
  #count of the upcoming shows
  upcoming_shows_count=len(upcoming_show)
  #populate the list of upcoming shows
  upcoming_show_data=[]
  for art, show, venue in upcoming_show:
    upcoming_show_data.append({
      "venue_id": venue.id,
      "venue_name": venue.name,
      "venue_image_link": venue.image_link,
      "start_time": str(show.start_time) 
    })

  #prepare the data
  data={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_show_data,
    "upcoming_shows": upcoming_show_data,
    "past_shows_count": past_shows_count,
    "upcoming_shows_count": upcoming_shows_count,
  }
   
  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  
  return render_template('pages/show_artist.html', artist=data)
  

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = db.session.query(Artist).get(artist_id)
  if artist:
    form.name.data = artist.name
    form.genres.data = artist.genres
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.website_link.data = artist.website
    form.facebook_link.data = artist.facebook_link
    form.seeking_venue.data = artist.seeking_venue
    form.seeking_description.data = artist.seeking_description
    form.image_link.data = artist.image_link
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error = False
  form = ArtistForm(request.form)
  artist = db.session.query(Artist).get(artist_id)
  if form.validate():

    try:
      artist.name = request.form['name']
      artist.genres = request.form.getlist('genres')
      artist.city = request.form['city']
      artist.state = request.form['state']
      artist.phone = request.form['phone']
      artist.website = request.form['website_link']
      artist.facebook_link = request.form['facebook_link']
      artist.seeking_venue = True if 'seeking_venue' in request.form else False
      artist.seeking_description = request.form['seeking_description']
      artist.image_link = request.form['image_link']

      db.session.add(artist)
      db.session.commit()
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
    finally:
      db.session.close()

    if not error:
      flash('Artist ' + request.form['name'] + ' was successfully edited!')
    # TODO: on unsuccessful db insert, flash an error instead.
    if error:
      flash('An error occurred. Artist '+ request.form['name']+ ' could not be edited. ')

    return redirect(url_for('show_artist', artist_id=artist_id))
  else:
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = db.session.query(Venue).get(venue_id)
  if venue:
    form.name.data = venue.name
    form.genres.data = venue.genres
    form.address.data = venue.address
    form.city.data = venue.city
    form.state.data = venue.state
    form.phone.data = venue.phone
    form.website_link.data = venue.website
    form.facebook_link.data = venue.facebook_link
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description
    form.image_link.data = venue.image_link
  
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False
  form = VenueForm(request.form)
  venue = db.session.query(Venue).get(venue_id)
  if form.validate():
    try:
      venue.name = request.form['name']
      venue.city = request.form['city']
      venue.state = request.form['state']
      venue.address = request.form['address']
      venue.phone = request.form['phone']
      venue.genres = request.form.getlist('genres')
      venue.image_link = request.form['image_link']
      venue.facebook_link = request.form['facebook_link']
      venue.website = request.form['website_link']
      venue.seeking_talent = True if 'seeking_talent' in request.form else False
      venue.seeking_description = request.form['seeking_description']

      db.session.add(venue)
      db.session.commit()
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
    finally:
      db.session.close()

    if not error:
      flash('Venue ' + request.form['name'] + ' was successfully edited!')
    # TODO: on unsuccessful db insert, flash an error instead.
    if error:
      flash('An error occurred. Venue '+ request.form['name']+ ' could not be edited. ')

    return redirect(url_for('show_venue', venue_id=venue_id))
  else:
    return render_template('forms/edit_venue.html', form=form, venue=venue)

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  error = False
  form = ArtistForm(request.form)
  if form.validate():
    try:
      name = request.form['name']
      city = request.form['city']
      state = request.form['state']
      phone = request.form['phone']
      genres = request.form.getlist('genres')
      facebook_link = request.form['facebook_link']
      image_link = request.form['image_link']
      website = request.form['website_link']
      seeking_venue = True if 'seeking_venue' in request.form else False
      seeking_description = request.form['seeking_description']

      artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link, website=website, seeking_venue=seeking_venue, seeking_description=seeking_description )
      db.session.add(artist)
      db.session.commit()
    except:
      error = False
      db.session.rollback()
      print(sys.exc_info())
    finally:
      db.session.close()
  
  
  
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    if not error:
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    if error:
      flash('An error occurred. Artist '+ request.form['name']+ ' could not be listed. ')
    
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')
  else:
    return render_template('forms/new_artist.html', form=form)

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #getting all the shows
  shows = db.session.query(Venue, Artist,Show.start_time).filter(Show.artist_id==Artist.id, Show.venue_id==Venue.id).all()
  data = []
  
  for venue, artist, start_time in shows:
    print(venue.name,artist.name)
    print("\n")
    data.append({
      "venue_id":venue.id,
      "venue_name":venue.name,
      "artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": str(start_time)
    })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False
  try:
    artist_id = request.form['artist_id']
    venue_id = request.form['venue_id']
    start_time = request.form['start_time']

    show = Show(artist_id=artist_id, venue_id = venue_id, start_time=start_time)
    db.session.add(show)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  # on successful db insert, flash success
  if not error:
    flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  if error: 
    flash('An error occurred. Show could not be listed')
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
