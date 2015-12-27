# letsmeet.click

## timeframe

We want to develop letsmeet.click at #32c3 in Hamburg.

For plan.md see: https://github.com/letsmeet-click/meta/blob/master/plan.md


## development setup

```
docker-compose build
docker-compose run web reset_db
docker-compose run web migrate
docker-compose run web createsuperuser
docker-compose up -d
```

### starting/creating docker instances

```
# database
docker run -d --restart=always -v /var/lib/postgres --name letsmeet-db mdillon/postgis:9.4

# home
docker run -d --name letsmeet-data aexea/aexea-base

# main image
docker build --tag=letsmeet-prod .
# reset database on first run
docker run --rm -ti --volumes-from letsmeet-data -v `pwd`/letsmeet/letsmeet/settings/production.py:/opt/code/letsmeet/letsmeet/settings/production.py --link letsmeet-db:db -e DJANGO_SETTINGS_MODULE=letsmeet.settings.production --entrypoint python3 letsmeet-prod manage.py reset_db
docker run --rm -ti --volumes-from letsmeet-data -v `pwd`/letsmeet/letsmeet/settings/production.py:/opt/code/letsmeet/letsmeet/settings/production.py --link letsmeet-db:db -e DJANGO_SETTINGS_MODULE=letsmeet.settings.production --entrypoint python3 letsmeet-prod manage.py migrate
docker run --rm -ti --volumes-from letsmeet-data -v `pwd`/letsmeet/letsmeet/settings/production.py:/opt/code/letsmeet/letsmeet/settings/production.py --link letsmeet-db:db -e DJANGO_SETTINGS_MODULE=letsmeet.settings.production --entrypoint python3 letsmeet-prod manage.py createsuperuser

### rebuild, update

./update.sh
```
