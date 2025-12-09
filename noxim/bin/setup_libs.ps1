<#
.SYNOPSIS
    Automated dependency setup for Noxim on Windows (MinGW/MSYS).
    
.DESCRIPTION
    1. Checks for required tools (git, cmake, mingw32-make).
    2. Downloads and builds yaml-cpp.
    3. Downloads and builds SystemC.
       NOTE: SystemC 2.3.1 is extremely old and notoriously difficult to build on modern MinGW.
       This script downloads a newer, compatible version (2.3.3) but installs it into the 
       'systemc-2.3.1' folder structure so your Noxim Makefile works without modification.
    
.USAGE
    Run this script in the root 'Noxim' folder (the one containing the 'noxim' subfolder or 'src').
    ./setup_libs.ps1
#>

$ErrorActionPreference = "Stop"

function Print-Color($text, $color) {
    Write-Host $text -ForegroundColor $color
}

function Check-Command($cmd) {
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
        Print-Color "CRITICAL ERROR: '$cmd' is not installed or not in PATH." "Red"
        Print-Color "Please install it and restart PowerShell." "Red"
        exit 1
    }
}

# --- Step 0: Pre-flight Checks ---
Print-Color ">>> Step 0: Checking Environment..." "Cyan"
Check-Command "git"
Check-Command "cmake"
Check-Command "mingw32-make"
Check-Command "g++"

$rootDir = Get-Location
$libsDir = Join-Path $rootDir "libs"

if (-not (Test-Path $libsDir)) {
    New-Item -ItemType Directory -Force -Path $libsDir | Out-Null
    Print-Color "Created 'libs' directory." "Green"
}

# --- Step 1: YAML-CPP Setup ---
Print-Color "`n>>> Step 1: Setting up YAML-CPP..." "Cyan"
$yamlDir = Join-Path $libsDir "yaml-cpp"

if (-not (Test-Path $yamlDir)) {
    Print-Color "Cloning yaml-cpp..." "Yellow"
    git clone https://github.com/jbeder/yaml-cpp.git $yamlDir
} else {
    Print-Color "yaml-cpp already present. Skipping clone." "Gray"
}

$yamlBuildDir = Join-Path $yamlDir "build"
if (-not (Test-Path $yamlBuildDir)) { New-Item -ItemType Directory -Force -Path $yamlBuildDir | Out-Null }

Push-Location $yamlBuildDir
try {
    Print-Color "Configuring YAML-CPP..." "Yellow"
    # Disable tests/tools to save time and avoid errors
    cmake -G "MinGW Makefiles" -DYAML_CPP_BUILD_TESTS=OFF -DYAML_CPP_BUILD_TOOLS=OFF ..
    
    Print-Color "Compiling YAML-CPP (This may take a minute)..." "Yellow"
    mingw32-make -j4
    
    # Organize output for Noxim Makefile structure
    # Noxim expects libs/yaml-cpp/lib/libyaml-cpp.a
    $libDest = Join-Path $yamlDir "lib"
    if (-not (Test-Path $libDest)) { New-Item -ItemType Directory -Force -Path $libDest | Out-Null }
    
    $builtLib = "libyaml-cpp.a"
    if (-not (Test-Path $builtLib)) { $builtLib = "libyaml-cppmd.a" } # Sometimes named differently
    
    Copy-Item $builtLib -Destination (Join-Path $libDest "libyaml-cpp.a") -Force
    Print-Color "YAML-CPP built and placed successfully." "Green"
} catch {
    Print-Color "Error building YAML-CPP: $_" "Red"
    Pop-Location
    exit 1
}
Pop-Location

# --- Step 2: SystemC Setup ---
Print-Color "`n>>> Step 2: Setting up SystemC..." "Cyan"
# NOTE: We use the folder name 'systemc-2.3.1' because Noxim expects it.
# However, we clone a newer stable branch because 2.3.1 is broken on modern GCC.
$syscDir = Join-Path $libsDir "systemc-2.3.1"

