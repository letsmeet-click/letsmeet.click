#!/bin/sh

set -e

git pull
docker build --tag=letsmeet-prod .
docker rm -f letsmeet letsmeet-nginx
docker run -d --volumes-from letsmeet-data --link letsmeet-db:db -v `pwd`/letsmeet/letsmeet/settings/production.py:/opt/code/letsmeet/letsmeet/settings/production.py --restart=always --name letsmeet letsmeet-prod
docker run --name letsmeet-nginx --net="host" --volumes-from letsmeet-data -v `pwd`/nginx.conf:/etc/nginx/nginx.conf --restart=always -d nginx

echo "Cleaning up old docker images..."
docker rmi $(docker images | grep "<none>" | awk '{print($3)}')
