@echo off
pyinstaller -w -i trans.ico trans.py
copy /Y trans.ico dist\trans\