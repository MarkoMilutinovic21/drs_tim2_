@echo off
REM ================================================
REM  RESTART DOCKER SA GMAIL SMTP
REM ================================================

echo.
echo ================================================
echo   FLIGHT BOOKING SYSTEM - RESTART
echo   Gmail SMTP: drsprojekat30@gmail.com
echo ================================================
echo.

echo [1/3] Zaustavljanje servisa...
docker-compose down

echo.
echo [2/3] Pokretanje servisa...
docker-compose up -d

echo.
echo [3/3] Cekanje da servisi startuju...
timeout /t 10 /nobreak >nul

echo.
echo ================================================
echo   STATUS SERVISA
echo ================================================
docker-compose ps

echo.
echo ================================================
echo   PROVERA GMAIL KONFIGURACIJE
echo ================================================
echo.
docker-compose exec server env | findstr MAIL_USERNAME
docker-compose exec server env | findstr MAIL_SERVER

echo.
echo ================================================
echo   SERVISI POKRENUTI!
echo ================================================
echo.
echo Aplikacija:  http://localhost:5173
echo Server API:  http://localhost:5000
echo Flight API:  http://localhost:5001
echo.
echo Za logove servera:
echo   docker-compose logs -f server
echo.
echo Za testiranje email-a:
echo   1. Uloguj se kao admin
echo   2. Promeni ulogu korisnika
echo   3. Proveri inbox korisnika
echo.
echo ================================================

pause
