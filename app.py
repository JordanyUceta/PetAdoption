from flask import Flask, request, render_template, redirect, session 
from models import db, connect_db, Pet
from flask_debugtoolbar import DebugToolbarExtension

from forms import AddPetForm, EditPetForm 

app = Flask(__name__)
app.app_context().push() 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'jord123'


connect_db(app) 

@app.route('/')
def main_page(): 
    pets = Pet.query.all() 
    return render_template('homepage.html', pets=pets)

@app.route("/add", methods=['get', 'post'])
def app_pet(): 
    """To add a pet.""" 

    form = AddPetForm() 

    if form.validate_on_submit(): 
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_pet = Pet(**data) 

        db.session.add(new_pet) 
        db.session.commit() 

        return redirect('/')

    else: 
        return render_template("pet_add_form.html", form=form)

@app.route("/<int:pet_id>", methods=['get', 'post'])
def edit_pet(pet_id): 
    """ Edit the info of the pet """

    pet = Pet.query.get_or_404(pet_id) 
    form = EditPetForm(obj=pet)

    if form.validate_on_submit(): 
        pet.notes = form.notes.data
        pet.available = form.available.data 
        pet.photo_url = form.photo_url.data 
        db.session.commit() 
        return redirect('/')

    else: 
        return render_template("pet_edit_form.html", form=form, pet=pet) 

