@echo off
REM ================================================
REM  Restart Docker sa Gmail SMTP Konfiguracijom
REM ================================================

echo.
echo ================================================
echo   RESTARTOVANJE SERVISA SA GMAIL SMTP
echo ================================================
echo.
echo Zaustavlja sve Docker servise i pokrece ponovo...
echo.

REM Zaustavi sve servise
echo [1/2] Zaustavljanje servisa...
docker-compose down

echo.
echo [2/2] Pokretanje servisa sa Gmail konfiguracijom...
docker-compose up -d

echo.
echo ================================================
echo   SERVISI POKRENUTI!
echo ================================================
echo.
echo Aplikacija koristi Gmail SMTP:
echo   - Email: drsprojekat30@gmail.com
echo   - Status: Aktivno
echo.
echo Pristup aplikaciji:
echo   - Client:   http://localhost:5173
echo   - Server:   http://localhost:5000
echo   - Flight:   http://localhost:5001
echo.
echo Provera logova:
echo   docker-compose logs -f server
echo.
echo ================================================

pause
