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
    PYTHONDONTWRITEBYTECODE=1

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

# Pin the exact release so CI/local are identical
ARG GPRMAX_REF=v.3.1.7
RUN git clone --depth 1 --branch ${GPRMAX_REF} https://github.com/gprMax/gprMax.git /opt/gprMax

WORKDIR /opt/gprMax

RUN python -m pip install --no-cache-dir --upgrade pip setuptools wheel \
 && python -m pip install --no-cache-dir --retries 10 --timeout 120 \
      colorama cython h5py matplotlib numpy psutil scipy terminaltables tqdm mpi4py

# Build binaries
RUN python setup.py build

# Install gprMax
RUN python -m pip install --no-cache-dir --no-deps .


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