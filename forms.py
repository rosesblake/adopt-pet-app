from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import InputRequired, Optional, NumberRange, ValidationError, URL

def allowed_species(form, field):
    allowed_species = ['cat', 'dog', 'porcupine']
    if field.data.lower() not in allowed_species:
        raise ValidationError('Species must be "cat", "dog", or "porcupine".')

class AddPetForm(FlaskForm):
    """form for adding a pet"""
    name = StringField('Pet Name', validators=[InputRequired(message='Please enter pet name')])
    species = StringField('Species', validators=[InputRequired(message='Please enter cat, dog, or porcupine'), allowed_species])
    photo_url = StringField('Photo URL', validators=[Optional(), URL(message='Please enter a valid URL')])
    age = IntegerField('Age', validators=[Optional(), NumberRange(min=0, max=30, message='Age must be between 0 and 30')])
    notes = StringField('Additional Notes')
    available = SelectField('Available', choices=[('yes', 'Yes'), ('no', 'No')], default='yes')
    