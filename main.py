import json
import os
import pytz
import datetime

from flask import Flask
from google.appengine.ext import db
from google.appengine.ext import ndb

from datetime import timedelta
from flask import request
from flask import render_template

app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

import jinja2
import webapp2
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_CABDETAIL = 'default_cabdetail'
@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Geo Cab Track service.'

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

class CabDetails(db.Model):
  cab_no = db.StringProperty()
  ldap = db.StringProperty()
  complaint_date = db.DateTimeProperty()
  shift_time = db.StringProperty()
  ticket_time = db.StringProperty()

def cabdetail_key(cab_detail=DEFAULT_CABDETAIL):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('CabDetails', cab_detail)

#@app.route('/savecab/?cab_no=<int:cab_no>&ldap=<string:ldap>&shift=<string:shift>', methods=['POST', 'GET'])
@app.route('/savecab/', methods=['POST', 'GET'])
def Save():
  if request.method in ['POST', 'GET']:
    cab_number=request.args.get('cab_no', '')
    requested_ldap = request.args.get('ldap', '')
    requested_shift_time = request.args.get('shift', '')
    get_ticket_time = request.args.get('ticket_time', '')
    cab = CabDetails(cab_no=cab_number, ldap=requested_ldap,
                     shift_time=requested_shift_time,
                     ticket_time=get_ticket_time)
    #utc=pytz.timezone("UTC")
    #india = pytz.timezone("Asia/Kolkata")
    cab.complaint_date = datetime.datetime.now()+timedelta(hours=5, minutes=30)
    cab.put()
    return "success"
  else:
    return "fail"
@app.route('/getcabdetails', methods=['GET'])
def GetCabDetail():
  if request.method == 'GET':
    cab = CabDetails()
    cab_data = CabDetails.gql('ORDER BY complaint_date DESC')
    #k =[]
    #for i in cab_data:
    #  k.append(i.ldap)      
    #return json.dumps(k)
    return render_template('index.html',cab_data= cab_data)
