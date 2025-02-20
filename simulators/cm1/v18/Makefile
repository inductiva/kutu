
#SHELL = /bin/csh

#-----------------------------------------------------------------------------
#                      NETCDF SECTION
#  (uncomment the following four lines if you want netcdf output capability)
#   (also, make sure the paths to netcdf files are correct for your machine)
#              (NOTE: Don't change lines 3 and 4!)
#  Note:  you may need to remove -DNCFPLUS if you use an old version of netcdf
#
OUTPUTINC = -I/usr/include
OUTPUTLIB = -L/usr/lib/x86_64-linux-gnu
OUTPUTOPT = -DNETCDF -DNCFPLUS
LINKOPTS  = -lnetcdf -lnetcdff
#-----------------------------------------------------------------------------
#                         HDF SECTION
#              NEW for cm1r15:  CM1 now supports HDF5
#  (uncomment the following four lines if you want hdf output capability)
#   (also, make sure the paths to hdf files are correct for your machine)
#              (NOTE: Don't change lines 3 and 4!)
# Note: You may need to remove -lsz.
#
#OUTPUTINC = -I/usr/local/hdf5/include
#OUTPUTLIB = -L/usr/local/hdf5/lib -L/usr/local/szip/lib
#OUTPUTOPT = -DHDFOUT
#LINKOPTS  = -lhdf5hl_fortran -lhdf5_hl -lhdf5_fortran -lhdf5 -lsz -lz -lm
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
#                     HARDWARE SECTION
#-- Choose the appropriate architecture, and uncomment all lines 
#-- in that section.  See "README.compile" for more information.
#-----------------------------------------------------------------------------
#  single processor, Intel compiler 
#      (eg, NCAR's yellowstone/caldera)
#FC   = ifort
#OPTS = -I../include -O3 -xHost -ip -assume byterecl -fp-model precise -ftz
#CPP  = cpp -C -P -traditional -Wno-invalid-pp-token
#-----------------------------------------------------------------------------
#  multiple processors, distributed memory (MPI), Intel compiler 
#      (eg, NCAR's yellowstone)
#FC   = mpif90
#OPTS = -I../include -O3 -xHost -ip -assume byterecl -fp-model precise -ftz
#CPP  = cpp -C -P -traditional -Wno-invalid-pp-token
#DM   = -DMPI
#-----------------------------------------------------------------------------
#  multiple processors, shared memory (OpenMP), Intel compiler 
#      (eg, NCAR's yellowstone)
#FC   = mpif90
#OPTS = -I../include -O3 -xHost -ip -assume byterecl -fp-model precise -ftz -openmp
#CPP  = cpp -C -P -traditional -Wno-invalid-pp-token
#-----------------------------------------------------------------------------
#  single processor, Portland Group compiler
#FC   = pgf90
#OPTS = -Mfree -I../include -O2 -Ktrap=none
#CPP  = cpp -C -P -traditional -Wno-invalid-pp-token
#-----------------------------------------------------------------------------
#  multiple processors, distributed memory (MPI), Portland Group compiler
#FC   = mpif90
#OPTS = -Mfree -I../include -O2 -Ktrap=none
#CPP  = cpp -C -P -traditional -Wno-invalid-pp-token
#DM   = -DMPI
#-----------------------------------------------------------------------------
#  multiple processors, shared memory (OpenMP), Portland Group compiler
#FC   = pgf90
#OPTS = -Mfree -I../include -O2 -Ktrap=none -mp
#CPP  = cpp -C -P -traditional -Wno-invalid-pp-token
#-----------------------------------------------------------------------------
#  single processor, Portland Group compiler, double precision
#FC   = pgf90
#OPTS = -Mfree -I../include -O2 -Ktrap=none -r8
#CPP  = cpp -C -P -traditional -Wno-invalid-pp-token
#DP   = -DDP
#-----------------------------------------------------------------------------
#  multiple processors, shared memory (OpenMP), Portland Group compiler, double precision
#FC   = pgf90
#OPTS = -Mfree -I../include -O2 -Ktrap=none -r8 -mp
#CPP  = cpp -C -P -traditional -Wno-invalid-pp-token
#DP   = -DDP
#-----------------------------------------------------------------------------
#  single processor, Cray fortran compiler
#      (eg, NCSA's bluewaters)
#  Remember to enter this on command line first:  module load libfast
#      (or, comment-out the "-lfast_mv" line below)
#FC   = ftn
#OPTS = -I../include -O3 -Ovector3 -Oscalar3 -Othread3 -h noomp
#LINKOPTS = -lfast_mv
#CPP  = cpp -C -P -traditional
#-----------------------------------------------------------------------------
#  multiple processors, distributed memory (MPI), Cray fortran compiler
#      (eg, NCSA's bluewaters)
#  Remember to enter this on command line first:  module load libfast
#      (or, comment-out the "-lfast_mv" line below)
#FC   = ftn
#OPTS = -I../include -O3 -Ovector3 -Oscalar3 -Othread3 -h noomp
#LINKOPTS = -lfast_mv
#CPP  = cpp -C -P -traditional
#DM   = -DMPI
#-----------------------------------------------------------------------------
#  multiple processors, shared memory (OpenMP), Cray fortran compiler
#      (eg, NCSA's bluewaters)
#  Remember to enter this on command line first:  module load libfast
#      (or, comment-out the "-lfast_mv" line below)
#FC   = ftn
#OPTS = -I../include -O3 -Ovector3 -Oscalar3 -Othread3 -h omp
#LINKOPTS = -lfast_mv
#CPP  = cpp -C -P -traditional
#DM   = -DMPI
#-----------------------------------------------------------------------------
#  single processor, gnu compiler
#FC   = gfortran
#OPTS = -ffree-form -ffree-line-length-none -I../include -O2
#CPP  = cpp -C -P -traditional -Wno-invalid-pp-token
#-----------------------------------------------------------------------------
#  multiple processors, distributed memory (MPI), gnu compiler
FC = mpif90
OPTS = -ffree-form -ffree-line-length-none -ffixed-form -I../include -O2
CPP  = cpp -C -P -traditional -Wno-invalid-pp-token
DM = -DMPI
#-----------------------------------------------------------------------------
#  single processor, g95 compiler
#FC   = g95
#OPTS = -ffree-form -ffree-line-length-huge -I../include -O2
#CPP  = cpp -C -P -traditional
#-----------------------------------------------------------------------------
#  multiple processors, distributed memory (MPI), g95 compiler
#FC = mpif90
#OPTS = -f90=g95 -ffree-form -ffree-line-length-huge -I../include -O2
#CPP = cpp -C -P -traditional
#DM = -DMPI
#-----------------------------------------------------------------------------
#  IBM POWER6, single processor
#      (e.g., NCAR's bluefire)
#      NOTE: on bluefire, use 'gmake'
#FC   = xlf_r
#OPTS = -qfree=f90 -I../include -O3 -qstrict -qnozerosize -qmaxmem=-1 -q64
#CPP  = /lib/cpp -C -P
#ADV  = -DSGN
#-----------------------------------------------------------------------------
#  IBM POWER6, multiple processors, shared memory using OpenMP
#      (e.g., NCAR's bluefire)
#      NOTE: on bluefire, use 'gmake'
#FC   = xlf_r
#OPTS = -qfree=f90 -I../include -O3 -qstrict -qnozerosize -qmaxmem=-1 -q64 -qsmp=noauto
#CPP  = /lib/cpp -C -P
#ADV  = -DSGN
#-----------------------------------------------------------------------------
#  IBM POWER6, multiple processors, distributed memory using MPI
#      (e.g., NCAR's bluefire)
#      NOTE: on bluefire, use 'gmake'
#FC   = mpxlf_r
#OPTS = -qfree=f90 -I../include -O3 -qstrict -qnozerosize -qmaxmem=-1 -q64
#CPP  = /lib/cpp -C -P
#DM   = -DMPI
#ADV  = -DSGN
#-----------------------------------------------------------------------------
#  IBM POWER6, multiple processors, hybrid ... both OpenMP and MPI
#      (e.g., NCAR's bluefire)
#      NOTE: on bluefire, use 'gmake'
#FC   = mpxlf_r
#OPTS = -qfree=f90 -I../include -O3 -qstrict -qnozerosize -qmaxmem=-1 -q64 -qsmp=noauto
#CPP  = /lib/cpp -C -P
#DM   = -DMPI
#ADV  = -DSGN
#-----------------------------------------------------------------------------
#-- You shouldn't need to change anything below here
#-----------------------------------------------------------------------------

