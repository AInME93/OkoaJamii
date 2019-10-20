from datetime import datetime
from gettext import ngettext, gettext

from flask import url_for, request, render_template, helpers, flash
from flask_admin import expose, form
from flask_admin.actions import action
from flask_admin.model.template import EndpointLinkRowAction
from flask_security import UserMixin, RoleMixin, current_user, LoginForm, login_user, logout_user, url_for_security
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from flask_admin.contrib import sqla

from app import db


# Define models

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    status = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), default='1')
    modified_at = db.Column(db.DateTime())
    modified_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    deleted_at = db.Column(db.DateTime())
    deleted_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __str__(self):
        return self.name


class user(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    org_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    status = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), default='1')
    modified_at = db.Column(db.DateTime())
    modified_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    deleted_at = db.Column(db.DateTime())
    deleted_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    roles = db.relationship('role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.username


class crimealert(db.Model):
    __tablename__ = "crimealert"
    id = db.Column(db.Integer, primary_key=True)
    victimType = db.Column(db.String(255))
    victimName = db.Column(db.String(255))
    perpetratorName = db.Column(db.String(255))
    reporterName = db.Column(db.String(255))
    reporterPhone = db.Column(db.String(255))
    detailsCrime = db.Column(db.String(1250))
    detailsPlace = db.Column(db.String(1250))
    country = db.Column(db.Integer, db.ForeignKey('country.id'))
    county = db.Column(db.Integer, db.ForeignKey('county.id'))
    constituency = db.Column(db.Integer, db.ForeignKey('constituency.id'))
    ward = db.Column(db.Integer, db.ForeignKey('ward.id'))
    urgency = db.Column(db.String(255))
    location = db.Column(db.String(255))
    status = db.Column(db.String(255))
    org_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    updated_at = db.Column(db.DateTime())
    deleted_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    deleted_at = db.Column(db.DateTime())

    county_ = db.relationship('county', backref=db.backref('crimealert', lazy='dynamic'))
    constituency_ = db.relationship('constituency', backref=db.backref('crimealert', lazy='dynamic'))
    ward_ = db.relationship('ward', backref=db.backref('crimealert', lazy='dynamic'))

    def __str__(self):
        return self.VictimType + ' ' + self.ward + '-' + self.time

# case_staff = db.Table('case_staff',
#         db.Column('case_id', db.Integer(), db.ForeignKey('Case.id')),
#         db.Column('role_id', db.Integer(), db.ForeignKey('Staff.id')))


class organization(db.Model):
    __tablename__ = "organization"
    id = db.Column(db.Integer, primary_key=True)
    orgName = db.Column(db.String(255))
    # logo = db.Column(db.LargeBinary)
    webURL = db.Column(db.String(255))
    orgBrief = db.Column(db.String(255))
    email = db.Column(db.String(255))
    founded = db.Column(db.DateTime())
    registered = db.Column(db.DateTime())
    alertCount = db.Column(db.Integer)
    address = db.Column(db.String(255))

    status = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), default='1')
    modified_at = db.Column(db.DateTime())
    modified_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    deleted_at = db.Column(db.DateTime())
    deleted_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __str__(self):
        return self.orgName


class country(db.Model):
    __tablename__ = "country"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    status = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), default='1')
    modified_at = db.Column(db.DateTime())
    modified_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    deleted_at = db.Column(db.DateTime())
    deleted_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __str__(self):
        return self.name

class county(db.Model):
    __tablename__ = "county"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    status = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), default='1')
    modified_at = db.Column(db.DateTime())
    modified_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    deleted_at = db.Column(db.DateTime())
    deleted_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __str__(self):
        return self.name


class constituency(db.Model):
    __tablename__ = "constituency"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    county_id = db.Column(db.Integer, db.ForeignKey('county.id'))
    status = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), default='1')
    modified_at = db.Column(db.DateTime())
    modified_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    deleted_at = db.Column(db.DateTime())
    deleted_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __str__(self):
        return self.name

class ward(db.Model):
    __tablename__ = "ward"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    constituency_id = db.Column(db.Integer, db.ForeignKey('constituency.id'))
    status = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), default='1')
    modified_at = db.Column(db.DateTime())
    modified_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    deleted_at = db.Column(db.DateTime())
    deleted_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __str__(self):
        return self.name

