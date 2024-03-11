# Using the dolfinx/dolfinx base image for building our container.
FROM dolfinx/dolfinx:v0.6.0

# Set frontend to be noninteractive, to avoid prompts during installation.
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
	&& apt-get install -y python3 python3-pip
RUN ln -sf /usr/bin/python3 /usr/bin/python
RUN pip install -U setuptools

COPY ./requirements.txt /
RUN pip install -r /requirements.txt

COPY ./scripts /scripts
