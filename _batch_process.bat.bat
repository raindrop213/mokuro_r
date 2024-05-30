@echo off
setlocal
echo Processing folder: %1
call .venv\Scripts\activate
mokuro --disable_confirmation --parent_dir "%1" --as_one_file False
echo Done.
pause