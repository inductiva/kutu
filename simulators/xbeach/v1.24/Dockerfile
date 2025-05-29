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

FROM ubuntu:22.04

RUN apt update -qq && \
    apt install -y \
        openmpi-bin=4.1.2-2ubuntu1 && \
    apt clean

ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

COPY --from=build /usr/local/bin/xbeach /usr/local/bin/xbeach

COPY --from=build /lib/x86_64-linux-gnu/libevent_pthreads-2.1.so.7 /lib/x86_64-linux-gnu/libevent_pthreads-2.1.so.7
COPY --from=build /lib/x86_64-linux-gnu/libhdf5_serial_hl.so.100 /lib/x86_64-linux-gnu/libhdf5_serial_hl.so.100
COPY --from=build /lib/x86_64-linux-gnu/libevent_core-2.1.so.7 /lib/x86_64-linux-gnu/libevent_core-2.1.so.7
COPY --from=build /lib/x86_64-linux-gnu/libhdf5_serial.so.103 /lib/x86_64-linux-gnu/libhdf5_serial.so.103
COPY --from=build /lib/x86_64-linux-gnu/libbrotlicommon.so.1 /lib/x86_64-linux-gnu/libbrotlicommon.so.1
COPY --from=build /lib/x86_64-linux-gnu/libkrb5support.so.0 /lib/x86_64-linux-gnu/libkrb5support.so.0
COPY --from=build /lib/x86_64-linux-gnu/libgssapi_krb5.so.2 /lib/x86_64-linux-gnu/libgssapi_krb5.so.2
COPY --from=build /lib/x86_64-linux-gnu/libmpi_mpifh.so.40 /lib/x86_64-linux-gnu/libmpi_mpifh.so.40
COPY --from=build /lib/x86_64-linux-gnu/libunistring.so.2 /lib/x86_64-linux-gnu/libunistring.so.2
COPY --from=build /lib/x86_64-linux-gnu/libopen-rte.so.40 /lib/x86_64-linux-gnu/libopen-rte.so.40
COPY --from=build /lib/x86_64-linux-gnu/libopen-pal.so.40 /lib/x86_64-linux-gnu/libopen-pal.so.40
COPY --from=build /lib/x86_64-linux-gnu/libbrotlidec.so.1 /lib/x86_64-linux-gnu/libbrotlidec.so.1
COPY --from=build /lib/x86_64-linux-gnu/libquadmath.so.0 /lib/x86_64-linux-gnu/libquadmath.so.0
COPY --from=build /lib/x86_64-linux-gnu/libnghttp2.so.14 /lib/x86_64-linux-gnu/libnghttp2.so.14
COPY --from=build /lib/x86_64-linux-gnu/libldap-2.5.so.0 /lib/x86_64-linux-gnu/libldap-2.5.so.0
COPY --from=build /lib/x86_64-linux-gnu/liblber-2.5.so.0 /lib/x86_64-linux-gnu/liblber-2.5.so.0
COPY --from=build /lib/x86_64-linux-gnu/libkeyutils.so.1 /lib/x86_64-linux-gnu/libkeyutils.so.1
COPY --from=build /lib/x86_64-linux-gnu/libk5crypto.so.3 /lib/x86_64-linux-gnu/libk5crypto.so.3
COPY --from=build /lib/x86_64-linux-gnu/libgfortran.so.5 /lib/x86_64-linux-gnu/libgfortran.so.5
COPY --from=build /lib/x86_64-linux-gnu/libp11-kit.so.0 /lib/x86_64-linux-gnu/libp11-kit.so.0
COPY --from=build /lib/x86_64-linux-gnu/libnetcdff.so.7 /lib/x86_64-linux-gnu/libnetcdff.so.7
COPY --from=build /lib/x86_64-linux-gnu/libnetcdf.so.19 /lib/x86_64-linux-gnu/libnetcdf.so.19
COPY --from=build /lib/x86_64-linux-gnu/libhogweed.so.6 /lib/x86_64-linux-gnu/libhogweed.so.6
COPY --from=build /lib/x86_64-linux-gnu/libgnutls.so.30 /lib/x86_64-linux-gnu/libgnutls.so.30
COPY --from=build /lib/x86_64-linux-gnu/libcom_err.so.2 /lib/x86_64-linux-gnu/libcom_err.so.2
COPY --from=build /lib/x86_64-linux-gnu/libresolv.so.2 /lib/x86_64-linux-gnu/libresolv.so.2
COPY --from=build /lib/x86_64-linux-gnu/libnettle.so.8 /lib/x86_64-linux-gnu/libnettle.so.8
COPY --from=build /lib/x86_64-linux-gnu/libhwloc.so.15 /lib/x86_64-linux-gnu/libhwloc.so.15
COPY --from=build /lib/x86_64-linux-gnu/libcrypto.so.3 /lib/x86_64-linux-gnu/libcrypto.so.3
COPY --from=build /lib/x86_64-linux-gnu/libtasn1.so.6 /lib/x86_64-linux-gnu/libtasn1.so.6
COPY --from=build /lib/x86_64-linux-gnu/libsasl2.so.2 /lib/x86_64-linux-gnu/libsasl2.so.2
COPY --from=build /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=build /lib/x86_64-linux-gnu/libzstd.so.1 /lib/x86_64-linux-gnu/libzstd.so.1
COPY --from=build /lib/x86_64-linux-gnu/libudev.so.1 /lib/x86_64-linux-gnu/libudev.so.1
COPY --from=build /lib/x86_64-linux-gnu/librtmp.so.1 /lib/x86_64-linux-gnu/librtmp.so.1
COPY --from=build /lib/x86_64-linux-gnu/libmpi.so.40 /lib/x86_64-linux-gnu/libmpi.so.40
COPY --from=build /lib/x86_64-linux-gnu/libkrb5.so.3 /lib/x86_64-linux-gnu/libkrb5.so.3
COPY --from=build /lib/x86_64-linux-gnu/libidn2.so.0 /lib/x86_64-linux-gnu/libidn2.so.0
COPY --from=build /lib/x86_64-linux-gnu/libgmp.so.10 /lib/x86_64-linux-gnu/libgmp.so.10
COPY --from=build /lib/x86_64-linux-gnu/libcurl.so.4 /lib/x86_64-linux-gnu/libcurl.so.4
COPY --from=build /lib/x86_64-linux-gnu/libssl.so.3 /lib/x86_64-linux-gnu/libssl.so.3
COPY --from=build /lib/x86_64-linux-gnu/libssh.so.4 /lib/x86_64-linux-gnu/libssh.so.4
COPY --from=build /lib/x86_64-linux-gnu/libpsl.so.5 /lib/x86_64-linux-gnu/libpsl.so.5
COPY --from=build /lib/x86_64-linux-gnu/libffi.so.8 /lib/x86_64-linux-gnu/libffi.so.8
COPY --from=build /lib/x86_64-linux-gnu/libaec.so.0 /lib/x86_64-linux-gnu/libaec.so.0
COPY --from=build /lib/x86_64-linux-gnu/libsz.so.2 /lib/x86_64-linux-gnu/libsz.so.2
COPY --from=build /lib/x86_64-linux-gnu/libz.so.1 /lib/x86_64-linux-gnu/libz.so.1
COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /usr/local/lib/libxbeach.so.0 /usr/local/lib/libxbeach.so.0
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2

COPY --from=test_env /home /home

COPY ../xbeach_animator /opt/xbeach_animator

# 4) Install Python deps
WORKDIR /opt/xbeach_animator
RUN pip3 install --no-cache-dir -r requirements.txt

# 5) Expose a CLI shim
RUN chmod +x xbeach_animator.py \
 && ln -s /opt/xbeach_animator/xbeach_animator.py /usr/local/bin/xbeach_animator

WORKDIR /
