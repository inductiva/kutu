# Start from the simsopt base image.
FROM hiddensymmetries/simsopt

COPY ./requirements.txt /

# Install requirements
RUN /venv/bin/pip install -r requirements.txt

COPY ./scripts /scripts
