from collections import UserString
import os
import json
from flask import Flask, flash, g, jsonify, session
from flask_login import login_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import render_template, redirect, request,url_for
#from flask_login import LoginManager, login_user
 
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.debug = True
 
# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
 
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)
migrate = Migrate(app,db)

# on utlise ceci pour notre application pour nous permetre de connecter et de deco l'utilisateur

from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int()
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Email()
    password = fields.Str()
    password_conf = fields.Str()

#Notre model c'est a dire notre class qui sera représenter par une table dans la BD
class User(db.Model):
    # ID
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    password_conf = db.Column(db.String(20), nullable=False)# a ne pas enregistré
    

""" @app.get('/api/user')
fonction moko
def get_all_users():
    users = [
        
            {
				"email": "deddy@gmail.com",
				"first_name": "titi",
				"last_name": "toto",
				"password": "azerty",
				"password_conf": "azerty"
			},
             {
				"email": "deddy@gmail.com",
				"first_name": "penis",
				"last_name": "kiki",
				"password": "azerty",
				"password_conf": "azerty"
			},
             {
				"email": "deddy@gmail.com",
				"first_name": "lolo",
				"last_name": "koko",
				"password": "azerty",
				"password_conf": "azerty"
			},
	]
    return users """

@app.route('/get_user', methods = ['GET'])
def get_user():
    users = User.query.all() #Recupere tous les users 
    usershema = UserSchema(many=True)
    data_send = usershema.dump(users)
    """ user_liste  =[]
    for user in users:
        user_data={
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email':user.email,
            'password':user.password,
            'password_conf':user.password_conf
		}
        user_liste.append(user_data)
        
        if request.method == "POST":
		#
		session.pop('user',None)
		#
		email= request.form['email']
		password = request.form['password']
		user = User.query.filter_by(email=email, password=password).first()
		#
		session ['user'] = request.form['email']
		#
		if user:
			return redirect(url_for('user_connect'))
		else:
			return render_template('login.html')
	return render_template('login.html'
         
          
            """
    return jsonify(data_send)

@app.route('/connecte_user',methods = ["GET","POST"])
def connecte_user():
    if request.method =='POST':
        session.pop('user',None)
        email = json.get('email')
        password = request.get('password')
        user = User.query.filter_by(email=email, password = password).first()
        session['user'] = request.data['email']
        if user :
            return "vous êtes connecter"
        else:
            return " nom for entrer"
    return "nom for entrer"
        


@app.post('/api/user')
def creat_user():
    data = request.json
    user = User(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        password=data.get('password'),
        password_conf=data.get('password_conf')
    )
    db.session.add(user)
    db.session.commit()
    return data

    
	#def __repr__(self):
		#return f"Name:{self.email}, last_name: {self.last_name}"
	
	# function to render index page
""" 
@app.route('/user_connect')
def user_connect():
	if g.user:
		return render_template('user_connect.html',user=session['user']) # ajouter
	return f"Vous etes connectes {{email}} "






@app.route('/add_data')
def add_data():
    return render_template('add_Usere.html')

@app.route('/add', methods = ["POST"])
def profile():
	# cette fonction va nous permettre de remplir le formulaire et de stocker les infos dans la bd
	email = request.form.get("first_name")
	last_name = request.form.get("last_name")
	email = request.form.get("email")
	password = request.form.get("password")
	password_conf = request.form.get("confirm_password")
# on va maintenant créer un objet a partir de la classe profile

	if first_name != " " and last_name!= " " and email!=" " and password!=" " and password_conf != " ":
		personne = User(first_name = first_name, last_name = last_name, email = email, password = password, password_conf = password_conf)
		db.session.add(personne)
		db.session.commit()
		return render_template('login.html')
	# c'est le fichier index.html qui se charge d'afficher la liste des utilisateurs
	else : 
		flash("Tous les champs du formulaire doivent être remplis.", "error")
		return redirect("/")
      
# connexion de l'utilisateur


@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		#
		session.pop('user',None)
		#
		email= request.form['email']
		password = request.form['password']
		user = User.query.filter_by(email=email, password=password).first()
		#
		session ['user'] = request.form['email']
		#
		if user:
			return redirect(url_for('user_connect'))
		else:
			return render_template('login.html')
	return render_template('login.html')


	
@app.route('/')
def index():
	# Query all data and then pass it to the template
	profiles = User.query.all()
	return render_template('index.html', profiles=profiles)

@app.route('/delete/<int:id>')
def erase(id):
	# Deletes the data on the basis of unique id and 
	# redirects to home page
	data = User.query.get(id)
	db.session.delete(data)
	db.session.commit()
	return redirect('/')


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_profile(id):
    # Récupérez l'objet Profil à mettre à jour
    profil = User.query.get(id)

    if request.method == 'POST':
        # Mettez à jour les attributs de l'objet Profil avec les nouvelles valeurs
        User.first_name = request.form['first_name']
        User.last_name = request.form['last_name']
        # Mettez à jour d'autres attributs si nécessaire

        # Confirmez les modifications dans la base de données
        db.session.commit()

        # Redirigez l'utilisateur vers une page appropriée
        return redirect(url_for('index'))  # Remplacez 'some_page' par la route appropriée

    # Affichez le formulaire pour la mise à jour
    return render_template('update.html', profil=profil)


 """
if __name__ == '__main__':
    app.run(debug=True)

# 