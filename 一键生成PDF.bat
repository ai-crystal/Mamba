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

echo [1/2] 生成插图 ...
%PY% "book\code\make_all.py"
if errorlevel 1 goto :err
%PY% "book\code\make_covers.py"
if errorlevel 1 goto :err

echo [2/2] 排版并输出 PDF ...
%PY% "book\build\build_pdf.py"
if errorlevel 1 goto :err

echo.
echo 完成：output\from-lssl-to-mamba3.pdf
pause
exit /b 0

:err
echo.
echo 构建失败，请查看上面的错误信息。
pause
exit /b 1
