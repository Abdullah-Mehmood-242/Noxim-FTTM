# Fault-Tolerant Network-on-Chip (NoC) Simulator

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Completed-success.svg)

A Python-based simulation of the **Fault-Tolerant Task Mapping (FTTM)** algorithm for Many-Core Processors. This project implements the concepts from the research paper *"Enhancing Reliability and Energy Efficiency in Many-Core Processors Through Fault-Tolerant Network-on-Chip"*.

## 📌 Project Overview
As transistor scaling continues, many-core processors become increasingly susceptible to permanent faults. This project simulates a **2D Mesh Network-on-Chip (NoC)** and implements a smart mapping algorithm that:
1.  **Detects** permanent core faults.
2.  **Remaps** tasks from faulty cores to the best available spare cores.
3.  **Optimizes** for energy efficiency by minimizing communication distance.

## 📊 Key Results
Our simulation demonstrates that the FTTM algorithm is significantly more energy-efficient than random remapping strategies.

| Metric | FTTM (Proposed) | Random Mapping | Improvement |
| :--- | :---: | :---: | :---: |
| **Avg Energy** | ~4618 units | ~5761 units | **~19.8%** |

![Energy Comparison](assets/comparison.png)

## 🚀 Features
*   **2D Mesh Simulator**: Configurable grid size (e.g., 4x4, 8x8).
*   **Dynamic Fault Injection**: Simulate permanent core failures at runtime.
*   **Smart Recovery**: Automatic task migration to spare cores.
*   **Energy Analysis**: Real-time calculation of communication energy ($Volume \times Hops$).
*   **Visualization**: Generates visual maps of the NoC state.

## 🛠️ Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Abdullah-Mehmood-242/Fault-Tolerant-NoC-Simulator.git
    ```
    **Enter the Directory**:
    ```bash
    cd Fault-Tolerant-NoC-Simulator-main/Fault-Tolerant-NoC-Simulator-main/
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 💻 Usage Guide

### 1. Basic Simulation
Run the main script to see a single fault recovery scenario on a 4x4 grid.
```bash
python main.py
```
**Output**: Generates `Initial_Mapping_*.png` and `Post-Fault_Mapping_*.png`.

| Initial State | Post-Fault Recovery |
| :---: | :---: |
| ![Initial](assets/initial_mapping.png) | ![Recovery](assets/post_fault.png) |

### 2. Stress Test
Simulate multiple sequential faults to test system robustness.
```bash
python stress_test.py
```

### 3. Comparative Analysis
Run the benchmark script to compare FTTM against Random Mapping.
```bash
python comparison.py
```

### 4. Run Unit Tests
Verify the correctness of the implementation.
```bash
python test_suite.py
```

## 📂 File Structure
```text
.
├── assets/               # Documentation images
├── noc_simulator.py      # Core NoC classes (NoC, Core, Task)
├── fttm_mapper.py        # Fault-Tolerant Mapping Algorithm
├── main.py               # Basic simulation entry point
├── stress_test.py        # Robustness testing script
├── comparison.py         # Benchmarking script
├── test_suite.py         # Unit tests
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## 📜 License
This project is open-source and available under the MIT License.

## 👥 Credits and Supervision

This project was developed by the following students under academic supervision:

* **Supervisor:** Ms. Adeeba Aslam (Lecturer, The University of Lahore - Sargodha Campus)

* **Developer:** Abdullah Mehmood ([@Abdullah-Mehmood-242](https://github.com/Abdullah-Mehmood-242/))
* **Developer:** Ammad Younas ([@Ammad-Younas](https://github.com/Ammad-Younas))
