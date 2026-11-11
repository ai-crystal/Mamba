@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

rem 优先使用 py 启动器，其次 python，最后常见安装路径
set PY=
where py >nul 2>nul && set PY=py
if not defined PY (where python >nul 2>nul && set PY=python)
if not defined PY if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set PY="%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not defined PY if exist "C:\Python312\python.exe" set PY="C:\Python312\python.exe"

if not defined PY (
  echo 未找到 Python，请安装 Python 3.10 及以上版本并加入 PATH。
  pause
  exit /b 1
)

echo [1/4] 生成入门版插图 ...
%PY% "books\intro\code\make_all.py"
if errorlevel 1 goto :err
%PY% "books\intro\code\make_covers.py"
if errorlevel 1 goto :err

echo [2/4] 生成专业版插图 ...
%PY% "books\pro\code\make_all.py"
if errorlevel 1 goto :err
%PY% "books\pro\code\make_covers.py"
if errorlevel 1 goto :err

echo [3/4] 排版入门版 ...
%PY% "books\build\build_pdf.py" --book intro
if errorlevel 1 goto :err

echo [4/4] 排版专业版 ...
%PY% "books\build\build_pdf.py" --book pro
if errorlevel 1 goto :err

echo.
echo 完成：
echo   output\mamba-intro.pdf
echo   output\from-lssl-to-mamba3.pdf
pause
exit /b 0

:err
echo.
echo 构建失败，请查看上面的错误信息。
pause
exit /b 1
