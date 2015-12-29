# How to contribute to letsmeet.click

## Important links and documents

* [Roadmap](https://github.com/letsmeet-click/meta/blob/master/roadmap.md)
* [Issues](https://github.com/letsmeet-click/letsmeet.click/issues)

## Feature requests

If you have an idea how to improve the service make sure to check our
roadmap and existing issues if there is already something planned for it.

If you can't find your suggestion please file an issue (see link above) and we will catch up with you when we have time.


## Coding

- if you work on something claim with [@<handle>] in the roadmap
- claim whole workpagage if reasonable
- set [✓] if sth is done
- everyone gets an invite to letsmeet-click.slack.com - ask @mfa or @asmaps

- as less code as feasible (KISS)
- no django-guardian. ownership/subscriptions by using fk and m2m tables, OLP with django-rules
- derive every model from `django_extensions.db.models import TimeStampedModel`! (created is important for KPIs)
- write tests(TM) for added functionality
