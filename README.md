# Kutu

Kutu, _куту_, is the Kyrgyz word for "box". In this repository, we box in containers several open-source simulators used in [Inductiva API](https://github.com/inductiva/inductiva/tree/main). These containers are inspired by many others available online. Moving forward, these containers will take into consideration high-performance computing environments (HPC), platform versatility and be as lightweight as possible.

## Getting Started

Currently, our container images follow the Dockerfile standards, which are compatible with other platforms like Apptainer.

Each simulator provided has at least one container image. Depending on the version of the simulator, more than one container image may be available.

To use one of the containers to run simulations, you need to build them locally. For example, we can build GROMACS as follows:

```bash
docker build -f simulators/gromacs/Dockerfile -t gromacs-image .
```

Then, you can run the container with the following command:

```bash
docker run -it gromacs-image
```

This will allow the isolation of the simulation environment from the host machine.
