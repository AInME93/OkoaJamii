from datetime import datetime

from flask import render_template, request, flash
from flask_admin import expose, BaseView, AdminIndexView
from flask_mail import Message

from app import db
from app.models import Alert
from app.forms import alertForm
from app.main import public


@public.route('/',  methods = ['GET','POST'])
def index():
    form = alertForm()

    if request.method == 'POST' and form.validate():
        alert = Alert(victimType =form.typeVictim.data, victimName = form.nameVictim.data, perpetratorName = form.perpetratorName.data, \
                      reporterName=form.nameReporter.data, reporterPhone=form.phoneReporter.data, detailsCrime = form.crimeDetails.data, \
                      detailsPlace = form.placeDetails.data, county=form.victCounty.data, constituency =form.victConstituency.data, \
                      ward = form.victWard.data, time=datetime.now(), status='new')

        db.session.add(alert)

        try:
            db.session.commit
        except:
            db.session.rollback()


        ward = form.victWard.data
        constituency = form.victConstituency.data
        type = form.typeVictim.data

        from app import mail

        # msg = Message(subject='no reply:New Crime Report!',
        #               html='<p> We have received a new report ' \
        #               'from the following location: ' + form.victWard.data +', ' + form.victConstituency.data + '. \n' \
        #               + 'The victim is a ' + form.typeVictim.data + '<p> \n' \
        #               + '<form> <button type="submit" formaction="https://www.google.com">Open Case</button></form>',
        #               recipients=["imransaid247@gmail.com"])

        msg = Message(subject='no reply:New Crime Report!',
                      html=render_template('reportmail.html', ward=ward, constituency=constituency, type=type),
                      recipients=["imransaid247@gmail.com"])


        mail.send(msg)

        flash('Thank you for playing your role in saving a life!')

    return render_template('index.html', form = form)

@public.route('/contact',  methods = ['GET','POST'])
def contact():
    return render_template('contact.html')

@public.route('/about',  methods = ['GET','POST'])
def aboutt():
    return render_template('about.html')

@public.route('/msg')
def sendmessage():
    from app import mail

    msg = Message(subject='no reply:New Crime Report!',
                  body='We have received a new' + ' email.', sender='user@gmail.com',
                  recipients=["imransaid247@gmail.com", "imran.abdalla@students.jkuat.ac.ke"])

    mail.send(msg)

    return 'Thank you for the email'

class CustomView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/custom_index.html')

class MyAdminIndexView(AdminIndexView):

    @expose('/mailbox')
    def mailboxMod(self):
        return self.render('mailbox.html')

    @expose('/randomurlthatsoundscool')
    def randomurlthatsoundscool(self):
        return self.render('mailbox.html')

    @expose('/manage')
    def managedash(self):
        return self.render('manage.html')
