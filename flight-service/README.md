# Flight Service - Flask Mikroservis

Mikroservis zadužen za upravljanje letovima i asinhronom obradom kupovine karata.

## Port
`5001`

## Struktura

```
flight-service/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models/              # SQLAlchemy modeli
│   │   ├── __init__.py
│   │   ├── flight.py        # Flight model
│   │   ├── booking.py       # Booking model
│   │   └── rating.py        # Rating model
│   ├── routes/              # API endpoints
│   │   ├── __init__.py
│   │   ├── flights.py       # /api/flights/*
│   │   ├── bookings.py      # /api/bookings/*
│   │   └── ratings.py       # /api/ratings/*
│   ├── services/            # Business logika
│   │   ├── __init__.py
│   │   ├── flight_service.py
│   │   ├── booking_service.py
│   │   └── rating_service.py
│   ├── utils/               # Helper funkcije
│   │   ├── __init__.py
│   │   └── async_tasks.py   # Multiprocessing
│   └── dto/                 # Data Transfer Objects
│       ├── __init__.py
│       ├── flight_dto.py
│       └── booking_dto.py
├── config/
│   ├── __init__.py
│   └── config.py            # Konfiguracija
├── tests/                   # Unit testovi
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
└── run.py                  # Entry point
```

## Odgovornosti

### Letovi
- Kreiranje letova (MENADŽER)
- CRUD operacije
- Pretraga i filtriranje
- 3 taba: Predstojeci, U toku, Završeni/Otkazani
- Tajmer za letove u toku

### Kupovina Karata
- **Asinhrona obrada** (Multiprocessing)
- Provera stanja na računu
- Kreiranje booking zapisa

### Ocene
- Ocenjivanje završenih letova (1-5)
- Prikaz ocena (ADMIN)

### PDF Izvještaji
- Generisanje PDF-a za sve tabove
- Slanje na email

## Baza Podataka 2 (MySQL)

### Tabele:
- **flights**: Letovi
- **bookings**: Kupljene karte
- **ratings**: Ocene letova

## Komunikacija

### Sa Server-om:
- REST API pozivi
- WebSocket (real-time notifikacije)

## Procesi

Koriste se za:
- Asinhronom obradu kupovine karata (sleep simulira duže trajanje)
- Generisanje PDF izvještaja

## Dependencies

```
Flask
Flask-SQLAlchemy
Flask-SocketIO
Flask-Cors
PyMySQL
ReportLab (PDF generisanje)
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
