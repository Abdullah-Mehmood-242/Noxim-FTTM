$ErrorActionPreference = "Stop"

# Go to the libs folder
Set-Location "C:\Users\abdul\Desktop\Noxim\noxim\bin\libs"

# 1. DELETE the corrupt folder
Write-Host ">>> Deleting corrupt SystemC folder..." -ForegroundColor Yellow
if (Test-Path "systemc-2.3.1") { 
    Remove-Item -Recurse -Force "systemc-2.3.1" 
}

# 2. DOWNLOAD (Shallow Clone - Much Faster)
Write-Host ">>> Downloading SystemC (Lightweight/Shallow)..." -ForegroundColor Cyan
try {
    # --depth 1 is the magic flag here
    git clone --depth 1 --branch 2.3.3 https://github.com/accellera-official/systemc.git systemc-2.3.1
} catch {
    Write-Host "Download failed again. Check your internet." -ForegroundColor Red
    exit 1
}

# 3. BUILD
Set-Location "systemc-2.3.1"
New-Item -ItemType Directory -Force -Path "build" | Out-Null
Set-Location "build"

Write-Host ">>> Configuring SystemC..." -ForegroundColor Cyan
cmake -G "MinGW Makefiles" -DCMAKE_CXX_STANDARD=14 -DENABLE_PTHREADS=OFF -DCMAKE_BUILD_TYPE=Release ..

Write-Host ">>> Compiling SystemC (Wait for it)..." -ForegroundColor Cyan
mingw32-make -j4

# 4. INSTALL (Move files where Noxim expects them)
Set-Location ..
New-Item -ItemType Directory -Force -Path "lib-mingw" | Out-Null

# Move the library file
$libFile = Get-ChildItem -Path "build" -Recurse -Filter "libsystemc.a" | Select-Object -First 1
if ($libFile) {
    Copy-Item $libFile.FullName -Destination "lib-mingw\libsystemc.a" -Force
    Write-Host "Library placed successfully." -ForegroundColor Green
} else {
    Write-Host "CRITICAL: libsystemc.a was not created." -ForegroundColor Red
    exit 1
}

# Move the headers (Noxim needs 'include', repo has 'src')
if (-not (Test-Path "include/systemc.h")) {
    Write-Host "Fixing header files..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path "include" | Out-Null
    Copy-Item -Path "src\*" -Destination "include" -Recurse -Force
}

Write-Host ">>> SystemC Repair Complete!" -ForegroundColor Green