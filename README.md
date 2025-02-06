
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
| nwchem_v7.2.2_dev | 0.1544809341430664 MB |
| echo_v0.1_dev | 28.16631507873535 MB |
| splishsplash_v2.13.0_dev | 41.682379722595215 MB |
| openfast_v3.5.2_dev | 73.00076580047607 MB |
| cans_v2.3.4_dev | 90.67843914031982 MB |
| xbeach_v1.24_dev | 94.5681209564209 MB |
| swash_v9.01A_dev | 97.0221700668335 MB |
| fvcom_v5.1.0_dev | 100.73816299438477 MB |
| gromacs_v2022.2_dev | 101.88790035247803 MB |
| amr-wind_v1.4.0_dev | 113.8293046951294 MB |
| erf_v24.11_dev | 176.28268814086914 MB |
| swan_v41.45_dev | 267.23991775512695 MB |
| swan_v41.31_dev | 270.5221252441406 MB |
| snl-swan_v2.2_dev | 295.7950563430786 MB |
| dualsphysics_v5.2.1_dev | 317.7802028656006 MB |
| swash_v10.01A_dev | 383.88838291168213 MB |
| swash_v10.05_dev | 383.98483180999756 MB |
| croco_v2.0.1_dev | 430.6199827194214 MB |
| delft3d_v6.04.00_dev | 517.3392171859741 MB |
| base-image_v0.1.0_dev | 523.4462175369263 MB |
| openfoam-foundation_v8_dev | 527.970461845398 MB |
| base-image_v0.1.1_dev | 553.7138233184814 MB |
| benchmarks_v0.1.0_dev | 574.0306100845337 MB |
| funwave_v3.6.0_dev | 579.7822141647339 MB |
| openfoam-foundation_v12_dev | 628.441707611084 MB |
| xbeach_v1.23_dev | 662.7043132781982 MB |
| seissol_v1.3.0_dev | 684.639045715332 MB |
| opensees_v3.7.1_dev | 714.5280160903931 MB |
| reef3d_v24.02_dev | 774.8494472503662 MB |
| schism_v5.11.0_dev | 814.246018409729 MB |
| fds_v6.8_dev | 904.3600873947144 MB |
| wrf_v4.6.1_dev | 1093.9902954101562 MB |
| openfoam-esi_v2206_dev | 1148.1960544586182 MB |
| openfoam-esi_v2406_dev | 1170.114875793457 MB |
| openfoam-esi_v2412_dev | 1177.4391889572144 MB |
| ww3_v11-2024_dev | 1216.6363620758057 MB |
| quantum-espresso_v7.3.1_dev | 1275.9759273529053 MB |
| gromacs_v2022.2_gpu_dev | 1384.075671195984 MB |
| dualsphysics_v5.2.1_gpu_dev | 1433.2349462509155 MB |
| fvcom_v4.4.7_dev | 1450.4781532287598 MB |
| coawst_v3.8_dev | 1853.8055114746094 MB |
| gx_v11-2024_gpu_dev | 2695.1921195983887 MB |
<!-- END-DOCKER-TAGS-TABLE -->
