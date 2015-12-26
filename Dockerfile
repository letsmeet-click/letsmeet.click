FROM aexea/aexea-base
MAINTAINER letsmeet.click Contributors

USER root

# install uwsgi for production
RUN pip3 install uwsgi

ADD requirements.txt /opt/code/requirements.txt
WORKDIR /opt/code
RUN pip3 install --find-links=http://pypi.qax.io/wheels/ --trusted-host pypi.qax.io -Ur requirements.txt
ADD . /opt/code

RUN chown -R uid1000: /opt

WORKDIR /opt/code/letsmeet

# uid1000 is created in aexea-base
USER uid1000
EXPOSE 8011

# production stuff
ENTRYPOINT ["./start.sh"]
CMD ["web"]
