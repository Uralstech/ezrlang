@echo off
title ezr builder

cls
pyinstaller ezrShell.spec
pause

cls
cd dist\ezrShell
ezrShell.exe