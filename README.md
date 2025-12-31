# 🔬 FTTM Network Stimulation Lab

[![Windows](https://img.shields.io/badge/Platform-Windows-blue.svg)](https://www.microsoft.com/windows)
[![C++](https://img.shields.io/badge/C++-17-00599C.svg)](https://isocpp.org/)
[![SystemC](https://img.shields.io/badge/SystemC-2.3.3-green.svg)](https://systemc.org/)
[![License](https://img.shields.io/badge/License-GPL-yellow.svg)](noxim/doc/LICENSE.txt)

> **Fault-Tolerant Task Mapping (FTTM) for Many-Core Network-on-Chip Systems**

An interactive stimulation platform implementing the FTTM algorithm on top of the **Noxim** Cycle-Accurate NoC Platform. Features real-time fault stimulation, dynamic task remapping, and energy-optimized recovery using Manhattan Distance heuristics.

---

## 📑 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage Guide](#-usage-guide)
- [GUI Stimulation Lab](#-gui-stimulation-lab)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Troubleshooting](#-troubleshooting)
- [References](#-references)
- [Credits](#-credits)
- [License](#-license)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **FTTM Algorithm** | Dynamic task remapping upon fault stimulation |
| **Energy-Aware Recovery** | Selects spare cores that minimize communication energy |
| **Configurable Fault Stimulation** | Edit `faults.txt` to specify fault locations |
| **Interactive GUI Stimulation Lab** | HTML/JS visualization with 4 stimulation modes |
| **Real-time Energy Charts** | Visual comparison of pre/post fault energy consumption |
| **Stress Testing** | Multi-fault sequential injection testing |
| **Windows Native Build** | Fully compatible with MinGW/MSYS on Windows |

---

## 📸 Screenshots

### GUI Stimulation Lab
The interactive HTML-based GUI allows you to:
- Stimulate faults by clicking on cores
- View real-time task remapping
- Compare energy consumption before/after faults
- Run automated stress tests

| Initial State | After Fault Stimulation |
|:-------------:|:-----------------------:|
| All tasks mapped to cores 0-9 | Task remapped to spare core |

---

## 📋 Prerequisites

Before installation, ensure you have the following software installed:

### Required Software

| Software | Version | Download Link |
|----------|---------|---------------|
| **Windows** | 10/11 | - |
| **MinGW-w64** | GCC 14+ | [Download](https://www.mingw-w64.org/downloads/) |
| **CMake** | 3.16+ | [Download](https://cmake.org/download/) |
| **PowerShell** | 5.0+ | Pre-installed on Windows |
| **Git** | Any | [Download](https://git-scm.com/downloads) |

### Verify Installation

Open PowerShell and run:
```powershell
# Check GCC version
g++ --version

# Check CMake version
cmake --version

# Check Git version
git --version
```

All commands should return version information without errors.

---

## 🛠️ Installation

### Step 1: Clone the Repository

```powershell
git clone https://github.com/Abdullah-Mehmood-242/Noxim-FTTM.git
cd Noxim-FTTM
```

### Step 2: Navigate to Build Directory

```powershell
cd noxim/bin
```

### Step 3: Install Dependencies (SystemC Library)

This script downloads and configures the SystemC library automatically:

```powershell
.\setup_libs.ps1
```

**Expected Output:**
```
Downloading SystemC...
Extracting SystemC...
SystemC setup complete!
```

> **Note:** If the download fails, run `.\fix_systemc.ps1` to fix the issue.

### Step 4: Build the Project

```powershell
mingw32-make -B
```

**Expected Output:**
```
Compiling Main.cpp...
Compiling NoC.cpp...
Compiling NoximManagerCore.cpp...
...
Linking noxim.exe...
Build successful!
```

### Step 5: Verify Installation

```powershell
.\noxim.exe --help
```

This should display the Noxim help message with available options.

---

## 💻 Usage Guide

### Quick Start

Run the stimulation with default settings:

```powershell
.\noxim.exe -config ../config_examples/default_config.yaml
```

### Method 1: Using the Helper Script (Recommended)

The `run_fttm.bat` script simplifies running stimulations:

```powershell
# Run with specific fault locations
.\run_fttm.bat 0,0 1,1 2,0

# Run with no specified faults (uses faults.txt if exists)
.\run_fttm.bat
```

### Method 2: Manual Configuration

#### Step 1: Configure Fault Stimulation Points

Edit `faults.txt` to specify where faults should be stimulated:

```text
# Fault Stimulation Configuration
# Format: x,y (one fault per line)
# Coordinates start from (0,0) at bottom-left

0,0    # Stimulate fault at Core (0,0)
1,1    # Stimulate fault at Core (1,1)
2,0    # Stimulate fault at Core (2,0)
```

#### Step 2: Run the Stimulation

```powershell
.\noxim.exe -config ../config_examples/default_config.yaml
```

#### Step 3: View Results in GUI

```powershell
start fttm_gui.html
```

Then click **📂 Load JSON File** → select `noxim_state.json`

### Expected Console Output

```
--------------------------------------------
        Noxim - the NoC Stimulator
        (C) University of Catania
--------------------------------------------

Mapped Task 0 to Core 0
Mapped Task 1 to Core 1
...
Mapped Task 9 to Core 9

Fault stimulated at Core 0 (0,0)
Task 0 displaced from Core 0. Finding spare...
Task 0 remapped to Core 10

Fault stimulated at Core 5 (1,1)
Task 5 displaced from Core 5. Finding spare...
Task 5 remapped to Core 12

=== FTTM STIMULATION COMPLETED ===
Stimulated 3 fault(s) from faults.txt
FTTM state saved to noxim_state.json
```

---

## 🎮 GUI Stimulation Lab

The interactive GUI provides multiple ways to visualize and stimulate the NoC system.

### Opening the GUI

```powershell
start fttm_gui.html
```

Or simply double-click `fttm_gui.html` in File Explorer.

### Stimulation Modes

| Mode | Icon | Description |
|------|:----:|-------------|
| **Fault Wave Stimulation** | 💥 | Auto-inject random fault sequence with configurable intensity |
| **Traffic Pattern Stimulation** | 📡 | Visualize communication load percentages on each core |
| **Thermal Hotspot Stimulation** | 🔥 | Simulate thermal stress zones in specific regions |
| **Workload Burst Stimulation** | 📊 | Trigger animated workload spikes on selected cores |

### Control Panel

| Control | Description |
|---------|-------------|
| **Intensity Slider** | Set number of stimulation events (1-5) |
| **Speed Slider** | Control animation speed (Very Slow → Very Fast) |
| **Auto-Repeat** | Enable continuous stimulation cycles |
| **Run/Stop Buttons** | Start or stop the stimulation |

### Loading Real Data

1. Click **📂 Load JSON File**
2. Select `noxim_state.json` from the `bin` folder
3. Use the state selector buttons to switch between snapshots
4. View energy comparison charts below the grid

### Interactive Mode

1. Click **🖱️ Interactive** button
2. Click any green (task) core to stimulate a fault
3. Watch FTTM algorithm remap the task to a spare core
4. View real-time energy updates

---

## 📁 Project Structure

```
Noxim-FTTM/
├── README.md                 # This file
├── noxim/
│   ├── bin/
│   │   ├── noxim.exe         # Compiled executable
│   │   ├── fttm_gui.html     # Interactive GUI Stimulation Lab
│   │   ├── faults.txt        # Fault stimulation configuration
│   │   ├── noxim_state.json  # Stimulation output (generated)
│   │   ├── run_fttm.bat      # Helper launch script
│   │   ├── Makefile          # Build configuration
│   │   ├── setup_libs.ps1    # Dependency installer
│   │   └── fix_systemc.ps1   # SystemC fix script
│   ├── src/
│   │   ├── Main.cpp          # Entry point with FTTM integration
│   │   ├── NoximManagerCore.cpp  # FTTM algorithm implementation
│   │   ├── NoximManagerCore.h    # FTTM header
│   │   ├── NoC.cpp           # Network-on-Chip implementation
│   │   ├── Router.cpp        # Router with MNOC support
│   │   ├── DataStructs.h     # Task and CoreStatus definitions
│   │   └── ...               # Other Noxim source files
│   ├── config_examples/
│   │   ├── default_config.yaml   # Default 4x4 mesh configuration
│   │   └── ...               # Other configuration examples
│   └── doc/
│       ├── LICENSE.txt       # GPL License
│       └── MANUAL.txt        # Noxim manual
├── reference_fttm/           # Python reference implementation
│   ├── fttm_mapper.py        # FTTM algorithm in Python
│   ├── noc_simulator.py      # NoC model in Python
│   ├── main.py               # Python entry point
│   ├── stress_test.py        # Stress testing script
│   └── comparison.py         # FTTM vs Random comparison
└── libs/                     # External libraries (SystemC)
```

---

## 🧠 How It Works

### The FTTM Algorithm

1. **Initial Mapping**: Tasks are mapped to cores sequentially (Task 0 → Core 0, Task 1 → Core 1, etc.)

2. **Fault Detection**: When a core fails, the FTTM ManagerCore detects it

3. **Best Spare Selection**: FTTM finds the optimal spare core by minimizing:
   ```
   Energy = Σ (communication_volume × manhattan_distance)
   ```
   for all communication partners

4. **Task Remapping**: The displaced task is moved to the selected spare core

5. **State Update**: The new mapping is recorded and energy is recalculated

### Energy Calculation

The Manhattan Distance formula calculates communication cost:

```
distance = |x1 - x2| + |y1 - y2|
energy = Σ (volume_to_partner × distance_to_partner)
```

This ensures tasks are remapped to cores that minimize total communication overhead.

---

## 🔧 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **"complete binding failed"** | Known SystemC warning, automatically suppressed in Main.cpp |
| **"ld returned 1 exit status"** | Run `mingw32-make -B` for a full rebuild |
| **SystemC download fails** | Run `.\fix_systemc.ps1` after setup |
| **GUI doesn't load data** | Ensure `noxim_state.json` exists and is valid JSON |
| **No faults in output** | Check `faults.txt` format: one `x,y` pair per line |

### Rebuilding from Scratch

If you encounter persistent issues:

```powershell
# Clean build directory
Remove-Item -Recurse build -Force
mingw32-make clean

# Rebuild
mingw32-make -B
```

### Checking Build Environment

```powershell
# Verify MinGW is in PATH
where g++

# Verify make is available
where mingw32-make
```

---

## 📚 References

1. **Research Paper**: *"Enhancing Reliability and Energy Efficiency in Many-Core Processors Through Fault-Tolerant Network-on-Chip"*

2. **Noxim Citation**: Catania V., Mineo A., Monteleone S., Palesi M., and Patti D. (2016) *Cycle-Accurate Network on Chip Simulation with Noxim*. ACM Trans. Model. Comput. Simul. 27, 1, Article 4.

---

## 👥 Credits

### Development Team

| Role | Name | GitHub |
|------|------|--------|
| **Developer** | Abdullah Mehmood | [@Abdullah-Mehmood-242](https://github.com/Abdullah-Mehmood-242/) |
| **Developer** | Ammad Younas | [@Ammad-Younas](https://github.com/Ammad-Younas) |

### Supervision

- **Ms. Adeeba Aslam** - Lecturer, The University of Lahore (Sargodha Campus)

### Original Noxim

- **University of Catania, Italy** - Original Noxim NoC Simulator

---

## 📄 License

This project is licensed under the GPL License - see [LICENSE.txt](noxim/doc/LICENSE.txt) for details.

---

<div align="center">

**⭐ Star this repo if you found it helpful! ⭐**

*FTTM Network Stimulation Lab - Operating System Course Project*

</div>