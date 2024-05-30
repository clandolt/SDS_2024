FROM codercom/code-server
# FROM condaforge/mambaforge
# FROM jupyter/datascience-notebook

ENV TZ=Europe/Zurich

USER root
## we use caddy as reverse proxy because it handles websockets automatically
RUN apt-get update && apt-get install -y build-essential curl less man python3 pip caddy
RUN mkdir -p /entrypoint.d && \
    chmod a+rwx /entrypoint.d && \
    chmod a+rw /etc/caddy/Caddyfile
USER coder

## the code-server base image starts all scripts mentioned in the env var ENTRYPOINTD (by default /entrypoint.d)
ADD .binder/entry-change-caddy.sh /entrypoint.d/

## configure here the parameters for the code-server startup as CMD
CMD [ "--app-name", "D Academy", "--disable-workspace-trust", "--disable-getting-started-override", "/home/coder/llm-profile-finder", "--auth", "none"] 

## Install Python Extension for code-server
RUN code-server --install-extension ms-python.python

## Install workshop specific packages

ADD --chown=coder:coder requirements.txt ./llm-profile-finder/
RUN pip install --break-system-packages -r ./llm-profile-finder/requirements.txt

ADD --chown=coder:coder * /workshop-notebooks/
ADD --chown=coder:coder . ./llm-profile-finder/

RUN ls -la /workshop-notebooks

# leave a marker for the date of the docker image in a writeable and later readable location
RUN date +'%F %T %Z' > .dockerimage-date

# docker build --platform linux/amd64 -t europe-west4-docker.pkg.dev/d-one-academy/d-academy/sds24/llm-profile-finder -f .binder/Dockerfile .
# docker push europe-west4-docker.pkg.dev/d-one-academy/d-academy/sds24/llm-profile-finder
## to run the image locally for development
# docker run --platform linux/amd64 --rm -p 8899:8888 --name coder europe-west4-docker.pkg.dev/d-one-academy/d-academy/sds24/llm-profile-finder
