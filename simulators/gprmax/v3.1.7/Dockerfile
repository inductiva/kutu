# Multi-stage Dockerfile for gprMax with MPI support
# ============================================
# Stage 1: Test environment setup
# ============================================
FROM python:3.11-slim AS test_env

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Download and prepare test files
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home

# Get input example
RUN curl -L https://storage.googleapis.com/inductiva-api-demo-files/gprmax-input-example.zip \
    --output /home/gprmax-input-example.zip \
    && unzip /home/gprmax-input-example.zip -d /home \
    && rm /home/gprmax-input-example.zip

# Copy test script
COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh


# ============================================
# Stage 2: Build gprMax
# ============================================
FROM python:3.11-slim AS build

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DEFAULT_TIMEOUT=120

# Install system dependencies including OpenMPI
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    git \
    make \
    libopenmpi-dev \
    openmpi-bin \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /opt

# Clone gprMax repository
RUN git clone https://github.com/gprMax/gprMax.git /opt/gprMax

# Change to gprMax directory
WORKDIR /opt/gprMax

# Install Python dependencies including mpi4py
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
    tqdm \
    mpi4py

# Install the python packages from /opt/gprMax/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Build and install gprMax
RUN python setup.py build && \
    python setup.py install


# ============================================
# Stage 3: Final runtime image
# ============================================
FROM python:3.11-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    OMPI_ALLOW_RUN_AS_ROOT=1 \
    OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1 \
    PRTE_ALLOW_RUN_AS_ROOT=1 \
    PRTE_ALLOW_RUN_AS_ROOT_CONFIRM=1

# Install only runtime MPI dependencies
RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y \
    openmpi-bin \
    libopenmpi40 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy built gprMax and Python packages from build stage
COPY --from=build /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/

# Copy test environment files
COPY --from=test_env /home /home

# Set working directory
WORKDIR /home

# Create directory for user models and outputs
RUN mkdir -p /home/input /home/output

# Default command - show help
CMD ["python", "-m", "gprMax", "-h"]