@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

set "TARGET=%~1"
if "%TARGET%"=="" set "TARGET=all"
set "OPT=%~2"

rem --- locate python -------------------------------------------------
set "PY="
where py >nul 2>nul && set "PY=py"
if not defined PY (where python >nul 2>nul && set "PY=python")
if not defined PY if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not defined PY if exist "C:\Python312\python.exe" set "PY=C:\Python312\python.exe"
if not defined PY goto :nopython

rem --- dispatch ------------------------------------------------------
if /i "%TARGET%"=="all" goto :all
if /i "%TARGET%"=="intro" goto :intro
if /i "%TARGET%"=="pro" goto :pro
if /i "%TARGET%"=="figures" goto :figures
echo.
echo Unknown target: %TARGET%
echo Usage: build.bat [all^|intro^|pro^|figures] [no-opt]
pause
exit /b 1

:all
call :book intro
if errorlevel 1 goto :err
call :book pro
if errorlevel 1 goto :err
echo.
echo Done: output\mamba-intro.pdf  output\from-lssl-to-mamba3.pdf
pause
exit /b 0

:intro
call :book intro
if errorlevel 1 goto :err
echo.
echo Done: output\mamba-intro.pdf
pause
exit /b 0

:pro
call :book pro
if errorlevel 1 goto :err
echo.
echo Done: output\from-lssl-to-mamba3.pdf
pause
exit /b 0

:figures
echo [1/2] redraw figures: intro
"%PY%" "books\intro\code\make_all.py"
if errorlevel 1 goto :err
"%PY%" "books\intro\code\make_covers.py"
if errorlevel 1 goto :err
echo [2/2] redraw figures: pro
"%PY%" "books\pro\code\make_all.py"
if errorlevel 1 goto :err
"%PY%" "books\pro\code\make_covers.py"
if errorlevel 1 goto :err
echo.
echo Figures updated.
pause
exit /b 0

rem --- one book: check first, then typeset ---------------------------
:book
set "BOOK=%~1"
echo.
echo ==== %BOOK% : check ====
"%PY%" "books\build\check.py" %BOOK%
if errorlevel 1 exit /b 1
echo ==== %BOOK% : build ====
if /i "%OPT%"=="no-opt" (
  "%PY%" "books\build\build_pdf.py" --book %BOOK% --no-opt
) else (
  "%PY%" "books\build\build_pdf.py" --book %BOOK%
)
if errorlevel 1 exit /b 1
exit /b 0

:nopython
echo.
echo Python 3.10+ not found. Install it and add it to PATH.
pause
exit /b 1

:err
echo.
echo Build failed. Read the messages above.
pause
exit /b 1
