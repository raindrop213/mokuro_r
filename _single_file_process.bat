@echo off
setlocal
echo Processing file: %1
call .venv\Scripts\activate
mokuro --disable_confirmation "%1" --as_one_file False
echo Done.
pause

mokuro --disable_confirmation "H:\qBit\115\【マンガ】\[本名ワコウ] ノ・ゾ・キ・ア・ナ" --as_one_file False