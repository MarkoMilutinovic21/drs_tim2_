@echo off
echo ================================================
echo   EMAIL DIJAGNOSTIKA - Flight Booking System
echo ================================================
echo.
echo Ova skripta testira Gmail SMTP konekciju.
echo.

echo [1/3] Proveravam Docker kontejnere...
docker-compose ps | findstr "server"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Server kontejner nije pokrenut!
    echo Pokrenite: docker-compose up -d
    pause
    exit /b 1
)
echo [OK] Server kontejner radi.
echo.

echo [2/3] Proveravam MAIL_PASSWORD environment varijablu...
docker-compose exec server printenv MAIL_PASSWORD > temp_pass.txt 2>&1
type temp_pass.txt
del temp_pass.txt
echo.
pause

echo [3/3] Testiram Gmail SMTP konekciju...
echo Kopiram test skriptu u kontejner...
docker cp test_gmail.py flight_booking_server:/app/test_gmail.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Nije moguce kopirati test skriptu!
    pause
    exit /b 1
)
echo.

echo Pokrecem test...
echo.
docker-compose exec server python test_gmail.py
echo.

echo ================================================
echo   DIJAGNOSTIKA ZAVRSENA
echo ================================================
echo.
echo Ako vidite:
echo   "SUCCESS! Login successful!" = Gmail kredencijali su ISPRAVNI
echo   "AUTHENTICATION ERROR" = App Password je NEISPRAVAN
echo.
echo Ako je App Password neispravan:
echo   1. Idi na https://myaccount.google.com/apppasswords
echo   2. Generiši NOVI App Password
echo   3. Kopiraj password BEZ razmaka
echo   4. Ažuriraj server/.env fajl
echo   5. Pokreni: docker-compose down ^&^& docker-compose up -d
echo.
echo Detaljno uputstvo: DIJAGNOZA_EMAIL_PROBLEMA.md
echo.
pause
