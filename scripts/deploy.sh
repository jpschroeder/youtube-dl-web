#!/bin/bash

echo "Start ssh agent"
eval `ssh-agent`
ssh-add

echo "Stop service"
ssh root@pipeto.me 'systemctl stop youtube-dl'

echo "Copying files"
scp -r ./app root@pipeto.me:/root/data/youtube-dl

echo "Start service"
ssh root@pipeto.me 'systemctl start youtube-dl'

echo "Stop ssh agent"
killall ssh-agent