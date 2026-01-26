# Flight Booking System - Distributed Application

Distributed flight booking system with microservices architecture built with Flask, React, MySQL, Redis, and Docker.

## 📧 Email Configuration Status

**✅ CONFIGURED**: This project sends **real emails** via Gmail SMTP.

- **Email Account**: `drsprojekat30@gmail.com`
- **Status**: Active and configured
- **Critical Fix**: App Password must be **without spaces** in `.env` file
- **See**: [RESENJE_EMAIL_PROBLEMA.md](./RESENJE_EMAIL_PROBLEMA.md) for complete fix details
- **Test**: Run `test-email.bat` to verify email functionality

---

## 🏗️ Architecture

### Components:
1. **Server (Flask)** - Main backend service
   - User authentication & management
   - Airline management
   - JWT authentication with Redis
   - Email notifications
   - WebSocket support

2. **Flight Service (Flask)** - Microservice for flights
   - Flight CRUD operations
   - Booking management with async processing (multiprocessing)
   - Rating system
   - WebSocket notifications

3. **Client (React + Vite)** - Frontend application
   - User interface
   - Real-time updates via WebSocket
   - Role-based access control

4. **Database 1 (MySQL)** - Server database
   - Users, Airlines, Login Attempts

5. **Database 2 (MySQL)** - Flight Service database
   - Flights, Bookings, Ratings

6. **Redis** - Caching and session storage
   - JWT token blacklist
   - Account lockout tracking
   - Caching

## 🚀 Quick Start

