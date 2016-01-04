# About

DJPanel (Django Control Panel) is Django-based software for easy control projects and servers.
In the past I controled everything via sublime plugins which parsed a lot of different config files across file system and it was a bit messy.

Now, everything is well structured in one single place - Django admin. All external software (Sublime plugins, GoLang programs) get information by API that is powered by Django Rest Framework.

# Features

Manipulation all information in Django admin. These are:

1. Servers
2. Projects
3. Countries
4. Providers
5. Ip addresses
6. Databases
7. Users
8. All configs for servers and projects.

Server auto installation available for Debian 8 via [GoLang program](https://github.com/vladgr/DCPanel-golang).
Following software can be installed and configured automatically:

1. IPTables
2. MySQL
3. Nginx
4. PHP (not much tested - just works)
5. Postfix (not much tested)
6. PostgreSQL
7. Python2
8. Python3
9. Redis
10. Supervisor
11. Squid

There are several types of projects: Django, GoLang, Python, PHP, HTML. 
The main projects are Django, GoLang and Python. Support for PHP and HTML I added just for a few projects that I made before 2010. 

The most convenient place for me to execute control commands is Sublime. So, Django admin is for creating and editing information.
And [Sublime3 plugins](https://github.com/vladgr/DCPanel-sublime) for executing commands.

## Sublime functions:

* MySQL databases
  * View databases.
  * Create database on remote host.
  * Download database from remote host to localhost.
  * Upload database from localhost to remote host.
* Servers
  * View servers.
  * Create SSH keys.
  * Create user on remote host.
  * View some logs.  
* Projects.
    * View projects.
    * Deploy project to remote host.
    * Create virtualenv on localhost for Django project.
    * Open file of any project by partial name.

My working PC is on Ubuntu. A lot of functions work via calling gnome terminal from Sublime plugins.
So, most of Sublime staff will work for you if you are on Linux too, otherwise you'll need to rewrite some functional.

If you need autoinstall for servers via GoLang program - use the same name on localhost and remote hosts.
For example, if your main local user john (/home/john/) use the same on remote hosts or rewrite functional for yourself.

# Installation

Actually, everything works on localhost on Django embedded (development) server and it works fast.
So, you can just install only development environment (for convenience I use autorun on tty1).

Install virtual environment. (panel/panel/requirements/)
Create migrations and install fixtures with examples (especially useful for configs.)

```
python manage.py makemigrations
python manage.py makemigrations api
python manage.py migrate

python manage.py loaddata setting.xml
python manage.py loaddata country.xml
python manage.py loaddata provider.xml
python manage.py loaddata server.xml
python manage.py loaddata project.xml
python manage.py loaddata db.xml
python manage.py loaddata user.xml
python manage.py loaddata ip.xml
python manage.py loaddata install.xml
python manage.py loaddata conf.xml
python manage.py loaddata postfix.xml

python manage.py createsuperuser
```

## Set environment variables or edit settings/base.py

* PANEL_SECRET_KEY  (Django's SECRET_KEY)
* PANEL_CRYPT_KEY   (length 16 - crypting passwords)
* PANEL_CRYPT_IV    (length 16 - crypting passwords)

# Database

I use sqlite to store all data. Since, there is no need for concurrent access, it works just fine!
Note: passwords stored crypted in database, but they are available decrypted in the API.

# Recommended Django project's structure in local file system.

projname/
  |--project/
     |--projname/
        |--appname/ (or apps)
        |--projname/
           |--requirements/
              |--development.txt
              |--production.txt
           |--settings/
              |--base.py
              |--development.py
              |--production.py
        |--manage.py

     |--static/
        |--files/
           |--js/
           |--media/
           |--pics/
           |--css/


# Conclusion.
I use these panel in production for myself. It saves me a lot of time and it is much more convenient than using tools like ansible e.t.c. I considered using Docker for each project, but for most of the projects Docker is overhead. For Django sites: virtual environment, nginx, uwsgi, supervisor and database is enough in most cases. 

May be panel has some specific features that you don't need. And it is not intended to cover everything.
It is just cover my specific requirements. So, use it "as is" or just clone and rewrite anything that you need.




