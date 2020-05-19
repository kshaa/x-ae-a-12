# X Æ A-12
Flask web app for sending push notifications using a web-hook  

Bootstrapped using [the Flask-User-Starter-App](https://github.com/lingthio/Flask-User-starter-app/)  
Push notifications sourced from [Push Notifications codelab](https://github.com/GoogleChrome/push-notifications)  

## Environment
Developed on python 3.6.9, other versions might also work  
Install dependencies using `pip install -r requirements.txt`  
Configure `app/local_settings.py` using `app/local_settings_example.py` as a template  
Initialize the database with migrations using `flask db upgrade`  

## Usage
Start the Flask development web server using `python3 manage.py runserver`  
Open `http://localhost:5000/`  

Example user story:  
- Register
- Confirm email
- Login
- Subscribe to push notifications using bell icon
- Create message topic
- Create API key
- Send messages using CLI through a webhook `http://localhost:5000/api/notify?key=<API_KEY>&topic=<TOPIC_CODE>&message=<MESSAGE>`  
