<!-- ABOUT THE PROJECT -->
## Capstone_group5 : Volunteer Social Network

This web-based platform, reminiscent of professional networks, is specifically tailored for the volunteering ecosystem.

DB: MySQL(8.0.34)
Framework: Django(4.2.5)
Libraries used: rest_framework(3.14.0)

<!-- GETTING STARTED -->
## Getting Started

To ensure that all developers are developing in the same environment, follow these simple example steps.

### Installation

1. Clone (in the Terminal)
```sh
git clone https://github.com/gurjots29/Capstone_group5.git
```
2. Start a virtualenv and install requirements
```sh
python3 -m venv venv  or  python -m venv venv
source venv/bin/activate (MAC/Linux)
venv\scripts\activate (Windows)
pip install -r requirements.txt
```
3. Setup MySQL
- Install MySQL and Create DB name, User id and Password
- You need to change 'default'
- volunteer_platform/settings.py  
```sh
DATABASES = {
    'default': {
 		'ENGINE': 'django.db.backends.mysql',
 		'NAME': 'volunteer',   # your DB name in MySQL
 		'USER': 'root',     # your User Id in MySQL
 		'PASSWORD': 'Admin$101011',   # your Password in MySQL
 		'HOST':'localhost',
 		'PORT':'3306',
 	}
}
```
4. Modify Timezone    // volunteer_platform/settings.py
- Change to the time zone we're in Vancouver instead of UTC
```sh
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Vancouver'    # 'UTC' -> 'America/Vancouver

USE_I18N = True

USE_TZ = False     # TRUE -> False

```
6. Run migrations and seed the database
```sh
python manage.py makemigrations
python manage.py migrate
```
7. Start the Server
```sh
python manage.py runserver
```
8. Check the running API
```sh
http://127.0.0.1:8000/api/post/post/
```
