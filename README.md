# py-ecpn

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

`py-ecpn` is a Python package for the numerical simulation of equal coupling
photonic networks. Currently, the software allows to study the dynamics on
fully connected, and long-range interacting one-dimensional systems. 


### Prerequisites

pyECPN is developed under python3 and requires the functionality of 

* numpy
* scipy

Further, the figure generation scripts included with the examples require the
functionality of python3's

* matplotlib

## Included materials

The repository follows a modular structure:

```
py-ecpn/
├── CITATION.cff
├── LICENSE.md
├── README.md
├── ecpn_src
│   ├── __init__.py
│   ├── coupling_matrix.py
│   ├── data_analysis.py
│   ├── initial_state_heuristic.py
│   ├── measurement.py
│   ├── solver.py
│   ├── thermal_equilibrium.py
│   └── thermodynamic_quantities.py
└── results
    ├── fig_01
    │   ├── cfg_01.npz
    │   ├── cfg_02.npz
    │   ├── fig_01.png
    │   └── main_fig01.py
    ├── fig_02
    │   ├── fig_02.png
    │   └── main_fig02.py
    ├── numExp01_small_systems
    │   ├── data_N8
    │   ├── data_N16
    │   ├── data_N32
    │   ├── data_N64
    │   ├── helper_ECPN.py
    │   ├── main_multiprocessing.py
    │   └── main_single_run.py
    └── pp_data_analysis
        ├── get_data.sh
        ├── main_postprocessing.py
        ├── res_N16.dat
        ├── res_N32.dat
        ├── res_N64.dat
        └── res_N8.dat
```

Subfolder `ecpn_src/` contains Python modules implementing the basic functionality of the software.

The folder `results/` implements a small project with exemplary simulation results for systems of
small size.

The repository further contains
* `CITATION.cff`, a file with software citation information.
* `LICENSE`, a license file.
* `Readme.md`, this file.

For a more detailed description of functions, defined in the above modules,
their parameters and return values we refer to the example cases and
documentation provided within the code.

## Exemplary results for systems of small size

![alt text](https://github.com/omelchert/py-ecpn/blob/main/results/fig_01/fig_01.png)
![alt text](https://github.com/omelchert/py-ecpn/blob/main/results/fig_02/fig_02.png)

### Brief explanation of the above figure

Equal-coupling photonic networks on fully connected graphs.  (a-b)
Configurations of 16 photonic soft-spins, demonstrating (a) order at energy
density h=-0.5, and, (b) disorder at h=0.9.  (c-d) Finite-size effects
exhibited by (a) a magnetization-like order parameter, and, (b) the associated
finite-size susceptibility. The peaks of the susceptibility indicate the
location of pseudocritical points at which the optical phase transition occurs
in the respective finite-size system.

## Availability of the software

The py-ecpn software package is derived from research software and meant to
work as a (system-)local software tool. There is no need to install it once you
got a local
[clone](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository)
of the repository, e.g. via

``$ git clone https://github.com/omelchert/py-ecpn.git``

## License 

This project is licensed under the MIT License - see the
[LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

This work received funding from the Deutsche Forschungsgemeinschaft  (DFG) under
Germany’s Excellence Strategy within the Cluster of Excellence PhoenixD
(Photonics, Optics, and Engineering – Innovation Across Disciplines) (EXC 2122,
projectID 390833453).