SRC   = adv.F \
	advaxi.F \
	anelp.F \
	base.F \
	bc.F \
	cm1.F \
	comm.F \
	diff2.F \
	goddard.F \
	init3d.F \
	init_physics.F \
	init_surface.F \
	init_terrain.F \
	kessler.F \
	lfoice.F \
	maxmin.F \
	misclibs.F \
	morrison.F \
	module_mp_nssl_2mom.F \
	param.F \
	parcel.F \
	pdef.F \
	poiss.F \
	sfcphys.F \
	singleton.F \
	solve.F \
	sounde.F \
	sound.F \
	soundns.F \
	soundcb.F \
	statpack.F \
	thompson.F \
	turb.F \
	writeout.F \
	restart.F \
	writeout_nc.F \
	writeout_hdf5.F \
	raddata3d.F \
	radlib3d.F \
	irrad3d.F \
	sorad3d.F \
	radtrns3d.F \
	getcape.F \
	ysu.F \
	sfclay.F \
	sfclayrev.F \
	slab.F \
	oml.F

OBJS = $(addsuffix .o, $(basename $(SRC)))

FFLAGS  =  $(OPTS)
AR      = ar cru

.SUFFIXES:
.SUFFIXES:      .F .f90 .o

all : cm1

cm1:			$(OBJS)
			$(FC) $(OBJS) $(FFLAGS) $(OUTPUTINC) $(OUTPUTLIB) $(LINKOPTS) -o ../run/cm1.exe
			$(AR) onefile.F $(SRC)
			mv onefile.F ../run

.F.o:
			$(CPP) $(DM) $(DP) $(ADV) $(OUTPUTOPT) $*.F > $*.f90
			$(FC) $(FFLAGS) $(OUTPUTINC) -c $*.f90

code:
			$(AR) onefile.F $(SRC)
			mv onefile.F ../run

clean:
			rm -f *.f90 *.o *.a *.mod

# DEPENDENCIES : only dependencies after this line (don't remove the word DEPENDENCIES)

cm1.o: restart.o
poiss.o: singleton.o
param.o: thompson.o morrison.o module_mp_nssl_2mom.o
solve.o: thompson.o morrison.o module_mp_nssl_2mom.o restart.o
init_physics.o: sfclay.o sfclayrev.o oml.o slab.o
turb.o: sfclay.o sfclayrev.o slab.o oml.o ysu.o
init_surface.o: oml.o
init3d.o:  module_mp_nssl_2mom.o
writeout_nc.o: restart.o
