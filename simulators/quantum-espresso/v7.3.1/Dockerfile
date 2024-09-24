FROM inductiva/kutu:base-image_v0.1.1 as test_env

RUN wget https://storage.googleapis.com/inductiva-api-demo-files/qe-input-example.zip -P /home/ && \
    unzip /home/qe-input-example.zip -d /home/ && \
    rm /home/qe-input-example.zip

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

FROM inductiva/kutu:base-image_v0.1.1 as build

RUN wget https://gitlab.com/QEF/q-e/-/archive/qe-7.3.1/q-e-qe-7.3.1.zip && \
    unzip q-e-qe-7.3.1.zip && \
    rm q-e-qe-7.3.1.zip && \
    cd q-e-qe-7.3.1 && \
    ./configure --prefix="/qe-mpi" && \
    make all && \
    make install && \
    make clean && \
    ./configure --prefix="/qe-openmp" --enable-openmp --disable-parallel && \
    make all && \
    make install && \
    for file in /qe-openmp/bin/*; do mv "$file" "${file%.*}_openmp.${file##*.}"; done && \
    mkdir /root/espresso && \
    cd test-suite && \
    make pseudo && \
    cp -r /q-e-qe-7.3.1/pseudo/ /root/espresso/pseudo/


FROM inductiva/kutu:base-image_v0.1.1

COPY --from=build /qe-openmp /qe-openmp
COPY --from=build /qe-mpi /qe-mpi
COPY --from=build /root/espresso /home/executer-tracker/espresso
COPY --from=build /root/espresso /root/espresso

ENV PATH="$PATH:/qe-openmp/bin:/qe-mpi/bin"
ENV OPENBLAS_NUM_THREADS=1

COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /lib/x86_64-linux-gnu/libz.so.1 /lib/x86_64-linux-gnu/libz.so.1
COPY --from=build /lib/x86_64-linux-gnu/libgomp.so.1 /lib/x86_64-linux-gnu/libgomp.so.1
COPY --from=build /lib/x86_64-linux-gnu/libmpi.so.40 /lib/x86_64-linux-gnu/libmpi.so.40
COPY --from=build /lib/x86_64-linux-gnu/libmvec.so.1 /lib/x86_64-linux-gnu/libmvec.so.1
COPY --from=build /lib/x86_64-linux-gnu/libudev.so.1 /lib/x86_64-linux-gnu/libudev.so.1
COPY --from=build /lib/x86_64-linux-gnu/libfftw3.so.3 /lib/x86_64-linux-gnu/libfftw3.so.3
COPY --from=build /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=build /lib/x86_64-linux-gnu/libhwloc.so.15 /lib/x86_64-linux-gnu/libhwloc.so.15
COPY --from=build /lib/x86_64-linux-gnu/libgfortran.so.5 /lib/x86_64-linux-gnu/libgfortran.so.5
COPY --from=build /lib/x86_64-linux-gnu/libopenblas.so.0 /lib/x86_64-linux-gnu/libopenblas.so.0
COPY --from=build /lib/x86_64-linux-gnu/libquadmath.so.0 /lib/x86_64-linux-gnu/libquadmath.so.0
COPY --from=build /lib/x86_64-linux-gnu/libfftw3_omp.so.3 /lib/x86_64-linux-gnu/libfftw3_omp.so.3
COPY --from=build /lib/x86_64-linux-gnu/libopen-pal.so.40 /lib/x86_64-linux-gnu/libopen-pal.so.40
COPY --from=build /lib/x86_64-linux-gnu/libopen-rte.so.40 /lib/x86_64-linux-gnu/libopen-rte.so.40
COPY --from=build /lib/x86_64-linux-gnu/libmpi_mpifh.so.40 /lib/x86_64-linux-gnu/libmpi_mpifh.so.40
COPY --from=build /lib/x86_64-linux-gnu/libevent_core-2.1.so.7 /lib/x86_64-linux-gnu/libevent_core-2.1.so.7
COPY --from=build /lib/x86_64-linux-gnu/libevent_pthreads-2.1.so.7 /lib/x86_64-linux-gnu/libevent_pthreads-2.1.so.7

COPY --from=test_env /home /home