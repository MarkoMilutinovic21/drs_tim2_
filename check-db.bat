@echo off
echo ============================================
echo DATABASE VIEWER - Flight Booking System
echo ============================================
echo.

:menu
echo.
echo Choose an option:
echo 1. View all users
echo 2. View all flights
echo 3. View all bookings
echo 4. View all ratings
echo 5. View login attempts
echo 6. View airlines
echo 7. Custom SQL query (DB1 - Users)
echo 8. Custom SQL query (DB2 - Flights)
echo 9. Exit
echo.
set /p choice="Enter your choice (1-9): "

if "%choice%"=="1" goto users
if "%choice%"=="2" goto flights
if "%choice%"=="3" goto bookings
if "%choice%"=="4" goto ratings
if "%choice%"=="5" goto login_attempts
if "%choice%"=="6" goto airlines
if "%choice%"=="7" goto custom1
if "%choice%"=="8" goto custom2
if "%choice%"=="9" goto end
goto menu

:users
echo.
echo ========== ALL USERS ==========
docker exec flight_booking_db1 mysql -u flight_user -pflight_password flight_booking_db -e "SELECT id, first_name, last_name, email, role, account_balance FROM users;" 2>nul
goto menu

:flights
echo.
echo ========== ALL FLIGHTS ==========
docker exec flight_booking_db2 mysql -u flight_user -pflight_password flight_service_db -e "SELECT id, name, status, departure_airport, arrival_airport, departure_time, ticket_price FROM flights;" 2>nul
goto menu

:bookings
echo.
echo ========== ALL BOOKINGS ==========
docker exec flight_booking_db2 mysql -u flight_user -pflight_password flight_service_db -e "SELECT * FROM bookings;" 2>nul
goto menu

:ratings
echo.
echo ========== ALL RATINGS ==========
docker exec flight_booking_db2 mysql -u flight_user -pflight_password flight_service_db -e "SELECT * FROM ratings;" 2>nul
goto menu

:login_attempts
echo.
echo ========== LOGIN ATTEMPTS ==========
docker exec flight_booking_db1 mysql -u flight_user -pflight_password flight_booking_db -e "SELECT * FROM login_attempts ORDER BY attempted_at DESC LIMIT 10;" 2>nul
goto menu

:airlines
echo.
echo ========== AIRLINES ==========
docker exec flight_booking_db1 mysql -u flight_user -pflight_password flight_booking_db -e "SELECT * FROM airlines;" 2>nul
goto menu

:custom1
echo.
set /p query="Enter SQL query for DB1: "
docker exec flight_booking_db1 mysql -u flight_user -pflight_password flight_booking_db -e "%query%" 2>nul
goto menu

:custom2
echo.
set /p query="Enter SQL query for DB2: "
docker exec flight_booking_db2 mysql -u flight_user -pflight_password flight_service_db -e "%query%" 2>nul
goto menu

:end
echo.
echo Goodbye!
pause
