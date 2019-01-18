from flask import url_for, request, render_template, helpers, flash
from flask_admin import expose
from flask_security import UserMixin, RoleMixin, current_user, LoginForm, login_user, logout_user, url_for_security
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from flask_admin.contrib import sqla
from app import db


# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('User.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('Role.id')))

class Role(db.Model, RoleMixin):
    __tablename__ = "Role"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


class Alert(db.Model):
    __tablename__ = "Alert"
    id = db.Column(db.Integer, primary_key=True)
    victimType = db.Column(db.String(255))
    victimName = db.Column(db.String(255))
    perpetratorName = db.Column(db.String(255))
    reporterName = db.Column(db.String(255))
    reporterPhone = db.Column(db.String(255))
    detailsCrime = db.Column(db.Text(1250))
    detailsPlace = db.Column(db.Text(1250))
    county = db.Column(db.String(255))
    constituency = db.Column(db.String(255))
    ward = db.Column(db.String(255))
    urgency = db.Column(db.String(255))
    choiceOrganization = db.Column(db.String(255))
    location = db.Column(db.String(255))
    time = db.Column(db.DateTime())
    status = db.Column(db.String(255))

class Case(db.Model):
    __tablename__ = "Case"
    id = db.Column(db.Integer, primary_key=True)
    victimType = db.Column(db.String(255))
    victimName = db.Column(db.String(255))
    perpetratorName = db.Column(db.String(255))
    reporterName = db.Column(db.String(255))
    reporterPhone = db.Column(db.String(255))
    detailsCrime = db.Column(db.String(1250))
    detailsPlace = db.Column(db.String(1250))
    county = db.Column(db.String(255))
    constituency = db.Column(db.String(255))
    urgency = db.Column(db.String(255))
    type = db.Column(db.String(255))
    assignedOrganization = db.Column(db.String(255))
    location = db.Column(db.String(255))
    time = db.Column(db.DateTime())
    stage = db.Column(db.String(255))
    files = db.Column(db.LargeBinary)

class Person(db.Model):
    __tablename__ = "Person"
    id = db.Column(db.Integer, primary_key=True)
    Type = db.Column(db.String(255))
    personName = db.Column(db.String(255))
    identification = db.Column(db.String(255))
    DOB = db.Column(db.DateTime())
    photo = db.Column(db.LargeBinary)
    gender = db.Column(db.String(255))
    phoneNo1 = db.Column(db.String(255))
    phoneNo2 = db.Column(db.String(255))
    occupation = db.Column(db.String(255))
    caseCount = db.Column(db.Integer)

class Organization(db.Model):
    __tablename__ = "Organization"
    id = db.Column(db.Integer, primary_key=True)
    orgName = db.Column(db.String(255))
    logo = db.Column(db.LargeBinary)
    webURL = db.Column(db.String(255))
    orgBrief = db.Column(db.String(255))
    founded = db.Column(db.DateTime())
    registered = db.Column(db.DateTime())
    alertCount = db.Column(db.Integer)

class Staff(db.Model):
    __tablename__ = "Staff"
    id = db.Column(db.Integer, primary_key=True)
    staffFirstName = db.Column(db.String(255))
    staffSecondName = db.Column(db.String(255))
    staffLastName = db.Column(db.String(255))
    organization = db.Column(db.String(255))
    password = db.Column(db.String(255))
    staffDesignation = db.Column(db.String(255))
    identification = db.Column(db.String(255))
    DOB = db.Column(db.DateTime())
    photo = db.Column(db.LargeBinary)
    gender = db.Column(db.String(255))
    phoneNo1 = db.Column(db.String(255))
    phoneNo2 = db.Column(db.String(255))
    caseCount = db.Column(db.Integer)

# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('admin'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


    # can_edit = True
    edit_modal = True
    create_modal = True
    can_export = True
    can_view_details = True
    details_modal = True

    @expose('/mailbox')
    def mailboxMod(self):
        return self.render('mailbox.html')

class UserView(MyModelView):
    column_editable_list = ['email']
    column_searchable_list = column_editable_list
    column_exclude_list = ['password']
    # form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list

# Create customized model view class
class OrganizationModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('admin'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


    # can_edit = True
    edit_modal = True
    create_modal = True
    can_export = True
    can_view_details = True
    details_modal = True

    @expose('/mailbox')
    def mailboxMod(self):
        return self.render('mailbox.html')

class UserViewOrg(OrganizationModelView):
    column_editable_list = ['email']
    column_searchable_list = column_editable_list
    column_exclude_list = ['password']
    # form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list