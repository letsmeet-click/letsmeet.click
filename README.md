# letsmeet.click

If you have a feature request please read
[CONTRIBUTING.md](https://github.com/letsmeet-click/letsmeet.click/blob/master/CONTRIBUTING.md)

This is most of the source-code you can find deployed on
[letsmeet.click](https://www.letsmeet.click/) except for the theme and
obviously our production settings 😉


[![Build Status](https://travis-ci.org/letsmeet-click/letsmeet.click.svg?branch=master)](https://travis-ci.org/letsmeet-click/letsmeet.click)

[![Code Issues](https://www.quantifiedcode.com/api/v1/project/11cf956b337f43abb2429dd08fbfe707/badge.svg)](https://www.quantifiedcode.com/app/project/11cf956b337f43abb2429dd08fbfe707)



## Timeframe

We developed the first version of letsmeet.click at #32c3 in Hamburg.
The plan for future features is here:
https://github.com/letsmeet-click/meta/blob/master/plan.md


## Development setup

letsmeet.click is a rather complex system esp. thanks to requiring PostGIS. To
make development easier it is highly recommended to use Docker in combination
with Docker-Compose to get up and running in finite amount of time:

```
docker-compose build
docker-compose run --rm web reset_db
docker-compose run --rm web migrate
docker-compose run --rm web createsuperuser
docker-compose up -d
```

Then head [here](http://localhost:8011/) to test your installation.

Use ``docker-compose logs`` for your debugging needs.

## Testing

In order to make the test setup easier, you can also execute them within the
Docker container:

```
docker-compose exec web tox
```

## Production setup

Mostly for us so that we don't forget 😊


### Starting/creating docker instances

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

# rebuild, update
./update.sh
```
