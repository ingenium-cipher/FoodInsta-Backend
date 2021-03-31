# Introduction

This is the backend for the app FoodInsta. The app aims to solve the problem of hunger, i.e. achieving a zero hunger state which connects people in a way which ensures no food wastage occurs!

### Main features

* Django Rest Framework

* PostgreSQL in production

* Hosted on heroku

* Google Firebase for authentication and notifications and Google Drive for media file storage

# Usage

To run the project locally:

Create virtual environment :- 
		`$ virtualenv venv`

Activate the virtual environment :-
`source venv/bin/activate`

First clone the repository from Github and switch to the new directory:

    $ https://github.com/ingenium-cipher/FoodInsta-Backend
    $ cd FoodInsta-Backend
   
    
Install project dependencies:

    $ pip3 install -r requirements.txt

Make tables on database :-

`$ python3 manage.py makemigrations`
    
    
Then simply apply the migrations:

    $ python3 manage.py migrate
    

You can now run the development server:

    $ python3 manage.py runserver
