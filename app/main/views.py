from datetime import datetime

from flask import render_template, request, flash
from flask_admin import expose, BaseView, AdminIndexView

from app import db
from app.models import Alert
from app.forms import alertForm
from app.main import public

@public.route('/', methods = ['GET','POST'])
def index():
    form = alertForm()

    if request.method == 'POST' and form.validate():
        alert = Alert(victimType =form.typeVictim.data,victimName = form.nameVictim.data, reporterName=form.nameReporter.data, \
                      reporterEmail=form.emailReporter.data,details = form.crimeDetails.data, \
                      county=form.victCounty.data,constituency =form.victConstituency.data, time=datetime.now(),status='new')
        db.session.add(alert)
        db.session.commit
        flash('Thank you for playing your role in saving a life!')

    return render_template('index.html', form = form)

class CustomView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/custom_index.html')

class MyAdminIndexView(AdminIndexView):
    @expose('/mailbox')
    def mailboxMod(self):
        return self.render('mailbox.html')