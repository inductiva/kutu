/*
** Options for EuroSea Test Case
** maria.liste - 2022
** Application flag:   COAWST MODEL - COUPLEDNESTED OPTION
** Input script:       ocean.in
**                     swan.in
**                     coupling.in
*/
#define ROMS_MODEL     /*if you want to use the ROMS model */
#define SWAN_MODEL     /*if you want to use the SWAN model */

/*OPTIONS for model coupling:*/
#define MCT_LIB          /*if you have more than one model selected */
#define MCT_INTERP_OC2WV /*allows grid interpolation between the ocean and wave models*/
#define UV_KIRBY 	 /*compute "depth-avg" current based on Hwave to */
                         /*be sent from the ocn to the wav model for coupling*/

/*OPTIONS for grid nesting:*/
#define NESTING	  	/*activate grid nesting: composite/refinement */
#define TWO_WAY		/*two-way nesting in refinement grids */

/*OPTIONS for surface fluxes formulation using atmospheric boundary layer (Fairall et al, 1996):*/
#define BULK_FLUXES	/*if you don�t have activate WRF, provide consistent fluxes*/
#define EMINUSP	        /*computing E-P*/

/*Wave effect on currents (WEC) and shallow water OPTIONS:*/
#define WEC_VF 		/*wave-current stresses from Uchiyama et al.*/
#define WDISS_WAVEMOD 	/*wave dissipation from a wave model*/

/*OPTIONS associated with momentum equations:*/
#define UV_ADV  	/*advection terms*/
#define UV_COR  	/*Coriolis term*/
#define UV_VIS2  	/*harmonic horizontal mixing*/
#undef UV_U3HADVECTION /*Third-order upstream horizontal advection of 3D momentum*/
#undef UV_SADVECTION   /*Parabolic splines vertical advection of momentum*/
#define SPLINES_VVISC   /*splines reconstruction of vertical viscosity*/
#define UV_LOGDRAG      /*logarithmic bottom friction*/

/*OPTIONS associated with tracers equations:*/
#define SPLINES_VDIFF   /*splines reconstruction of vertical diffusion*/
#define SALINITY   	/*having salinity*/
#define TS_DIF4    	/*harmonic horizontal mixing*/
#define NONLIN_EOS      /*nonlinear equation of state*/
#define SOLAR_SOURCE	/*solar radiation source term*/

#define TS_MPDATA

/*Pressure gradient algorithm OPTIONS*/
#define DJ_GRADPS  	/*splines density Jacobian (Shchepetkin, 2000)*/
#define ATM_PRESS 	/*to impose atmospheric pressure onto sea surface*/

/*Model configuration OPTIONS:*/
#define CURVGRID   	/*curvilinear coordinates grid*/
#define SOLVE3D    	/*solving 3D primitive equations*/
#define MASKING 	/*land/sea masking*/
#define SPHERICAL

/*OPTIONS for horizontal mixing of momentum:*/
#define MIX_S_UV  	/*mixing along constant S-surfaces*/

/*OPTIONS for horizontal mixing of tracers:*/
#define MIX_GEO_TS 	/*mixing on geopotential (constant Z) surfaces*/

/*OPTIONS for vertical turbulent mixing scheme of momentum and tracers*/
#define GLS_MIXING	/*Generic Length-Scale mixing closure*/
#undef LIMIT_VDIFF
#undef LIMIT_VVISC

/*OPTIONS for the Generic Length-Scale closure (Warner et al., 2005):*/
#define KANTHA_CLAYSON	/*Kantha and Clayson stability function*/
#define N2S2_HORAVG	/*horizontal smoothing of buoyancy/shear*/
#define RI_SPLINES	/*splines reconstruction for vertical sheer*/

/*Lateral boundary conditions OPTIONS:*/
#define RADIATION_2D	/*tangential phase speed in radiation conditions*/

/*OPTIONS for analytical fields configuration:*/
#define ATM_PRESS

#define ANA_BTFLUX 	/*Bottom temperature flux */
#define ANA_BSFLUX 	/*Bottom salinity flux*/

#undef ANA_NUDGCOEF	/*analytical climatology nudging coefficients*/
#undef ANA_SMFLUX	/*analytical surface momentum stress*/
#undef ANA_FSOBC	/*analytical free-surface boundary conditions*/
#undef ANA_M2OBC	/*analytical 2D momentum boundary conditions */
#define ANA_STFLUX	/*analytical surface net heat flux*/
#define ANA_SSFLUX	/*analytical surface salinity flux*/
#undef ANA_BPFLUX 	/*analytical bottom passive tracers fluxes */
#undef ANA_SPFLUX 	/*analytical surface passive tracers fluxes */
#undef ANA_SRFLUX	/*analytical surface shortwave radiation flux*/
