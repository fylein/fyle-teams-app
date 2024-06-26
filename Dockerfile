FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

#================================================================
# pip install required modules
#================================================================

RUN pip install --upgrade setuptools pip
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

#==================================================
# Copy the latest code
#==================================================

RUN mkdir -p /fyle-teams-app
WORKDIR /fyle-teams-app
COPY . /fyle-teams-app

# Run pylint checks
# RUN pylint --rcfile=.pylintrc fyle_teams_app/

# Expose server port
EXPOSE 8000

CMD /bin/bash run.sh