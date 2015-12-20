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
