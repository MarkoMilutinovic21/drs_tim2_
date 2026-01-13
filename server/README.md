# Server - Flask Backend

Glavni backend servis koji upravlja korisnicima, autentifikacijom i avio kompanijama.

## Port
`5000`

## Struktura

```
server/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models/              # SQLAlchemy modeli
│   │   ├── __init__.py
│   │   ├── user.py          # User model
│   │   └── airline.py       # Airline model
│   ├── routes/              # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py          # /api/auth/*
│   │   ├── users.py         # /api/users/*
│   │   └── airlines.py      # /api/airlines/*
│   ├── services/            # Business logika
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   └── email_service.py
│   ├── utils/               # Helper funkcije
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   └── decorators.py
│   └── dto/                 # Data Transfer Objects
│       ├── __init__.py
│       ├── user_dto.py
│       └── auth_dto.py
├── config/
│   ├── __init__.py
│   └── config.py            # Konfiguracija
├── tests/                   # Unit testovi
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
└── run.py                  # Entry point
```

## Odgovornosti

### Autentifikacija
- JWT token generisanje i validacija
- Login/Logout
- Blokada naloga (3 neuspešna pokušaja)

### Korisnici
- Registracija
- CRUD operacije
- Upravljanje ulogama (Admin)
- Upload slike profila

### Avio Kompanije
- CRUD operacije
- Dropdown lista za frontend

## Baza Podataka 1 (MySQL)

### Tabele:
- **users**: Korisnici sistema
- **airlines**: Avio kompanije
- **login_attempts**: Praćenje neuspešnih pokušaja

## Redis Keš

Koristi se za:
- Caching korisničkih podataka
- Blacklist za odjavljene JWT tokene
- Blokada naloga

## Dependencies

```
Flask
Flask-SQLAlchemy
Flask-JWT-Extended
Flask-SocketIO
Flask-Mail
Flask-Cors
PyMySQL
Redis
Bcrypt
Python-dotenv
```

## Pokretanje

```bash
# Kreirati virtualno okruženje
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalirati dependencies
pip install -r requirements.txt

# Pokrenuti
python run.py
```
