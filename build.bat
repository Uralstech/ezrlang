@echo off
title ezr builder

cls
pyinstaller ezrShell.spec --clean --distpath ./Builds --workpath ./Temp