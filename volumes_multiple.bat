@echo off
for %%a in ("%~1") do (
    echo Run on multiple volumes: %%~a
    "%~dp0py310-embed\python.exe" "%~dp0mokuro" --disable_confirmation --parent_dir "%%~a" --as_one_file False 
)
pause
