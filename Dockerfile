FROM centos:8

# Read Arguments Required for the image build
ARG APP_DIR
ARG DJANGO_HOME

# Set environment for Python
ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING utf-8
ENV DJANGO_HOME=${DJANGO_HOME}

# Install Python3, Postgres Client 10 and Redis 5
RUN dnf -y install python3
RUN dnf -y install postgresql
RUN dnf -y install redis

# Add some useful utilities and build dependencies
# required to install Python PostgreSQL driver (Psycopg2)
# These are temporary dependencies and removed after requirements installed
RUN dnf -y install sudo openldap-clients \
    gcc postgresql-devel python3-devel

# Install application dependencies
COPY ./requirements.txt requirements.txt

# Upgrade PIP to latest version
RUN pip3 install --upgrade pip

# Install Gunicorn
RUN pip3 install --upgrade gunicorn

RUN pip3 install -r requirements.txt && \
    rm requirements.txt

# Clean Up installations
RUN dnf -y remove gcc postgresql-devel python3-devel && \
    dnf clean all && \
    rm -f /etc/yum.repos.d/*.rpm; rm -fr /var/cache/*

# PyCharm expect to find the python command in the system path
# So we set the default Python Version (Unversioned Python Command)
RUN alternatives --set python /usr/bin/python3

# Add an user under which the application should run
# and grant him sudo permissions
RUN useradd -ms /bin/bash nautilus && \
    usermod -aG wheel,nautilus nautilus && \
    echo 'nautilus ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

# Create directory structure for the web app
RUN mkdir -p ${APP_DIR}
RUN mkdir -p ${DJANGO_HOME}/logs
RUN mkdir -p ${DJANGO_HOME}/www/static
COPY ./naupy ${DJANGO_HOME}

# Make startserver.sh runable
RUN chown -R nautilus:nautilus ${APP_DIR}

# Workaround to start server - docker can't handle non-root directory as cmd entry points
COPY ./naupy/bin/startserver.sh /startserver.sh
RUN chmod +x /startserver.sh

# Set User to nautilus
USER nautilus

# Set the work directory
WORKDIR ${DJANGO_HOME}
