@echo off
REM FTTM Noxim Launcher with Custom Faults
REM Usage: run_fttm.bat [fault1] [fault2] [fault3] ...
REM Example: run_fttm.bat 0,0 1,1 2,0

echo ========================================
echo   FTTM-Noxim Simulator Launcher
echo ========================================
echo.

REM Clear old faults file
if exist faults.txt del faults.txt

REM If arguments provided, create faults.txt from them
if "%~1"=="" (
    echo No faults specified. Running with default faults.txt if exists.
) else (
    echo Creating faults.txt with specified faults:
    (
        echo # Auto-generated fault configuration
        for %%a in (%*) do (
            echo %%a
            echo   - %%a
        )
    ) > faults.txt
    echo.
)

echo Running Noxim simulator...
echo.

noxim.exe -config ../config_examples/default_config.yaml

echo.
echo Simulation complete!
echo Output saved to noxim_state.json
echo.
echo Opening GUI...
start fttm_gui.html

pause
