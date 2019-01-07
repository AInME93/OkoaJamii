from datetime import datetime

from flask import render_template, request, flash
from flask_admin import expose, BaseView, AdminIndexView

from app import db
from app.organization import private

@private.route('/', methods = ['GET','POST'])

# def index():
#     return render_template('index.html', form = form)

class CustomView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/custom_index.html')

class OrganizationAdminIndexView(AdminIndexView):
    @expose('/mailbox')
    def mailboxMod(self):
        return self.render('mailbox.html')