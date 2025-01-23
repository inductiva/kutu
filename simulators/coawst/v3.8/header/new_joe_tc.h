/*
** Modified JOE_TC for EuroSea Application
** Based on original JOE_TC Test and EuroSea requirements
** Application flag: JOE_TC
*/

/* === Model Experiment Configuration === */
# undef ExpA1
# undef ExpA
# undef ExpB
# undef ExpC
# undef ExpD
# undef ExpE
# define ExpF

#ifdef ExpA1            /* WRF<->SWAN */
# define WRF_MODEL
# define SWAN_MODEL
#endif

#ifdef ExpA            /* WRF->ROMS */
# define AKLIMIT
# define WRF_MODEL
# define SST_CONST
# define ROMS_MODEL
#endif

#ifdef ExpB  /* WRF<->ROMS */
# define WRF_MODEL
# define ROMS_MODEL
#endif

#ifdef ExpC /* WRF<->ROMS<- SWAN :enhanced surface stress, no currents from ROMS to SWAN*/
# define WRF_MODEL
# define ROMS_MODEL
# define SWAN_MODEL
# define UV_CONST
# define COARE_TAYLOR_YELLAND
#endif

#ifdef ExpD /* WRF<->ROMS<-> SWAN :enhanced surface stress, currents from ROMS to SWAN*/
# define WRF_MODEL
# define ROMS_MODEL
# define SWAN_MODEL
# define COARE_TAYLOR_YELLAND
#endif

#ifdef ExpE  /*Same as ExpD, but will SWAN BBL dynamics */
# define WRF_MODEL
# define ROMS_MODEL
# define SWAN_MODEL
# define COARE_TAYLOR_YELLAND
# define SSW_BBL
#endif



/* === Model Coupling Options === */
#ifdef ExpF 
# define SWAN_MODEL
# define WRF_MODEL
# define ROMS_MODEL
# define COARE_TAYLOR_YELLAND
# define WEC_VF
# define SSW_BBL
# define WDISS_WAVEMOD
# define UV_KIRBY
#endif

/* === MCT Coupling Library Options === */
#define MCT_LIB
#define MCT_INTERP_OC2AT
#define MCT_INTERP_WV2AT
#define MCT_INTERP_OC2WV

/* === Grid Nesting Options === */
#define NESTING
#define TWO_WAY

/* === Core Model Configuration === */
#ifdef ROMS_MODEL
/* Physics and Numerics */
# define UV_ADV
# define UV_COR
# define UV_VIS2
# define MIX_S_UV
# define SPHERICAL
# define CURVGRID

/* Bottom Boundary Layer Options */
# ifdef SSW_BBL
#  define SSW_CALC_ZNOT
# else
#  define UV_LOGDRAG
# endif

/* Tracer Options */
# define TS_MPDATA
# define TS_DIF4
# define DJ_GRADPS
# define MIX_GEO_TS
# define SALINITY
# define SOLVE3D
# define SPLINES_VDIFF
# define SPLINES_VVISC
# define AVERAGES
# define NONLIN_EOS

/* Grid Configuration */
# define MASKING

/* Forcing Options */
# ifdef WRF_MODEL
#  define ATM2OCN_FLUXES
#  define BULK_FLUXES
#  define EMINUSP
# else
#  define BULK_FLUXES
#  define ANA_SMFLUX
#  define ANA_STFLUX
#  define ANA_SSFLUX
# endif

/* Pressure and Boundary Options */
# define ATM_PRESS
# define RADIATION_2D
# define ANA_BTFLUX
# define ANA_BSFLUX

/* Solar Radiation */
# define SOLAR_SOURCE

/* Turbulence Closure */
# define GLS_MIXING
# undef  MY25_MIXING
# if defined GLS_MIXING || defined MY25_MIXING
#  define KANTHA_CLAYSON
#  define N2S2_HORAVG
#  define RI_SPLINES
# endif

/* Undef Analytical Options */
# undef ANA_NUDGCOEF
# undef ANA_FSOBC
# undef ANA_M2OBC
# undef ANA_BPFLUX
# undef ANA_SPFLUX
# undef ANA_SRFLUX

/* Output Options */
# define DIAGNOSTICS_UV
# define DIAGNOSTICS_TS
#endif

/* === Wave Model Options === */
#if defined WRF_MODEL && defined SWAN_MODEL
# define DRAGLIM_DAVIS
#endif