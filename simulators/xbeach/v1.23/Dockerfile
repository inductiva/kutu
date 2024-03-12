FROM library/centos:7 as builder
RUN yum update -y && \
	yum install epel-release -y

RUN	yum install -y gcc \
	hdf5-devel \
	libtool \
	make \
	netcdf-devel \
	netcdf-fortran \
	netcdf-fortran-devel \
	openmpi-devel \
	git \
	python-mako

ENV PATH=/usr/lib64/openmpi/bin:$PATH \
	LD_LIBRARY_PATH=/usr/lib64/openmpi/lib:$LD_LIBRARY_PATH

RUN git clone https://github.com/openearth/xbeach.git /xbeach

WORKDIR /xbeach

RUN ./autogen.sh && \
	FCFLAGS=-I/usr/lib64/gfortran/modules ./configure --with-netcdf --without-mpi && \
	make clean && \
	make && \
	make install

FROM library/centos:7

RUN yum update -y && \
	yum install epel-release -y && \
	yum install -y \
	gcc \
	geos \
	make \
	perl-core \
	pcre-devel \
	bzip2-devel \
	libffi-devel \
	zlib-devel \
	xz-devel \
	netcdf-fortran-openmpi \
	netcdf-fortran \
	git \
	openmpi \
	wget \
	&&  yum clean all

# Install openssl 1.1.1, needed for Python 3.10
# Install instructions from:
#  - https://gist.github.com/Bill-tran/5e2ab062a9028bf693c934146249e68c
RUN wget https://ftp.openssl.org/source/openssl-1.1.1k.tar.gz && \
	tar -xzf openssl-1.1.1k.tar.gz

WORKDIR /openssl-1.1.1k
RUN ./config --prefix=/usr --openssldir=/etc/ssl --libdir=lib no-shared zlib-dynamic
RUN make && make install
ENV LD_LIBRARY_PATH=/usr/local/lib:/usr/local/lib64:$LD_LIBRARY_PATH

ENV PATH=/usr/lib64/openmpi/bin:$PATH \
	LD_LIBRARY_PATH=/usr/lib64/openmpi/lib:$LD_LIBRARY_PATH

ENV MPIRUN_BIN=mpirun
ENV XBEACH_BIN=xbeach

COPY --from=builder /usr/local/ /usr/local/
