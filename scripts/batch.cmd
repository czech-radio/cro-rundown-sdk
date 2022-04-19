@echo off
@REM https://ss64.com/nt/for_l.html

FOR %%i IN (21, 22, 23, 24, 25, 26) DO start /b cro.rundown.clean -s \\cro.cz\srv\annova\export-avo\TEST\2020\W%%i
