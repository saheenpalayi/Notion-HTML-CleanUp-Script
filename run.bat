@echo off

:loop
python HTML-CleanUP-Script.py
echo.
choice /c RC /m "Press R to restart or C to close the window: "
if errorlevel 2 goto close
goto loop

:close
exit
