#!/bin/bash

echo "Start ssh agent"
eval `ssh-agent`
ssh-add

## Deployment

echo "Create destination folder"
ssh root@pipeto.me 'mkdir /root/data/youtube-dl'

echo "Make sure that python is installed"
ssh root@pipeto.me 'apt-get install -y python3-venv'

echo "Copying files"
scp -r ./app root@pipeto.me:/root/data/youtube-dl

echo "Setup key"
ssh root@pipeto.me 'printf "SECRET_KEY=" > /root/data/youtube-dl/app/.env'
ssh root@pipeto.me 'tr -dc "a-zA-Z0-9" < /dev/urandom | head -c 25 >> /root/data/youtube-dl/app/.env'

echo "Setup venv"
ssh root@pipeto.me 'python3 -m venv /root/data/youtube-dl/venv'
ssh root@pipeto.me '/root/data/youtube-dl/venv/bin/pip3 install -r /root/data/youtube-dl/app/requirements.txt'

### Service

echo "Copy service definition"
scp ./scripts/youtube-dl.service root@pipeto.me:/lib/systemd/system/youtube-dl.service
ssh root@pipeto.me 'systemctl daemon-reload'

echo "Start service"
ssh root@pipeto.me 'systemctl start youtube-dl'

echo "Enable service on boot"
ssh root@pipeto.me 'systemctl enable youtube-dl'

echo "Check service status"
ssh root@pipeto.me 'systemctl status youtube-dl'

### Nginx

# echo "Make sure that nginx is installed"
# ssh root@pipeto.me 'apt-get install -y nginx'

echo "Copy nginx config"
scp ./scripts/youtube-dl.nginx.conf root@pipeto.me:/etc/nginx/sites-available/youtube-dl.nginx.conf

echo "Enable the nginx"
ssh root@pipeto.me 'ln -s /etc/nginx/sites-available/youtube-dl.nginx.conf /etc/nginx/sites-enabled/youtube-dl.nginx.conf'

echo "Restart nginx to pick up the changes"
ssh root@pipeto.me 'systemctl restart nginx'

### Nginx Https

# echo "Install letsencrypt client"
# ssh root@pipeto.me 'add-apt-repository ppa:certbot/certbot'
# ssh root@pipeto.me 'apt-get install python-certbot-nginx'

echo "Generate and install certificate"
ssh root@pipeto.me 'certbot --nginx -d youtube.pipeto.me'


echo "Stop ssh agent"
killall ssh-agent