#!/bin/bash
echo '=> Start deploying...'
echo

echo '=> Pulling updates from the remote repository...'
git pull
echo '=> End pull.'
echo

echo '=> Syncing project files...'
rsync -a ./mysite/ "$WEBSITE_ROOT"
echo '=> End sync.'
echo

echo '=> Installing package dependencies...'
source "$WEBSITE_ROOT/venv/bin/activate"
python -m pip install -r requirements.txt
echo '=> End pip install.'
echo

echo '=> Running model migrations...'
python3 $WEBSITE_ROOT/manage.py migrate
echo '=> End Migration.'
echo

echo '=> Collecting static files into STATIC_ROOT...'
python3 $WEBSITE_ROOT/manage.py collectstatic --noinput --clear
echo '=> End collectstatic'
echo

echo '=> Restarting the website...'
devil www restart "$WEBSITE_HOST"
echo '=> End restart.'
echo

echo '=> End deploy.'
echo