### Prerequisites
- Docker
- Docker Compose

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd flight-booking-system
```

2. **Start all services:**

   **Option A - Use restart script (Windows):**
   ```bash
   RESTART.bat
   ```

   **Option B - Manual start:**
   ```bash
   docker-compose up --build -d
   ```

3. **Verify services are running:**
   ```bash
   docker-compose ps
   ```
   All services should show status "Up"

2. Start all services:
```bash
docker-compose up --build
```

3. Access the application:
   - Client: http://localhost:5173
   - Server API: http://localhost:5000
   - Flight Service API: http://localhost:5001

### Default Admin Account
After starting the services, you can create an admin account by registering a user and then manually updating the role in the database, or use the API.

## 📋 Features

### User Roles

1. **KORISNIK (Regular User)**
   - Register and login
   - Browse flights (Upcoming, In Progress, Completed)
   - Book flights
   - Rate completed flights
   - Manage account balance
   - View booking history

2. **MENADŽER (Manager)**
   - All KORISNIK features
   - Create new flights
   - Edit rejected flights and resubmit
   - View all created flights

3. **ADMINISTRATOR (Admin)**
   - All KORISNIK features
   - Approve/reject pending flights
   - Manage users (change roles, delete users)
   - Receive real-time notifications for new flights
   - Cancel flights

### Key Features

- **JWT Authentication** with 3-attempt lockout (15 minutes)
- **Async Booking Processing** using multiprocessing (5-second simulation)
- **Real-time WebSocket** notifications for admins
- **Redis Caching** for JWT blacklist and user lockout
- **Email Notifications** for role changes and flight cancellations
- **Flight Status Tracking**:
  - Upcoming flights
  - In-progress flights (with real-time countdown timer)
  - Completed/Cancelled flights
- **Rating System** (1-5 stars) for completed flights

## 🛠️ Development

### Running Services Individually

#### Server
```bash
cd server
pip install -r requirements.txt
cp .env.example .env
# Update .env with your configuration
python run.py
```

#### Flight Service
```bash
cd flight-service
pip install -r requirements.txt
cp .env.example .env
# Update .env with your configuration
python run.py
```

#### Client
```bash
cd client
npm install
npm run dev
```

## 📁 Project Structure
```
flight-booking-system/
├── server/                 # Main backend service
│   ├── app/
│   │   ├── models/        # User, Airline, LoginAttempt
│   │   ├── routes/        # API endpoints
│   │   ├── services/      # Business logic
│   │   ├── dto/           # Data Transfer Objects
│   │   └── utils/         # Validators, decorators
│   ├── config/
│   ├── requirements.txt
│   └── run.py
│
├── flight-service/        # Flight microservice
│   ├── app/
│   │   ├── models/        # Flight, Booking, Rating
│   │   ├── routes/        # API endpoints
│   │   ├── services/      # Business logic
│   │   ├── dto/           # Data Transfer Objects
│   │   └── utils/         # Async tasks (multiprocessing)
│   ├── config/
│   ├── requirements.txt
│   └── run.py
│
├── client/                # React frontend
│   ├── src/
│   │   ├── components/   # Reusable components
│   │   ├── context/      # React Context (Auth, Socket)
│   │   ├── hooks/        # Custom hooks
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   └── utils/        # Formatters, validators
│   ├── package.json
│   └── vite.config.js
│
└── docker-compose.yml     # Docker orchestration
```

## 🔌 API Endpoints

### Server (Port 5000)

#### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user

#### Users
- `GET /api/users` - Get all users (admin)
- `GET /api/users/:id` - Get user by ID
- `PUT /api/users/:id` - Update user
- `DELETE /api/users/:id` - Delete user (admin)
- `PUT /api/users/:id/role` - Update user role (admin)
- `POST /api/users/:id/balance` - Add balance

#### Airlines
- `POST /api/airlines` - Create airline (manager)
- `GET /api/airlines` - Get all airlines
- `GET /api/airlines/:id` - Get airline by ID
- `PUT /api/airlines/:id` - Update airline (manager)
- `DELETE /api/airlines/:id` - Delete airline (admin)

### Flight Service (Port 5001)

#### Flights
- `POST /api/flights` - Create flight (manager)
- `GET /api/flights` - Get all flights
- `GET /api/flights/tabs` - Get flights by tabs
- `GET /api/flights/pending` - Get pending flights (admin)
- `GET /api/flights/:id` - Get flight by ID
- `POST /api/flights/:id/approve` - Approve/reject flight (admin)
- `PUT /api/flights/:id` - Update flight (manager, rejected only)
- `POST /api/flights/:id/cancel` - Cancel flight (admin)

#### Bookings
- `POST /api/bookings` - Create booking
- `GET /api/bookings/:id` - Get booking by ID
- `GET /api/bookings/user/:userId` - Get user bookings
- `GET /api/bookings/flight/:flightId` - Get flight bookings

#### Ratings
- `POST /api/ratings` - Create rating
- `GET /api/ratings/:id` - Get rating by ID
- `GET /api/ratings/flight/:flightId` - Get flight ratings
- `GET /api/ratings` - Get all ratings (admin)

## 🧪 Testing

### Manual Testing Steps

1. **Register & Login**
   - Register a new user
   - Login with credentials
   - Verify JWT token storage

2. **Book a Flight**
   - Browse upcoming flights
   - Add balance to account
   - Book a flight
   - Wait 5 seconds for async processing
   - Verify booking status changes to COMPLETED

3. **Manager Workflow**
   - Create admin account and change role to MENADŽER
   - Create a new flight
   - Verify flight appears in pending list

4. **Admin Workflow**
   - Create admin account (role: ADMINISTRATOR)
   - Approve/reject pending flights
   - Change user roles
   - Receive WebSocket notifications for new flights

5. **Rate Completed Flights**
   - Complete a flight (wait for timer to finish)
   - Rate the flight (1-5 stars)
   - Add optional comment

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Check if databases are running
docker-compose ps

# View database logs
docker-compose logs db1
docker-compose logs db2

# Restart databases
docker-compose restart db1 db2
```

### Redis Connection Issues
```bash
# Check Redis status
docker-compose logs redis

# Test Redis connection
docker exec -it flight_booking_redis redis-cli ping
```

### Port Conflicts
If ports 3306, 3307, 5000, 5001, 5173, or 6379 are already in use, update the ports in `docker-compose.yml`.

## 📝 Environment Variables

See `.env.example` files in each service directory for required environment variables.

## 🔐 Security Notes

- Change default secret keys in production
- Use strong passwords for MySQL and Redis
- Enable HTTPS in production
- Implement rate limiting for API endpoints
- Use environment variables for sensitive data

## 📄 License

This project is for educational purposes.

## 👥 Contributors

- Your Name

## 🎓 University Project

This is a university project for Distributed Systems course.