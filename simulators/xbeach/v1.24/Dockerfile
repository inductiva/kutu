FROM inductiva/kutu:base-image_v0.1.0 as test_env

RUN wget https://storage.googleapis.com/inductiva-api-demo-files/xbeach-input-example.zip -P /home/ && \
	unzip /home/xbeach-input-example.zip -d /home/ && \
	rm /home/xbeach-input-example.zip

COPY ./test_sim.sh /home/test_sim.sh

RUN chmod +x /home/test_sim.sh

FROM inductiva/kutu:base-image_v0.1.0 as build

RUN apt update -qq && \
    apt install --no-install-recommends -y \
        subversion \
        python3 \
        python3-mako \
		netcdf-bin \
        libnetcdf-dev \
		libnetcdff-dev  && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    apt clean

RUN svn co https://svn.oss.deltares.nl/repos/xbeach/trunk@6082 /xbeach

WORKDIR /xbeach

RUN ./autogen.sh && \
	FCFLAGS=-I/usr/include ./configure --with-netcdf --with-mpi && \
	make && \
	make install && \
	make clean

ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

COPY --from=test_env /home /home
