from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, render_template, redirect, request, flash
from models import db, Pet
from forms import AddPetForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Initialize SQLAlchemy and connect to app
db.init_app(app)
debug = DebugToolbarExtension(app)
#cant run without this context push
app.app_context().push()

@app.route('/')
def pet_list():
    '''list all pets in db'''
    pets = Pet.query.all()
    return render_template('pets.html', pets=pets)

@app.route('/add', methods=['GET', 'POST'])
def add_pet_form():
    '''show form to add a new pet'''
    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        # add new pet to db 
        new_pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)
        db.session.add(new_pet)
        db.session.commit()
        return redirect("/")
    else:
        return render_template('add-pet.html', form=form)
    
    # need help here. cant get it to submit post request unless i separate the get and post routes.
@app.route('/<int:pet_id>', methods=['GET'])
def pet_details(pet_id):
    """show details about a specific pet"""
    pet = Pet.query.get_or_404(pet_id)
    form = AddPetForm(obj=pet)
    return render_template('pet-details.html', pet=pet, form=form)
    
@app.route('/<int:pet_id>', methods=['POST'])
def edit_pet_details(pet_id):
    """edit pet details"""
    pet = Pet.query.get_or_404(pet_id)
    form = AddPetForm(obj=pet)
    pet.photo_url = form.photo_url.data
    pet.notes = form.notes.data
    # cant get the available to prepopulate correctly
    pet.available = form.available.data == 'yes'
    db.session.commit()
    return redirect(f"/{pet_id}")
