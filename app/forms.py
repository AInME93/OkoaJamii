from flask_security import RegisterForm
from flask_wtf import FlaskForm
from wtforms import BooleanField, validators, StringField, TextField, SelectField, TextAreaField, SubmitField
from wtforms.fields.html5 import EmailField, TelField

from app.models import user


class ExtendedRegisterForm(RegisterForm):

    username = StringField('Username',[validators.DataRequired(message='username is required')])

    def validate(self):
        """ Add username validation
        #ha

            :return: True is the form is valid
        """
        # Use standard validator
        validation = FlaskForm.validate(self)
        if not validation:
            return False

        # Check if username already exists
        user_ = user.query.filter_by(
            username=self.username.data).first()
        if user_ is not None:
            # Text displayed to the user
            self.username.errors.append('Username already exists. Try a unique name that best describes you, like LadiesMan01.')
            return False

        return True

    remember = BooleanField('Remember Me')

class alertForm(FlaskForm):

    nameVictim = TextField("Name Of Victim")
    perpetratorName = TextField("Name of Perpetrator")
    typeVictim = SelectField("Type of Victim", choices = [('','Type of Victim'),('Woman', 'Woman'),
                                                          ('Child','Child'),
                                                          ('Person living with disability.','Person living with disability.')], validators = [validators.Required()])
    nameReporter = TextField("Your Name(Optional)")
    phoneReporter = TelField("Your Phone Number (Optional)")
    victCountry = SelectField()
    victCounty = SelectField()
    victConstituency = SelectField()
    victWard = SelectField()
    crimeDetails = TextAreaField("Please describe the crime/incident in detail")
    placeDetails = TextAreaField("Please describe the place where the crime is committed in detail")
    submit = SubmitField("Report Anonymously")