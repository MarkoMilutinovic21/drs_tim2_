@echo off
echo ================================================
echo   TEST EMAIL SLANJA - Flight Booking System
echo ================================================
echo.
echo Ova skripta testira da li email slanje radi.
echo.
echo INSTRUKCIJE:
echo 1. Otvori aplikaciju: http://localhost:5173
echo 2. Uloguj se kao admin (admin@test.com / admin123)
echo 3. Idi na Admin Dashboard - Users
echo 4. Promeni ulogu nekog korisnika
echo 5. Proveri inbox na email adresi tog korisnika
echo.
echo ================================================
echo   PROVERA LOGOVA
echo ================================================
echo.

echo [1/3] Proveravamo da li server kontejner radi...
docker-compose ps | findstr "server"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Server kontejner nije pokrenut!
    echo Pokrenite: docker-compose up -d
    pause
    exit /b 1
)
echo [OK] Server kontejner radi.
echo.

echo [2/3] Proveravamo Gmail SMTP kredencijale...
docker-compose exec server env | findstr "MAIL_"
echo.
echo Proverite da li je MAIL_PASSWORD bez razmaka!
echo Ispravno:   MAIL_PASSWORD=dszyvqfkoqqwfshq
echo Neispravno: MAIL_PASSWORD=dszy vqfk oqqw fshq
echo.
pause

echo [3/3] Proveravamo server logove za email greske...
echo.
docker-compose logs server --tail=100 | findstr /i "email error failed"
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [WARNING] Pronadjene greske u logu!
    echo Pogledajte logove iznad.
) else (
    echo [OK] Nema grešaka u logovima.
)
echo.

echo ================================================
echo   GOTOVO!
echo ================================================
echo.
echo Sada testirati rucno:
echo 1. Otvori http://localhost:5173
echo 2. Uloguj se kao admin
echo 3. Promeni ulogu korisnika
echo 4. Proveri email inbox
echo.
pause
