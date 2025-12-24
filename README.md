# Fault-Tolerant Network-on-Chip (FTTM) Simulator

This project implements the **Fault-Tolerant Task Mapping (FTTM)** algorithm on top of the **Noxim** Cycle-Accurate NoC Simulator. It features a custom `ManagerCore` that detects hardware faults and dynamically remaps tasks to spare cores based on energy optimization (Manhattan Distance).

## Features
* **FTTM Algorithm:** Dynamic task remapping upon fault injection
* **Energy-Aware Recovery:** Selects spare cores that minimize communication energy
* **Configurable Fault Injection:** Edit `faults.txt` to specify fault locations
* **Interactive GUI Visualizer:** HTML/JS visualization with real-time charts
* **Windows Native Build:** Fully compatible with MinGW/MSYS on Windows

## Prerequisites
- **Windows** with PowerShell
- **MinGW-w64** (GCC 14+ recommended)
- **CMake**

## Quick Start

### 1. Clone and Build
```powershell
git clone https://github.com/Abdullah-Mehmood-242/Noxim-FTTM.git
cd Noxim-FTTM/noxim/bin

# Install dependencies (one-time)
.\setup_libs.ps1

# Build
mingw32-make -B
```

### 2. Configure Faults
Edit `faults.txt` to specify fault injection points:
```
# Format: x,y (one per line)
0,0    # Inject fault at Core (0,0)
1,1    # Inject fault at Core (1,1)
2,0    # Inject fault at Core (2,0)
```

### 3. Run Simulation
```powershell
.\noxim.exe -config ../config_examples/default_config.yaml
```

Or use the helper script:
```powershell
.\run_fttm.bat 0,0 1,1 2,0
```

### 4. View Results
```powershell
start fttm_gui.html
```
Then click **📂 Load JSON File** → select `noxim_state.json`

## Expected Output
```
Mapped Task 0-9 to Cores 0-9

Fault injected at Core 0 (0,0)
Task 0 remapped to Core 10

Fault injected at Core 5 (1,1)
Task 5 remapped to Core 12

=== FTTM SIMULATION COMPLETED ===
Injected 3 fault(s) from faults.txt
```

## GUI Features

| Button | Description |
|--------|-------------|
| 📂 Load JSON | Load real simulation output |
| 🎮 Single Fault | Demo with 1 fault |
| 🔥 Stress Test | Demo with 3 faults |
| 🖱️ Interactive | Click cores to inject faults |

## Project Structure
```
noxim/
├── bin/
│   ├── faults.txt          # Fault configuration
│   ├── fttm_gui.html       # GUI Visualizer
│   ├── run_fttm.bat        # Helper script
│   ├── noxim_state.json    # Simulation output
│   └── Makefile
├── src/
│   ├── Main.cpp            # Entry point with FTTM
│   ├── NoximManagerCore.cpp # FTTM algorithm
│   └── ...
└── config_examples/
```

## Troubleshooting

**"complete binding failed"**: Known SystemC issue, suppressed in Main.cpp.

**"ld returned 1 exit status"**: Run `mingw32-make -B` for full rebuild.

**SystemC download fails**: Run `.\fix_systemc.ps1` after setup.

## References

Catania V., Mineo A., Monteleone S., Palesi M., and Patti D. (2016) *Cycle-Accurate Network on Chip Simulation with Noxim*. ACM Trans. Model. Comput. Simul. 27, 1, Article 4.

## License
See [LICENSE.txt](noxim/doc/LICENSE.txt)