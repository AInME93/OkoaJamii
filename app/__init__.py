from flask import Flask, url_for
from flask_admin import Admin
from flask_admin import helpers as admin_helpers

from config import config
from flask_security import Security, SQLAlchemyUserDatastore
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models import User, Role, Alert
from app.models import MyModelView, UserView, OrganizationModelView, UserViewOrg
from app.main.views import MyAdminIndexView
from app.organization.views import OrganizationAdminIndexView
mail = Mail()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from app.forms import ExtendedRegisterForm

    # Create admin
    admin = Admin(
        app,
        'My Dashboard',
        index_view=MyAdminIndexView(),
        base_template='my_master.html',
        template_mode='bootstrap3'
    )

    org_admin = Admin(
        app,
        'Dashboard',
        index_view= OrganizationAdminIndexView(url='/<org_name>/admin', endpoint='organization'),
        base_template='my_master.html',
        template_mode='bootstrap3'
    )

    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore, register_form=ExtendedRegisterForm)

    from app.main import public as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.organization import private as private_blueprint
    app.register_blueprint(private_blueprint)

    # define a context processor for merging flask-admin's template context into the
    # flask-security views.
    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
        )

    from app.main.views import CustomView

    # Add model views
    admin.add_view(MyModelView(Alert, db.session, menu_icon_type='fa', menu_icon_value='fa-exclamation-triangle', name="Alerts"))
    admin.add_view(MyModelView(Role, db.session, menu_icon_type='fa', menu_icon_value='fa-server', name="Roles"))
    admin.add_view(UserView(User, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="Users"))
    admin.add_view(CustomView(name="Custom view", endpoint='custom', menu_icon_type='fa', menu_icon_value='fa-connectdevelop', ))


    # org_admin.add_view(OrganizationModelView(Alert, db.session, menu_icon_type='fa', menu_icon_value='fa-exclamation-triangle', name="Alerable"))
    org_admin.add_view(CustomView(name="Custom", endpoint='custom_1', menu_icon_type='fa', menu_icon_value='fa-connectdevelop', ))


    with app.app_context():
        db.init_app(app)
        mail.init_app(app)
        # admin.init_app(app)
    
    

    return app