# class Case(db.Model):
#     __tablename__ = "Case"
#     id = db.Column(db.Integer, primary_key=True)
#     victimType = db.Column(db.String(255))
#     victimName = db.Column(db.String(255))
#     perpetratorName = db.Column(db.String(255))
#     reporterName = db.Column(db.String(255))
#     reporterPhone = db.Column(db.String(255))
#     detailsCrime = db.Column(db.String(1250))
#     detailsPlace = db.Column(db.String(1250))
#     county = db.Column(db.String(255))
#     constituency = db.Column(db.String(255))
#     urgency = db.Column(db.String(255))
#     type = db.Column(db.String(255))
#     assignedOrganization = db.Column(db.String(255))
#     location = db.Column(db.String(255))
#     time = db.Column(db.DateTime())
#     stage = db.Column(db.String(255))
#     # files = db.Column(db.LargeBinary, nullable=True)
#
#     status = db.Column(db.Boolean())
#     created_at = db.Column(db.DateTime())
#     created_by = db.Column(db.Integer, db.ForeignKey('user.id'), default='1')
#     modified_at = db.Column(db.DateTime())
#     modified_by = db.Column(db.Integer, db.ForeignKey('user.id'), default='1')
#     deleted_at = db.Column(db.DateTime())
#     deleted_by = db.Column(db.Integer, db.ForeignKey('user.id'), default='1')
#
#
#     assignedStaff = db.relationship('Staff', secondary=case_staff,
#                             backref=db.backref('staff', lazy='dynamic'))
#
#     def __str__(self):
#         return self.id + ' ' + self.victimName
#
# class Person(db.Model):
#     __tablename__ = "Person"
#     id = db.Column(db.Integer, primary_key=True)
#     Type = db.Column(db.String(255))
#     personFirstName = db.Column(db.String(255))
#     personSecondName = db.Column(db.String(255))
#     personLastName = db.Column(db.String(255))
#     identification = db.Column(db.String(255))
#     DOB = db.Column(db.DateTime())
#     photo = db.Column(db.LargeBinary)
#     gender = db.Column(db.String(255))
#     phoneNo1 = db.Column(db.String(255))
#     phoneNo2 = db.Column(db.String(255))
#     occupation = db.Column(db.String(255))
#     caseCount = db.Column(db.Integer)
#
#     status = db.Column(db.Boolean())
#     created_at = db.Column(db.DateTime())
#     created_by = db.Column(db.Integer, db.ForeignKey('user.id'), default='1')
#     modified_at = db.Column(db.DateTime())
#     modified_by = db.Column(db.Integer, db.ForeignKey('user.id'), default='1')
#     deleted_at = db.Column(db.DateTime())
#     deleted_by = db.Column(db.Integer, db.ForeignKey('user.id'), default='1')
#
#     def __str__(self):
#         return self.personFirstName + ' ' + self.personSecondName + ' ' + self.personLastName
#
# class Staff(db.Model):
#     __tablename__ = "Staff"
#     id = db.Column(db.Integer, primary_key=True)
#     staffFirstName = db.Column(db.String(255))
#     staffSecondName = db.Column(db.String(255))
#     staffLastName = db.Column(db.String(255))
#     organization = db.Column(db.String(255))
#     password = db.Column(db.String(255))
#     staffDesignation = db.Column(db.String(255))
#     identification = db.Column(db.String(255))
#     DOB = db.Column(db.DateTime())
#     photo = db.Column(db.LargeBinary, nullable=True)
#     gender = db.Column(db.String(255))
#     phoneNo1 = db.Column(db.String(255))
#     phoneNo2 = db.Column(db.String(255))
#     caseCount = db.Column(db.Integer)
#
#     status = db.Column(db.Boolean())
#     created_at = db.Column(db.DateTime())
#     created_by = db.Column(db.Integer, db.ForeignKey('user.id'), default='1')
#     modified_at = db.Column(db.DateTime())
#     modified_by = db.Column(db.Integer, db.ForeignKey('user.id'), default='1')
#     deleted_at = db.Column(db.DateTime())
#     deleted_by = db.Column(db.Integer, db.ForeignKey('user.id'), default='1')
#
#     def __str__(self):
#         return self.staffFirstName + ' ' + self.staffLastName


# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('admin'):
            return True

        return False

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('new'))


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

    edit_modal_template = 'admin/edit.html'
    details_modal_template = "admin/details.html"
    # can_edit = True
    edit_modal = True
    create_modal = True
    can_export = True
    can_view_details = True
    details_modal = True

    @expose('/mailbox')
    def mailboxMod(self):
        return self.render('mailbox.html')

class AlertView(MyModelView):

    def get_query(self):
        return self.session.query(self.model).filter(self.model.status != 'assigned', self.model.org_id == 1)

    column_list = ['victimName', 'victimType', 'perpetratorName','reporterName', 'reporterPhone', 'detailsCrime', 'detailsPlace', \
                   'county_', 'constituency_.name', 'ward_', 'urgency', 'status', 'org_id']
    column_searchable_list = ['victimName', 'victimType', 'perpetratorName', 'ward_.name', 'constituency_.name', 'county_.name']
    column_labels = dict(victimName = 'Victim', victimType = 'Type', perpetratorName = 'Perpetrator',\
                         reporterName = 'Reporter', reporterPhone = 'Reporter #', detailsCrime ='Details', \
                         detailsPlace = 'Place Description', county = 'County', constituency = 'Constituency', \
                         ward = 'Ward',urgency = 'Urgency', org_id = 'organization')

    column_filters = column_searchable_list
    column_select_related_list = ['county_']

    # form_widget_args = {
    #     'victimName': {'rows': 100,
    #                 'placeholder': 'ex. M132 or T456'
    #                 }
    #             }
    can_edit = False
    can_create = False

    @action('pick_case', 'Pick Case', 'Are you sure you want to pick this alert and create a new case?')
    def action_pick_case(self, ids):
        try:
            query = crimealert.query.filter(crimealert.id.in_(ids))

            for alert in query.all():
                # case = Case(victimType =alert.victimType,
                #             victimName = alert.victimName,
                #             perpetratorName= alert.perpetratorName,
                #             reporterName = alert.reporterName,
                #             reporterPhone = alert.reporterPhone,
                #             detailsCrime = alert.detailsCrime,
                #             detailsPlace = alert.detailsPlace,
                #             county = alert.county,
                #             constituency = alert.constituency,
                #             time = datetime.now())
                #
                # db.session.add(case)
                alert.status ='assigned'
                alert.updated_at = datetime.now()
                alert.updated_by = current_user.id

                try:
                    db.session.commit
                except:
                    db.session.rollback()

                flash('Case picked succesfully', 'message')

        except Exception as ex:
            print('Error encountered: ',ex)
            flash('Failed to pick alert', 'error')

    list_template = 'lists/alerts.html'

