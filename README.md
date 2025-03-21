
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
| echo_v0.1 | 28.168192863464355 MB |
| openfast_v3.5.2 | 73.00116920471191 MB |
| openfast_v4.0.2 | 83.28230571746826 MB |
| xbeach_v1.24 | 94.56818866729736 MB |
| swash_v9.01A | 97.02248287200928 MB |
| cans_v2.4.0 | 97.27389526367188 MB |
| fvcom_v5.1.0 | 100.73739910125732 MB |
| gromacs_v2025.0 | 109.83393669128418 MB |
| amr-wind_v1.4.0 | 113.89888286590576 MB |
| amr-wind_v3.4.0 | 127.6489782333374 MB |
| mohid_v24.10 | 175.23876190185547 MB |
| cm1_v18 | 239.32962894439697 MB |
| swan_v41.45 | 282.0641851425171 MB |
| swan_v41.31 | 282.0675048828125 MB |
| opensees_v2.5.0 | 290.51967906951904 MB |
| snl-swan_v2.2 | 295.79521083831787 MB |
| dualsphysics_v5.2.1 | 317.7801342010498 MB |
| swash_v11.01 | 381.3209295272827 MB |
| swash_v10.01A | 383.88835620880127 MB |
| swash_v10.05 | 383.98499584198 MB |
| nwchem_v7.2.2 | 396.5039577484131 MB |
| nwchem_v7.2.3 | 401.409161567688 MB |
| openfoam-foundation_v8 | 527.9802980422974 MB |
| base-image_v0.1.1 | 553.7915143966675 MB |
| swan_v41.51 | 558.3809003829956 MB |
| cm1_v21.1 | 576.6939287185669 MB |
| openfoam-foundation_v12 | 628.443922996521 MB |
| opensees_v3.7.1 | 719.4835586547852 MB |
| reef3d_v24.02 | 778.3759803771973 MB |
| openseespy_v3.7.1 | 899.0399379730225 MB |
| fds_v6.9.1 | 944.8491230010986 MB |
| reef3d_v24.12 | 1075.5085287094116 MB |
| reef3d_v25.02 | 1102.0069732666016 MB |
| openfoam-esi_v2206 | 1148.198037147522 MB |
| openfoam-esi_v2406 | 1170.1125230789185 MB |
| openfoam-esi_v2412 | 1177.428095817566 MB |
| quantum-espresso_v7.3.1 | 1275.9760751724243 MB |
| quantum-espresso_v7.4.1 | 1307.454647064209 MB |
| gromacs_v2022.2_gpu | 1385.8429822921753 MB |
| gromacs_v2025.0_gpu | 1410.7519044876099 MB |
| dualsphysics_v5.2.1_gpu | 1433.2349166870117 MB |
| coawst_v3.8 | 1674.9419555664062 MB |
| cp2k_v2025.1 | 1710.383994102478 MB |
| cp2k_v2025.1_gpu | 2147.861210823059 MB |
| gx_v11-2024_gpu | 2695.2003326416016 MB |
<!-- END-DOCKER-TAGS-TABLE -->
