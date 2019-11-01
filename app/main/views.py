from datetime import datetime

from flask import render_template, request, flash, url_for, jsonify
from flask_admin import expose, BaseView, AdminIndexView
from flask_admin.actions import action
from flask_login import current_user
from flask_mail import Message
from werkzeug.utils import redirect

from app import db
from app.models import constituency, ward
from app.models import crimealert, country, county
from app.forms import alertForm
from app.main import public

@public.route('/',  methods = ['GET','POST'])
def index():

    form = alertForm()
    form.victCounty.choices =[('', "County")]+[(str(c.id), c.name) for c in county.query.order_by('name').all()]
    form.victConstituency.choices =[('', "Constituency")]+[(str(d.id), d.name) for d in constituency.query.order_by('name').all()]
    form.victWard.choices =[('', "Ward")]+[(str(w.id), w.name) for w in ward.query.order_by('name').all()]


    if request.method == 'POST' and form.validate():

        countyIns = form.victCounty.data
        consituencyIns = form.victConstituency.data
        wardIns = form.victWard.data

        alert = crimealert(victimType =form.typeVictim.data, victimName = form.nameVictim.data, perpetratorName = form.perpetratorName.data, \
                      reporterName=form.nameReporter.data, reporterPhone=form.phoneReporter.data, detailsCrime = form.crimeDetails.data, \
                      detailsPlace = form.placeDetails.data, country=147,county=int(countyIns), constituency = int(consituencyIns), \
                      ward = int(wardIns),status='new', urgency = 'medium', org_id= 1, location='1')

        print('Nothing here')
        db.session.add(alert)

        # alert.county.append(county.query.get(form.victCounty.data))
        # alert.constituency.append(constituency.query.get(form.victConstituency.data))
        # alert.ward.append(ward.query.get(form.victWard.data))

        try:
            print('Success')
            db.session.commit
        except AttributeError:
            print(repr(action))
            raise AttributeError
        except:
            print('Error')
            db.session.rollback()

        # need to create separate function with arguments for sending mails
        from app import mail

        ward_name = form.victWard.name
        constituency_name = form.victConstituency.name
        type_= form.typeVictim.data

        # msg = Message(subject='no reply:New Crime Report!',
        #               html='<p> We have received a new report ' \
        #               'from the following location: ' + form.victWard.data +', ' + form.victConstituency.data + '. \n' \
        #               + 'The victim is a ' + form.typeVictim.data + '<p> \n' \
        #               + '<form> <button type="submit" formaction="https://www.google.com">Open Case</button></form>',
        #               recipients=["imransaid247@gmail.com"])

        msg = Message(subject='No Reply : New Crime Report!',
                      html=render_template('reportmail.html', ward=ward_name, constituency=constituency_name, type=type_),
                      recipients=["imransaid247@gmail.com"])

        mail.send(msg)

        flash('Thank you for playing your role in saving a life!')

    return render_template('index.html', form = form)


@public.route('/_get_constituencies/', methods =['GET', 'POST'])
def _get_constituencies():
    county_id = request.args.get('victCounty', '01', type = str)
    constituencies = [('', "Constituency")]+[(str(d.id), d.name) for d in constituency.query.filter_by(county_id = county_id).order_by('name').all()]
    return jsonify(constituencies)


@public.route('/_get_wards/', methods =['GET', 'POST'])
def _get_wards():
    const_id = request.args.get('victConstituency', '01', type = str)
    wards = [('', "Ward")]+[(str(d.id), d.name) for d in ward.query.filter_by(constituency_id = const_id).order_by('name').all()]
    return jsonify(wards)

@public.route('/contact')
def contact():
    return render_template('contact.html')

@public.route('/about')
def about():
    return render_template('about.html')

"""
@public.route('/chart',  methods = ['GET','POST'])
def chart():

    return render_template('chartstest.html')"""

@public.route('/msg')
def sendmessage():
    from app import mail

    msg = Message(subject='no reply:New Crime Report!',
                  body='We have received a new' + ' email.', sender='user@gmail.com',
                  recipients=["imransaid247@gmail.com"])

    mail.send(msg)

    return 'Thank you for the email'

class CustomView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/custom_index.html')


class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.has_role('admin'):
            return redirect(url_for('public.index'))
        return self.render('admin/index.html')

    @expose('/mailbox')
    def mailboxMod(self):
        return self.render('mailbox.html')

    @expose('/randomurlthatsoundscool')
    def randomurlthatsoundscool(self):
        return self.render('mailbox.html')

    @expose('/manage')
    def managedash(self):
        return self.render('manage.html')

    @expose('/test')
    def get_all_alerts(self):
        alerts = crimealert.query.all()
        return self.render('admin/custom_index2.html',alerts=alerts)

    @expose('/analysis')
    def analysis(self):
        return self.render('admin/custom_index3.html')

    @expose('/analysis/subcounty')
    def subcounty(self):
        mvita_cases  = 0
        kisauni_cases = 0
        likoni_cases = 0
        nyali_cases = 0

        alerts = crimealert.query.all()
        for alert in alerts:
            if alert.constituency == "Mvita":
                mvita_cases += 1
            elif alert.constituency == "Kisauni":
                kisauni_cases += 1
            elif alert.constituency == "Likoni":
                likoni_cases += 1
            else:
                nyali_cases += 1

        labels = ["Mvita","Kisauni","Likoni","Nyali"]
        values = [mvita_cases,kisauni_cases,likoni_cases,nyali_cases]
        colors = [ "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA" ]
        return self.render('admin/sub_county.html', values=values, labels=labels, colors=colors)

    @expose('/analysis/casetype')
    def casetype(self):
        woman  = 0
        child = 0
        disability = 0

        alerts = crimealert.query.all()
        for alert in alerts:
            if alert.victimType == "Woman":
                woman += 1
            elif alert.victimType == "Person living with disability.":
                disability += 1
            else:
                child += 1

        labels = ["Woman","Person living with disability","Child"]
        values = [woman,disability,child]
        colors = [ "#F7464A", "#46BFBD", "#FDB45C" ]
        return self.render('admin/case_type.html', values=values, labels=labels, colors=colors)


# def populate_form_choices(registration_form):
#     countries = country.query.all()
#     counties = county.query.all()
#     constituencies = constituency.query.all()
#     wards = ward.query.all()


