@echo off
echo Running %~n0% from: %cd%
cd ..
python "wsgi.py"
pause