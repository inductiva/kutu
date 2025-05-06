
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
| openfast_v3.5.2 | 73.00116920471191 MB |
| openfast_v4.0.3 | 83.2683687210083 MB |
| openfast_v4.0.2 | 83.28230571746826 MB |
| cans_v2.4.0 | 97.27389526367188 MB |
| cans_v3.0.0 | 98.62833499908447 MB |
| swash_v9.01A | 101.622633934021 MB |
| gromacs_v2025.0 | 109.83393669128418 MB |
| gromacs_v2025.1 | 111.13646411895752 MB |
| apptainer-converter_v0.1.0 | 114.74631023406982 MB |
| mohid_v24.10 | 175.23876190185547 MB |
| cm1_v18 | 239.32962894439697 MB |
| swan_v41.45 | 282.5113525390625 MB |
| swan_v41.31 | 282.51443099975586 MB |
| opensees_v2.5.0 | 290.51967906951904 MB |
| snl-swan_v2.2 | 298.9218330383301 MB |
| amr-wind_v1.4.0 | 325.1194372177124 MB |
| amr-wind_v3.4.1 | 333.0209074020386 MB |
| amr-wind_v3.4.0 | 333.0294647216797 MB |
| opentelemac_v9.0.0 | 382.2199287414551 MB |
| opentelemac_v8p4r0 | 384.2470808029175 MB |
| swash_v10.01A | 390.79254245758057 MB |
| swash_v10.05 | 390.88879013061523 MB |
| swash_v11.01 | 390.89534854888916 MB |
| nwchem_v7.2.2 | 403.40702056884766 MB |
| nwchem_v7.2.3 | 404.76081562042236 MB |
| delft3d_v6.04.00 | 517.3401861190796 MB |
| swan_v41.51 | 558.3809080123901 MB |
| cm1_v21.1 | 576.6939287185669 MB |
| opensees_v3.7.1 | 719.4835586547852 MB |
| reef3d_v24.02 | 778.3759803771973 MB |
| schism_v5.13.0 | 836.2760696411133 MB |
| fds_v6.9.1 | 944.8491230010986 MB |
| fds_v6.10.1 | 952.6337289810181 MB |
| reef3d_v24.12 | 1075.5085287094116 MB |
| reef3d_v25.02 | 1102.0069732666016 MB |
| quantum-espresso_v7.3.1 | 1275.9760751724243 MB |
| quantum-espresso_v7.4.1 | 1307.454647064209 MB |
| gromacs_v2025.0_gpu | 1410.7519044876099 MB |
| gromacs_v2025.1_gpu | 1412.1280975341797 MB |
| dualsphysics_v5.4.1 | 1653.303677558899 MB |
| coawst_v3.8 | 1674.9419555664062 MB |
| cp2k_v2025.1 | 1710.383994102478 MB |
| openseespy_v3.7.1 | 1811.5896615982056 MB |
| cp2k_v2025.1_gpu | 2147.861210823059 MB |
| gx_v11-2024_gpu | 2695.2003326416016 MB |
| dualsphysics_v5.4.1_gpu | 3081.0428953170776 MB |
<!-- END-DOCKER-TAGS-TABLE -->
