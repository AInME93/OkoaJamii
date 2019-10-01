from datetime import datetime

from flask import render_template, request, flash
from flask_admin import expose, BaseView, AdminIndexView, Admin
from flask_security import LoginForm

from app import db
from app.models import organization
from app.organization import private

# class CustomViewOrg(BaseView):
#     @expose('/')
#     def __init__(self, *args, **kwargs):
#         self._default_view = True
#         super(CustomViewOrg, self).__init__(*args, **kwargs)
#         self.admin = Admin()
#
#     def index(self, org_name):
#         return self.render('admin/custom_index.html')

class OrganizationAdminIndexView(AdminIndexView):
    @expose('/mailbox')
    def mailboxMod(self):
        return self.render('mailbox.html')

@private.route('/<org_name>')
def organizationindex(org_name):
    return '<a href="/<org_name>/admin">Go To Admin</a>'