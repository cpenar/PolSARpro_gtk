REM @echo off

cd c:\msys64

set MSYSTEM=MINGW64
set _TERM=usr/bin/mintty --option AppId=msys2 -i /msys2.ico
set _SH=usr/bin/bash --login -i -c
set _PSP_dir=~/work/PolSARpro_gtk/src/ui/
set _PSP_exe=./main.py


start /min %_TERM% %_SH% "cd %_PSP_dir% ; %_PSP_exe%"
