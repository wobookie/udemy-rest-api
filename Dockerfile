FROM centos:8

# Read Arguments Required for the image build
ARG APP_DIR
ARG DJANGO_HOME
ARG APP_USER_NAME
ARG APP_USER_ID
ARG APP_USER_PASSWORD

# Set environment for Python
ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING utf-8
ENV DJANGO_HOME=${DJANGO_HOME}

# Install Python3, Postgres Client 10, Redis 5
RUN dnf -y install python3
RUN dnf -y install postgresql
RUN dnf -y install redis

# Install Nginx web server and set ownership to related directories
RUN dnf -y install nginx
RUN mkdir -p /var/cache/nginx /var/run/nginx
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
RUN chown -R nginx:nginx /etc/nginx && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /var/run/nginx && \
    chown -R nginx:nginx /var/lib/nginx && \
    chown -R nginx:nginx /usr/share/nginx
RUN chmod g+w /var/run/nginx

# Add some useful utilities and build dependencies
# required to install Python PostgreSQL driver (Psycopg2)
# These are temporary dependencies and removed after requirements installed
RUN dnf -y install sudo passwd openldap-clients \
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
# set a password for that user
# and grant sudo permissions to start / stop nginx
RUN useradd -ms /bin/bash -u ${APP_USER_ID} ${APP_USER_NAME} && \
    echo -e ${APP_USER_PASSWORD}'\n'${APP_USER_PASSWORD} | passwd ${APP_USER_NAME}

# Add application user to Nginx group
RUN usermod -a -G nginx ${APP_USER_NAME}

# Create directory structure for the web app
RUN mkdir -p ${APP_DIR}
RUN mkdir -p ${DJANGO_HOME}/logs

# Copy application
COPY ./naupy ${DJANGO_HOME}

# Make startserver.sh runable
RUN chown -R nautilus:nautilus ${APP_DIR}

# Workaround to start server - docker can't handle non-root directory as cmd entry points
COPY ./naupy/bin/startserver.sh /startserver.sh
RUN chmod +x /startserver.sh

# Set User to nautilus
USER ${APP_USER_NAME}

# Set the work directory
WORKDIR ${DJANGO_HOME}
