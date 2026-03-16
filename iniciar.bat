@echo off
cd /d %~dp0
call myenv\Scripts\activate
start http://127.0.0.1:8000
python manage.py runserver 127.0.0.1:8000