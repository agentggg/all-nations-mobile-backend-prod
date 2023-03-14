# Starting the project

Create an env file in the root folder of the project folder. Not the actual folder, nor the app folder, but the project folder that has all settings and etc

**#Database Dev Info**
  DATABASE_HOST=sql5.freesqldatabase.com
  DATABASE_NAME=sql5461755
  DATABASE_PASSWORD=*****
  DATABASE_PORT=3306
  DATABASE_USER=sql5461755
  DATABASE_HOST=sql5.freesqldatabase.com
  DATABASE_NAME=sql5509124
  DATABASE_PASSWORD=*****
  DATABASE_PORT=3306
  DATABASE_USER=sql5509124
  ENGINE_NAM=django.db.backends.mysql

**#Admin email (all administrative emails will be sent from this account)**
  admin_contact=raw2535@gmail.com

**Email info for Django emailing**
  email=raw2535@gmail.com
  EMAIL_HOST=smtp.gmail.com
  EMAIL_POR=587
  pas=*****

**Django Secret Key**
  SECRET_KEY=*****

**Used for Twilio messages**
  SID=*****
  TWILIO_ACCOUNT_SID=*****
  TWILIO_AUTH_TOKEN=****


**# Installing the project dependencies**
  pip install -r requirements.txt
  
**Starting Celery**
  each in their own terminal:
    redis-server
    celery -A app_backend worker -l info
    celery -A app_backend beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler




# all-nations-mobile-backend-prod
# all-nations-mobile-backend-prod
