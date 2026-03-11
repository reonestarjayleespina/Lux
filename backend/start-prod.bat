@echo off
REM Production startup script for LUX backend (Windows)
REM DO NOT use --reload in production

REM Load environment variables from .env if it exists
if exist .env (
    for /f "delims=" %%i in ('type .env') do set %%i
)

REM Start Uvicorn in production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