if (-not (Test-Path $syscDir)) {
    Print-Color "Cloning SystemC (Using official mirror)..." "Yellow"
    # Using 2.3.3 as it is the most stable version for MinGW
    git clone --branch 2.3.3 https://github.com/accellera-official/systemc.git $syscDir
} else {
    Print-Color "SystemC directory already exists. Skipping clone." "Gray"
}

$syscBuildDir = Join-Path $syscDir "build"
if (-not (Test-Path $syscBuildDir)) { New-Item -ItemType Directory -Force -Path $syscBuildDir | Out-Null }

Push-Location $syscBuildDir
try {
    Print-Color "Configuring SystemC for MinGW..." "Yellow"
    # CRITICAL: -DCMAKE_CXX_STANDARD=14 or 17 is often needed for modern GCC
    # CRITICAL: -DENABLE_PTHREADS=ON is usually required for SystemC on MinGW
    cmake -G "MinGW Makefiles" -DCMAKE_CXX_STANDARD=14 -DENABLE_PTHREADS=ON ..
    
    Print-Color "Compiling SystemC (This will take several minutes)..." "Yellow"
    mingw32-make -j4
    
    # Organize output for Noxim Makefile structure
    # Noxim expects libs/systemc-2.3.1/lib-mingw/libsystemc.a
    $syscLibDest = Join-Path $syscDir "lib-mingw"
    if (-not (Test-Path $syscLibDest)) { New-Item -ItemType Directory -Force -Path $syscLibDest | Out-Null }
    
    # Find the built library (could be in src or root of build)
    $foundLib = Get-ChildItem -Path . -Recurse -Filter "libsystemc.a" | Select-Object -First 1
    
    if ($foundLib) {
        Copy-Item $foundLib.FullName -Destination (Join-Path $syscLibDest "libsystemc.a") -Force
        Print-Color "SystemC built and placed successfully." "Green"
    } else {
        throw "Could not find 'libsystemc.a' in build folder."
    }
    
    # Ensure includes are where Noxim expects them (usually src or include)
    # The git repo usually has 'src' containing the headers. Noxim looks for 'include'.
    # We create a symlink or copy if 'include' doesn't exist populated.
    $includeDest = Join-Path $syscDir "include"
    $srcInclude  = Join-Path $syscDir "src"
    
    # If the repo uses 'src' for headers but no 'include', we copy contents of src to include
    if (-not (Test-Path (Join-Path $includeDest "systemc.h"))) {
         Print-Color "Fixing include paths..." "Yellow"
         if (-not (Test-Path $includeDest)) { New-Item -ItemType Directory -Force -Path $includeDest | Out-Null }
         Copy-Item -Path "$srcInclude\*" -Destination $includeDest -Recurse -Force
    }

} catch {
    Print-Color "Error building SystemC: $_" "Red"
    Print-Color "Ensure you have MinGW C++ (g++) installed correctly." "Red"
    Pop-Location
    exit 1
}
Pop-Location

# --- Step 3: Validation ---
Print-Color "`n>>> Step 3: Validating Setup..." "Cyan"

$path1 = Join-Path $libsDir "systemc-2.3.1/include/systemc.h"
$path2 = Join-Path $libsDir "systemc-2.3.1/lib-mingw/libsystemc.a"
$path3 = Join-Path $libsDir "yaml-cpp/lib/libyaml-cpp.a"

$missing = $false

if (-not (Test-Path $path1)) { Print-Color "MISSING: $path1" "Red"; $missing = $true }
if (-not (Test-Path $path2)) { Print-Color "MISSING: $path2" "Red"; $missing = $true }
if (-not (Test-Path $path3)) { Print-Color "MISSING: $path3" "Red"; $missing = $true }

if ($missing) {
    Print-Color "SETUP FAILED. Check the errors above." "Red"
    exit 1
} else {
    Print-Color "SUCCESS! All libraries are installed." "Green"
    Print-Color "You can now run 'mingw32-make' in your noxim/bin folder." "Green"
}