class RoleView(MyModelView):
    column_editable_list = ['name']
    column_searchable_list = column_editable_list
    column_filters = column_editable_list

class UserView(MyModelView):

    @action('approve', 'Approve', 'Are you sure you want to approve selected users?')
    def action_approve(self, ids):
        try:
            query = user.query.filter(user.id.in_(ids))

            # count = 0
            # for user in query.all():
            #     if user.approve():
            #         count += 1
            #
            # flash(ngettext('User was successfully approved.',
            #                '%(count)s users were successfully approved.',
            #                count)
            #                count=count)

        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise

            flash(gettext('Failed to approve users. %(error)s', error=str(ex)), 'error')

    column_editable_list = ['email', 'username']
    column_searchable_list = column_editable_list
    column_exclude_list = ['password']
    # form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list
    # column_extra_row_actions = [
    #     EndpointLinkRowAction('fa fa-plus', 'user.action_play'),
    # ]
    column_auto_select_related = True
    list_template = 'lists/users.html'

    # @expose('/action/play', methods=('GET','POST'))
    # def action_play(self, *args, **kwargs):
    #     flash('NEW')
    #     return self.handle_action()
    #

class OrgView(MyModelView):
    column_exclude_list = ['alertCount']
    form_excluded_columns = column_exclude_list


# class StaffView(MyModelView):
#     column_editable_list = ['staffFirstName']
#     column_searchable_list = column_editable_list
#     column_filters = column_editable_list
#     column_labels = dict(Stafffirstname = 'First Name', Staffsecondname = 'Middle Name',Stafflastname = 'Last Name',\
#                          Staffdesignation = 'Designation', Dob = 'Date of Birth')
#

    # form_overrides = {
    #     'photo': request.files['fileimg'].read(),
    # }

    # def on_model_change(self, form, model, is_created = False):
    #     model.photo = bytes(model.photo, 'utf-8')
    #     pass
    #
    # def after_model_change(self, form, model, is_created):
    #     if is_created:
    #         # newUser = User(email = form.email.data, password = 'newpassword')
    #         model.photo = str(model.photo, 'utf-8')
    #         # db.session.add(newUser)
    #         # db.session.commit()
    #
    #     else:
    #         model.photo = str(model.photo, 'utf-8')


# class CaseView(MyModelView):
#     column_editable_list = ['victimType']
#     column_searchable_list = column_editable_list
#     column_exclude_list = ['assignedOrganization','location']
#     form_excluded_columns = column_exclude_list
#     column_details_exclude_list = column_exclude_list
#     column_filters = column_editable_list
#
#     column_labels = dict(victimName = 'Victim', victimType = 'Type', perpetratorName = 'Perpetrator',\
#                          reporterName = 'Reporter', reporterPhone = 'Reporter #', detailsCrime ='Details', \
#                          detailsPlace = 'Place Description', county = 'County', constituency = 'Constituency', \
#                          ward = 'Ward',urgency = 'Urgency', choiceOrganization = 'Organization')


# # Create customized model view class
# class OrganizationModelView(sqla.ModelView):
#
#     def is_accessible(self):
#         if not current_user.is_active or not current_user.is_authenticated:
#             return False
#
#         if current_user.has_role('admin'):
#             return True
#
#         return False
#
#     def _handle_view(self, name, **kwargs):
#         """
#         Override builtin _handle_view in order to redirect users when a view is not accessible.
#         """
#         if not self.is_accessible():
#             if current_user.is_authenticated:
#                 # permission denied
#                 abort(403)
#             else:
#                 # login
#                 return redirect(url_for('security.login', next=request.url))
#
#
#     # can_edit = True
#     edit_modal = True
#     create_modal = True
#     can_export = True
#     can_view_details = True
#     details_modal = True
#
#     @expose('/mailbox')
#     def mailboxMod(self):
#         return self.render('mailbox.html')
#
# class UserViewOrg(OrganizationModelView):
#     column_editable_list = ['email']
#     column_searchable_list = column_editable_list
#     column_exclude_list = ['password']
#     # form_excluded_columns = column_exclude_list
#     column_details_exclude_list = column_exclude_list
#     column_filters = column_editable_list