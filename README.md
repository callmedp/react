# careerplus

# Os Setup

sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install -y python3-pip
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev libmysqlclient-dev
sudo pip3 install virtualenv virtualenvwrapper
cp ~/.bashrc ~/.bashrc-org
printf '\n%s\n%s\n%s' '# virtualenv' 'export WORKON_HOME=~/virtualenvs' 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc
source ~/.bashrc

# Env Setup

mkvirtualenv careerplus
pip install geoip
pip3 install -r requirements/common.txt
sudo apt-get install mysql-server
mkdir /etc/uwsgi/
mkdir /etc/uwsgi/vassals
sudo ln -s /path/to/your/mysite/mysite_uwsgi.ini /etc/uwsgi/vassals/
uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data

# Data Setup
python manage.py makemigrations
python manage,py makemigrations thumbnails
python manage.py migrate


SQL collate error fix:
ALTER DATABASE careerplus CHARACTER SET utf8 COLLATE utf8_general_ci;

SELECT CONCAT('ALTER TABLE ', a.table_name, ' CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;') FROM information_schema.tables a WHERE a.table_schema = 'careerplus';

Copy queries and run

# Fixtures
# python manage.py cities_light
python manage.py loaddata pdata.json
python manage.py loaddata shop.json
python manage.py loaddata blog.json
python manage.py loaddata mdata.json
python manage.py loaddata geolocation.json
python manage.py loaddata shopdata.json

make entry in hosts files
172.22.67.111 sumosc.shine.com sumosc1.shine.com
172.22.65.64 recruiter.shine.com
172.22.65.140 www.shine.com

