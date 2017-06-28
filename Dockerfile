FROM aexea/aexea-base:py3.6
MAINTAINER letsmeet.click Contributors

USER root

# install geo stuff
RUN apt-get update && apt-get install -y \
	binutils \
	gdal-bin \
	libproj-dev \
	&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt /opt/code/requirements.txt
WORKDIR /opt/code
RUN pip3 install --find-links=http://pypi.qax.io/wheels/ --trusted-host pypi.qax.io -Ur requirements.txt
COPY . /opt/code

RUN chown -R uid1000: /opt

WORKDIR /opt/code/letsmeet

# uid1000 is created in aexea-base
USER uid1000
EXPOSE 8011

# production stuff
ENTRYPOINT ["./start.sh"]
CMD ["web"]
