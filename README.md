
![kutu-banner](https://github.com/inductiva/kutu/assets/7538022/847e6ba9-e420-45d7-b98e-d21192fbdafe)

# Kutu

Kutu, _куту_, is the Kyrgyz word for "box". Here we store all the container
images of the open-source simulators supported by the 
[Inductiva API](https://github.com/inductiva/inductiva/tree/main),
which allows users to easily run physical simulations on the cloud.

These containers are inspired by many others available online. Moving forward, these
containers will take into consideration high-performance computing environments (HPC),
platform versatility and be as lightweight as possible.

## Getting Started

Currently, our container images follow the Dockerfile standards, which are compatible
with other platforms like Apptainer.

Each simulator provided has at least one container image. Depending on the version
of the simulator, more than one container image may be available.

To use one of the containers to run simulations, you need to build them locally.
For example, we can build GROMACS as follows:

```bash
docker build -f simulators/gromacs/Dockerfile -t gromacs-image .
```

Then, you can run the container with the following command:

```bash
docker run -it gromacs-image
```

This will allow the isolation of the simulation environment from the host machine.

Additionally, all our Docker images are available in our
[Docker Hub repository](https://hub.docker.com/r/inductiva/kutu). You can pull
any image directly from there without needing to build it locally. For instance,
to pull the GROMACS image, you can use:

```bash
docker pull inductiva/kutu:gromacs_v2022.2
```

### Docker Images

<!-- DOCKER-TAGS-TABLE -->
| Tag | Size (MB) |
|---|---|
| calculix_v2.22 | 75.58064842224121 MB |
| openfast_v4.0.3 | 83.2683687210083 MB |
| openfast_v4.1.0 | 83.68922710418701 MB |
| cans_v3.0.0 | 98.62833499908447 MB |
| gromacs_v2025.1 | 111.13646411895752 MB |
| sfincs_v2.2.1 | 214.66022109985352 MB |
| swan_v41.45 | 277.1442565917969 MB |
| swan_v41.31 | 277.14671516418457 MB |
| snl-swan_v2.2 | 298.9218330383301 MB |
| dualsphysics_v5.2.1 | 320.4835147857666 MB |
| amr-wind_v1.4.0 | 325.1194372177124 MB |
| amr-wind_v3.4.1 | 333.0209074020386 MB |
| amr-wind_v3.4.0 | 333.0294647216797 MB |
| opentelemac_v9.0.0 | 382.2199287414551 MB |
| opentelemac_v8p4r1 | 384.2730484008789 MB |
| splishsplash_v2.13.0 | 385.70003032684326 MB |
| opentelemac_v8p1r2 | 392.26356506347656 MB |
| delft3d_v6.04.00 | 519.2441167831421 MB |
| cm1_v21.1 | 570.0145578384399 MB |
| swan_v41.51 | 575.2361478805542 MB |
| openfoam-foundation_v13 | 604.4442005157471 MB |
| xbeach_v1.24 | 651.6205368041992 MB |
| openfoam-foundation_v12 | 723.0185632705688 MB |
| openfoam-foundation_v8 | 730.0319910049438 MB |
| schism_v5.13.0 | 836.2760696411133 MB |
| octopus_v16.1 | 882.8841123580933 MB |
| opensees-eesd_v3.0.2 | 890.849702835083 MB |
| wavewatch3_v11-2024 | 1004.6025238037109 MB |
| fds_v6.8 | 1094.3659648895264 MB |
| fds_v6.9.1 | 1109.0954656600952 MB |
| fds_v6.10.1 | 1114.0761919021606 MB |
| openfoam-esi_v2206 | 1249.4238557815552 MB |
| openfoam-esi_v2406 | 1271.3269062042236 MB |
| openfoam-esi_v2412 | 1278.6407299041748 MB |
| openfoam-esi_v2506 | 1283.2025861740112 MB |
| gromacs_v2025.1_gpu | 1412.1280975341797 MB |
| dualsphysics_v5.4.1 | 1662.9539070129395 MB |
| wrf_v4.6.1 | 1965.3614587783813 MB |
| wrf_v4.7.1 | 1966.6437969207764 MB |
| dualsphysics_v5.4.1_gpu | 2167.187635421753 MB |
| cans_v2.4.0_gpu | 3278.5980014801025 MB |
| cans_v3.0.0_gpu | 3280.701066017151 MB |
| amr-wind_v3.4.0_gpu | 3588.6835708618164 MB |
| amr-wind_v3.4.1_gpu | 3613.75515460968 MB |
| octopus_v16.1_gpu | 3742.739362716675 MB |
| amr-wind_v1.4.0_gpu | 5300.673182487488 MB |
<!-- END-DOCKER-TAGS-TABLE -->
