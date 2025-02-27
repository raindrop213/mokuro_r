@echo off
for %%a in ("%~1") do (
    echo Run on one volume: %%~a
    "%~dp0py310-embed\python.exe" "%~dp0mokuro" --disable_confirmation --as_one_file False "%%~a"
)
pause
