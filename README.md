# Deploying a Django Application on Nginx

### Prerequisites
    - Django project located at /home/ubuntu/djangoapp

    - Virtual environment located at /home/ubuntu/djangoapp/venv

    - Nginx installed

    - Gunicorn installed in the virtual environment

    - Django project- Tested locally and has a requirements.txt

## Steps to Deploy
## Secure Key Management8 using .env
Main aim is to separate sensitive data with the code base.

```bash
pip install python-decouple
```

### Create a .env on the root directory
```bash
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=db_name
DB_USER=db_user
DB_PASSWORD=db_password
DB_HOST=db_host
DB_PORT=3306
ALLOWED_HOSTS=127.0.0.1,yourdomain.com

```
### Consuming data from the .env
Update your settings.py or any other location that reads from the .env
```python
from decouple import config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Fetching the secret key from the .env file
SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG',cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS',default='').split(',')

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT',cast=int,default='3306'),
    }
}
```

## Install Required Packages
Run the following to install dependancies
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx
```

## Upload website files.
Your website files can be uploaded in a number of ways. The most convenient one is cloning a github repository.
```
#clone the code. Ensure you are in the root directory.
cd /home/ubuntu/djangoapp/
git clone https://repository-link.git

#move the files to the root durectory
mv git-folder/* .

```
If the files are in form of a zip file, you can use scp method to upload them.
```
#For AWS
scp -i ~/path-to-your-key.pem djangoapp.zip ec2-user@192.0.2.0:/home/ubuntu/djangoapp
unzip djangoapp.zip

#Other VPS
scp djangoapp.zip username@remote-server:/home/ubuntu/djangoapp

```

## Create, Activate Virtual Environment and Install Gunicorn
Run the following:
```bash
#Ensure you are in the work directory
cd /home/ubuntu/djangoapp

#create virtualenv
python3 -m venv venv

#Activate virtualenv
source venv/bin/activate

#Install dependencies
pip install --upgrade pip    #Optional. 
pip install -r requirements.txt
pip install gunicorn

```


## Create a Gunicorn Systemd Service File
```bash
sudo nano /etc/systemd/system/djangoapp.service
```
Add the following. Adjust the paths accordingly. Refer to the root directories you set.
```bash
[Unit]
Description=gunicorn daemon for djangoapp
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/home/ubuntu/djangoapp
ExecStart=/home/ubuntu/djangoapp/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/home/ubuntu/djangoapp/djangoapp.sock \
    djangoproject.wsgi:application

[Install]
WantedBy=multi-user.target
```
##Note: Replace djangoproject with the directory name that holds your wsgi.py file.

## Start and Enable Gunicorn Service
```bash
sudo systemctl start djangoapp
sudo systemctl enable djangoapp
```

## Configure Nginx
Run the following command:
```bash
sudo nano /etc/nginx/sites-available/djangoapp
```
Add the Following Content:
```bash
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com and or ServerIP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ubuntu/djangoapp;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/djangoapp/djangoapp.sock;
    }
}
```

The above block, will make the  web application to be accessed by both PublicIP and domain name-if provided. We may want to only access our website using the domain name, and or redirect the traffic from the IP to the domain name. We can update the above code by the following:

```bash
# Redirect traffic from the server's public IP to the domain
server {
    listen 80;
    server_name your-server-ip;

    return 301 http://yourdomain.com$request_uri;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ubuntu/djangoapp;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/djangoapp/djangoapp.sock;
    }
}
```

## Enable the Nginx Configuration
```
sudo nginx -t
sudo ln -s /etc/nginx/sites-available/djangoapp /etc/nginx/sites-enabled
sudo systemctl restart nginx
```



## Change Ownership or Permissions
Update file ownership
```bash
# Set ownership of the directory and socket file to www-data
sudo chown -R www-data:www-data /home/ubuntu/djangoapp

# Allow read, write, and execute for the directory
sudo chmod 755 /home/ubuntu/djangoapp

# Allow read and write for the socket file
sudo chmod 664 /home/ubuntu/djangoapp/djangoapp.sock

#add the Nginx user (www-data) to a group that owns the directory or socket file:
sudo usermod -aG ubuntu www-data
```
Once permissions are updated, restart the following services.

```bash
sudo systemctl daemon-reload
sudo systemctl restart djangoapp
sudo systemctl restart nginx
```

## Application Monitoring and Maintainance
To inspect application logs, see the following.
```bash
#Check Gunicorn logs: 
journalctl -u djangoapp
journalctl -f -u djangoapp

Access logs: /var/log/nginx/djangoapp_access.log
Error logs: /var/log/nginx/djangoapp_error.log
example:
tail -f /var/log/nginx/mydjangoapp_error.log
```
At this stage, your website should be accessible if operating on the sqlite3 DB. To configure MySQL mysql database, follow the following steps.
## 11. How to Install MySQL Server. 
### Update Package Lists
```bash
sudo apt update
```

### Install MySQL Server
```bash
sudo apt install mysql-server
```

### Configure MySQL
```bash
sudo mysql_secure_installation
```
### Start and Enable MySQL Service
```bash
sudo systemctl start mysql  #Start mysql service
sudo systemctl enable mysql #enable the service to start on reboot
```

### Verify MySQL Installation
```bash
sudo mysql
```

### Create Database and user
```bash
CREATE DATABASE mydatabase;
USE mydatabase;

#create a user
CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'mypassword'; 

#Grant privileges
GRANT ALL PRIVILEGES ON mydatabase.* TO 'myuser'@'localhost';
FLUSH PRIVILEGES;
```

# Configure mysql on Django

### Install the required dependancies
```bash
pip install pymysql
pip install cryptography
```
### Replace default database settings with MySQL settings

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djangodb',
        'USER': 'djangouser',
        'PASSWORD': 'userpass',
        'HOST': 'localhost', 
        'PORT': '3306',
        'OPTIONS': {
'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
}
    }
}
```
### Update the ‘__init__.py’ file
```bash
import pymysql

pymysql.install_as_MySQLdb()
```

### Apply Database Migrations and create a superuser
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## Obtain an SSL Certificate with Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com www.yourdomain.com
```

## 403 Error in Django Admin
1. CSRF Token Issue - ensure to update a list of ALLOWED_HOSTS
```bash
ALLOWED_HOSTS = ['your-domain.com', 'your-server-ip', 'localhost']
```
2. CSRF Trusted Origins - Add a list of trusted Origins
```bash
CSRF_TRUSTED_ORIGINS = ['https://your-domain.com']
```
3. Static Files Setup - Ensure to collectstatic
```bash
python manage.py collectstatic
```
