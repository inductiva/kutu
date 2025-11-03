# Lightweight Docker container for gprMax (CPU-only)
# Based on Python slim image for minimal size

FROM python:3.11-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    OMP_NUM_THREADS=4

# Install system dependencies (gcc for OpenMP support)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    git \
    make \
    curl \
    zip \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /opt

# Clone gprMax repository
RUN git clone https://github.com/gprMax/gprMax.git /opt/gprMax

# Change to gprMax directory
WORKDIR /opt/gprMax

# Install Python dependencies
# Using pip instead of conda for a lighter image
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    colorama \
    cython \
    h5py \
    matplotlib \
    numpy \
    psutil \
    scipy \
    terminaltables \
    tqdm

    # Build and install gprMax
RUN python setup.py build && \
    python setup.py install

    
# Set the working directory for running models
WORKDIR /home

# Create directory for user models and outputs
RUN mkdir -p /home/input /home/output

# Get input example
RUN curl -L https://storage.googleapis.com/inductiva-api-demo-files/gprmax-input-example.zip \
    --output /home/gprmax-input-example.zip \
    && mkdir -p /home/gprmax-input-example \
    && unzip /home/gprmax-input-example.zip -d /home/gprmax-input-example \
    && rm /home/gprmax-input-example.zip


COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

# Default command - show help
CMD ["python", "-m", "gprMax", "-h"]
