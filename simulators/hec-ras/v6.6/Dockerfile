FROM inductiva/kutu:base-image_v0.1.0 as test_env

# Download and unzip
RUN wget https://www.hec.usace.army.mil/software/hec-ras/downloads/Linux_RAS_v66.zip -O /tmp/Linux_RAS_v66.zip && \
    unzip /tmp/Linux_RAS_v66.zip -d /tmp/hec-ras && \
    rm /tmp/Linux_RAS_v66.zip

# Move binaries to PATH
RUN cp /tmp/hec-ras/Linux_RAS_v66/bin/* /bin/ && chmod +x /bin/* && \
    rm -rf /tmp/hec-ras
