cd /home/ubuntu/hydrafloodstool/hydrafloodviewer
git pull
source /home/ubuntu/hydrafloodstool/hydrafloods_env/bin/activate
python manage.py collectstatic
sudo systemctl daemon-reload
sudo systemctl restart gunicorn.socket gunicorn.service 
sudo nginx -t && sudo systemctl restart nginx
