# Client - React Frontend

React aplikacija sa Vite build toolom.

## Port
`5173` (development)

## Struktura

```
client/
├── public/                  # Statički fajlovi
├── src/
│   ├── components/          # React komponente
│   │   ├── Auth/
│   │   │   ├── LoginForm.jsx
│   │   │   └── RegisterForm.jsx
│   │   ├── Flight/
│   │   │   ├── FlightCard.jsx
│   │   │   ├── FlightList.jsx
│   │   │   ├── FlightTabs.jsx
│   │   │   └── FlightTimer.jsx
│   │   ├── User/
│   │   │   ├── UserProfile.jsx
│   │   │   └── UserList.jsx
│   │   └── Common/
│   │       ├── Navbar.jsx
│   │       ├── Footer.jsx
│   │       └── Modal.jsx
│   ├── pages/               # Stranice
│   │   ├── HomePage.jsx
│   │   ├── LoginPage.jsx
│   │   ├── RegisterPage.jsx
│   │   ├── FlightsPage.jsx
│   │   ├── ProfilePage.jsx
│   │   ├── AdminPage.jsx
│   │   └── ManagerPage.jsx
│   ├── services/            # API komunikacija
│   │   ├── api.js           # Axios instance
│   │   ├── authService.js
│   │   ├── flightService.js
│   │   ├── userService.js
│   │   └── socketService.js # WebSocket
│   ├── hooks/               # Custom hooks
│   │   ├── useAuth.js
│   │   ├── useSocket.js
│   │   └── useFlights.js
│   ├── context/             # React Context
│   │   ├── AuthContext.jsx
│   │   └── SocketContext.jsx
│   ├── utils/               # Helper funkcije
│   │   ├── validators.js
│   │   └── formatters.js
│   ├── assets/              # Slike, ikone
│   ├── App.jsx              # Root komponenta
│   ├── main.jsx             # Entry point
│   └── index.css            # Global styles
├── .env.example             # Environment template
├── package.json
├── vite.config.js
└── README.md
```

## Funkcionalnosti

### Autentifikacija
- Login/Logout forme
- JWT token storage (localStorage)
- Protected routes

### Korisnici
- Registracija
- Profil (prikaz i izmena)
- Upload slike
- Uplata na račun

### Letovi
- **3 Taba**:
  1. Predstojeci letovi
  2. Letovi u toku (sa tajmerom)
  3. Završeni/Otkazani letovi
- Pretraga po imenu
- Filter po avio kompaniji (dropdown)
- Kupovina karata
- Ocenjivanje

### Admin Panel
- Odobravanje/Odbijanje letova (WebSocket notifikacije)
- Upravljanje korisnicima
- Prikaz ocena
- Generisanje PDF izvještaja

### Manager Panel
- Kreiranje letova
- Kreiranje avio kompanija

### Real-time
- WebSocket notifikacije za nove letove (Admin)
- Live update statusa leta

## Dependencies

```json
{
  "react": "^18.3.1",
  "react-dom": "^18.3.1",
  "react-router-dom": "^6.x",
  "axios": "^1.x",
  "socket.io-client": "^4.x",
  "tailwindcss": "^3.x"
}
```

## Pokretanje

```bash
# Instalirati dependencies
npm install

# Development mode
npm run dev

# Build za production
npm run build

# Preview production build
npm run preview
```

## Environment Variables

```
VITE_API_URL=http://localhost:5000
VITE_FLIGHT_SERVICE_URL=http://localhost:5001
VITE_SOCKET_URL=http://localhost:5000
```

## Routing

```
/               - Home page
/login          - Login
/register       - Register
/flights        - Letovi (3 taba)
/profile        - User profil
/admin          - Admin panel
/manager        - Manager panel
```
