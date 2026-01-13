# Struktura Projekta - Flight Booking System

## Root Direktorijum
```
flight-booking-system/
├── README.md                    # Glavna dokumentacija
├── .gitignore                   # Git ignore fajl
├── docker-compose.yml           # Docker orchestration
│
├── client/                      # React Frontend
│   ├── README.md
│   ├── public/                  # Statički fajlovi
│   └── src/
│       ├── components/          # React komponente
│       │   ├── Auth/           # Login, Register
│       │   ├── Flight/         # FlightCard, FlightList, FlightTabs, Timer
│       │   ├── User/           # UserProfile, UserList
│       │   └── Common/         # Navbar, Footer, Modal
│       ├── pages/              # Stranice
│       │   ├── HomePage.jsx
│       │   ├── LoginPage.jsx
│       │   ├── RegisterPage.jsx
│       │   ├── FlightsPage.jsx
│       │   ├── ProfilePage.jsx
│       │   ├── AdminPage.jsx
│       │   └── ManagerPage.jsx
│       ├── services/           # API komunikacija
│       │   ├── api.js          # Axios instance
│       │   ├── authService.js
│       │   ├── flightService.js
│       │   ├── userService.js
│       │   └── socketService.js
│       ├── hooks/              # Custom hooks
│       ├── context/            # React Context
│       ├── utils/              # Helper funkcije
│       ├── assets/             # Slike
│       ├── App.jsx
│       ├── main.jsx
│       └── index.css
│
├── server/                      # Flask Server (Port 5000)
│   ├── README.md
│   ├── app/
│   │   ├── __init__.py         # Flask app factory
│   │   ├── models/             # SQLAlchemy modeli
│   │   │   ├── __init__.py
│   │   │   ├── user.py         # Korisnik
│   │   │   └── airline.py      # Avio kompanija
│   │   ├── routes/             # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── auth.py         # /api/auth/*
│   │   │   ├── users.py        # /api/users/*
│   │   │   └── airlines.py     # /api/airlines/*
│   │   ├── services/           # Business logika
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── user_service.py
│   │   │   └── email_service.py
│   │   ├── utils/              # Helper funkcije
│   │   │   ├── __init__.py
│   │   │   ├── validators.py
│   │   │   └── decorators.py
│   │   └── dto/                # Data Transfer Objects
│   │       ├── __init__.py
│   │       ├── user_dto.py
│   │       └── auth_dto.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py           # Konfiguracija
│   ├── tests/                  # Unit testovi
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example
│   └── run.py                  # Entry point
│
└── flight-service/              # Flight Service (Port 5001)
    ├── README.md
    ├── app/
    │   ├── __init__.py         # Flask app factory
    │   ├── models/             # SQLAlchemy modeli
    │   │   ├── __init__.py
    │   │   ├── flight.py       # Let
    │   │   ├── booking.py      # Karta
    │   │   └── rating.py       # Ocena
    │   ├── routes/             # API endpoints
    │   │   ├── __init__.py
    │   │   ├── flights.py      # /api/flights/*
    │   │   ├── bookings.py     # /api/bookings/*
    │   │   └── ratings.py      # /api/ratings/*
    │   ├── services/           # Business logika
    │   │   ├── __init__.py
    │   │   ├── flight_service.py
    │   │   ├── booking_service.py
    │   │   └── rating_service.py
    │   ├── utils/              # Helper funkcije
    │   │   ├── __init__.py
    │   │   └── async_tasks.py  # Multiprocessing
    │   └── dto/                # Data Transfer Objects
    │       ├── __init__.py
    │       ├── flight_dto.py
    │       └── booking_dto.py
    ├── config/
    │   ├── __init__.py
    │   └── config.py           # Konfiguracija
    ├── tests/                  # Unit testovi
    ├── requirements.txt        # Python dependencies
    ├── .env.example
    └── run.py                  # Entry point
```

## Baze Podataka

### DB1 (MySQL Port 3306) - Server Database
Tabele:
- `users` - Korisnici
- `airlines` - Avio kompanije
- `login_attempts` - Neuspešni pokušaji prijave

### DB2 (MySQL Port 3307) - Flight Service Database
Tabele:
- `flights` - Letovi
- `bookings` - Kupljene karte
- `ratings` - Ocene letova

## Redis (Port 6379)
- Keš za korisnike
- JWT blacklist
- Blokada naloga

## Portovi
- Client: 5173
- Server: 5000
- Flight Service: 5001
- DB1 (MySQL): 3306
- DB2 (MySQL): 3307
- Redis: 6379
