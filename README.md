# Superconducting Qubit Capacitor Geometry Optimization - DRL Implementation
This repository contains the deep reinforcement learning (DRL) model training code for the research paper **Optimization of Superconducting Qubit Capacitor Geometry Based on Deep Reinforcement Learning**, published in *Quantum Information Processing* (2026). The code implements the DRL dual neural network model for autonomous optimization of superconducting qubit double-pad capacitor geometries, with the Purcell-limited \(T_\text{1,limit}\) as the core optimization target.

## Paper Information
- **Publication**: Quantum Information Processing, Volume 25, Article number 68 (2026)
- **DOI**: [10.1007/s11128-026-05100-9](https://doi.org/10.1007/s11128-026-05100-9)
- **Official Link**: [Springer Nature](https://link.springer.com/article/10.1007/s11128-026-05100-9)
- **Key Contribution**: This work optimizes arc-edged capacitor geometries to reduce interface energy participation ratio (EPR), improve electric field distribution, and enhance the Purcell-limited \(T_\text{1,limit}\) under a fixed \(430~\mathrm {\mu m} \times 300~\mathrm {\mu m}\) footprint. Supplementary 3D simulations verify the optimized structure mitigates surface dielectric loss for better qubit coherence performance.

## Installation
### Prerequisites
- Python 3.8+
- PyTorch (for DRL model implementation and training)
- NumPy & SciPy (for numerical calculation and EPR analysis)
- Matplotlib (for electric field distribution and EPR result visualization)
- Additional electromagnetic simulation dependencies (consistent with the paper's numerical analysis of dielectric loss and EPR)

### Install Dependencies
```bash
pip install torch numpy scipy matplotlib
# Install additional electromagnetic simulation tools
```

## Usage
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/Celester7/Optimization-of-superconducting-qubit-capacitor-geometry-based-on-deep-reinforcement-learning.git
   ```
2. Model training: Run the main DRL training script to start capacitor geometry optimization (target: \(T_\text{1,limit}\) maximization).
   ```bash
   newpurcell_training_model.ipynb
   ```
3. Parameter Configuration: Modify the `DDPG_env.py` and `Q3D.py` files to adjust DRL model hyperparameters, capacitor constraints, calculation parameters and simulation settings (consistent with the paper's experimental setup).

### Key Scripts
- `newpurcell_training_model.ipynb`: Core DRL dual neural network training script for autonomous capacitor shape evolution (human-in-the-loop-free).
- `DDPG_env.py`: All configurable parameters for DRL training.
- `Q3D.py`: All configurable parameters for electromagnetic simulation.
- `T1_cal.py`: All functions for capacitor geometry modeling, and \(T_\text{1,limit}\) evaluation.

## Citation
If you use this code or the findings of this research in your work, please cite the original paper:
```bibtex
@Article{Zhang2026,
  author  = {Zhang, Chaojie and Wang, Weilong and Li, Jiaxin and Yuan, Benzheng and Yu, Xiaohan and Zha, Zhiguo and Mu, Qing and Shan, Zheng},
  title   = {Optimization of superconducting qubit capacitor geometry based on deep reinforcement learning},
  journal = {Quantum Information Processing},
  year    = {2026},
  volume  = {25},
  number  = {68},
  doi     = {10.1007/s11128-026-05100-9},
  url     = {https://link.springer.com/article/10.1007/s11128-026-05100-9}
}
```

## Data Availability
The full dataset (including simulation results, EPR calculation data, and DRL training logs) supporting the key findings of the paper is available from the corresponding author (Dr. Weilong Wang) upon reasonable request. The cleaned dataset will be publicly deposited in this repository and other persistent open science repositories in line with the journal's open science initiatives.

## Acknowledgements
- We thank Chuanbing Han and Haoran He for in-depth discussions on capacitor structures and optimization methods.
- This work is affiliated with the Information Engineering University (Zhengzhou, China) and the Laboratory for Advanced Computing and Intelligence Engineering (ACIE Lab, Zhengzhou, China).
- Special thanks to the research team and their families for their unwavering support and encouragement.
