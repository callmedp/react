# careerplus

# Os Setup

sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install -y python3-pip
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev libmysqlclient-dev
sudo apt-get install libcairo2-dev
sudo apt-get install python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0.0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

sudo pip3 install virtualenv

# Env Setup
virtualenv careerplus
pip3 install geoip
pip3 install -r requirements/common.txt
sudo apt-get install mysql-server
## Take dump from staging
SQL collate error fix:
ALTER DATABASE careerplus CHARACTER SET utf8 COLLATE utf8_general_ci;

SELECT CONCAT('ALTER TABLE ', a.table_name, ' CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;') FROM information_schema.tables a WHERE a.table_schema = 'careerplus';

Copy queries and run

make entry in hosts files
172.22.67.111 sumosc.shine.com sumosc1.shine.com
172.22.65.64 recruiter.shine.com
172.22.65.140 www.shine.com


# Install redis
apt-get install redis-server
https://www.rosehosting.com/blog/how-to-install-configure-and-use-redis-on-ubuntu-16-04/

## install redis
sudo apt-get install ruby-full
sudo gem install sass

### Prod
mkdir /etc/uwsgi/
mkdir /etc/uwsgi/apps-available/
create uwsgi files
mkdir /etc/uwsgi/vassals
sudo ln -s /etc/uwsgi/apps-available/careerplus.ini /etc/uwsgi/vassals/
uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data

### Staging
Add access to Mysql
https://stackoverflow.com/questions/19101243/error-1130-hy000-host-is-not-allowed-to-connect-to-this-mysql-server

CREATE USER 'root'@'10.24.8.130';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'10.24.8.130' IDENTIFIED BY 'root';

## Prod -- change fa and skill in shell
upload_Skill('/tmp/Courses-Skill.csv')
upload_FA('/tmp/Courses-FA.csv')

# Prod Setup crons
apt-get install cron
cd /opt/
mkdir crons
cd crons
mkdir logs
# create cron scripts daily/weekly/etc
crontab -e

# Prod start a screen for celery
cd /code/careerplus
workon careerplus
celery multi restart w1 -A careerplus -l debug --logfile=/var/log/celery/w1.log --pidfile=/var/log/celery/w1.pid
#upload skills and FA
scp '/path-to/Courses-FA.csv' vijay1@172.22.65.33:/tmp/
scp '/path-to/Courses-Skill.csv' vijay1@172.22.65.33:/tmp/















