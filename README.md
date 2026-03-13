# PrimeWatch - Crypto Token Watchlist Platform

A full-stack web application for managing cryptocurrency watchlists with secure authentication and role-based access control.

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM for database interactions
- **JWT** - Stateless authentication
- **Bcrypt** - Password hashing
- **Docker** - Containerization

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client
- **React Hot Toast** - Toast notifications

## Features

### Authentication & Authorization
- User registration and login
- JWT-based authentication
- Role-Based Access Control (RBAC)
  - **User**: Can manage their own watchlist
  - **Admin**: Can view all users' watchlists

### Watchlist Management
- Create new watchlist items (token symbol, target price, notes)
- Read all watchlist items
- Update existing items
- Delete items
- Admin view of all watchlists

### Security Features
- Password hashing with Bcrypt
- JWT tokens with expiration
- Protected API endpoints
- Automatic token refresh handling
- CORS configuration

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Quick Start with Docker

1. Clone the repository
```bash
git clone <repository-url>
cd primewatch
```

2. Start the services
```bash
docker-compose up -d
```

This will start:
- PostgreSQL database on port 5432
- FastAPI backend on port 8000

3. Start the frontend (in a new terminal)
```bash
cd frontend
npm install
npm run dev
```

4. Access the application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs

### Test Accounts

You can register new accounts or use the API to create test accounts:

**Regular User:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123","role":"user"}'
```

**Admin User:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123","role":"admin"}'
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and receive JWT token

### User
- `GET /api/v1/users/me` - Get current user profile (Protected)

### Watchlist
- `POST /api/v1/watchlist/` - Create a new watchlist item (Protected)
- `GET /api/v1/watchlist/` - Get user's watchlist items (Protected)
- `PUT /api/v1/watchlist/{id}` - Update a watchlist item (Protected - Owner only)
- `DELETE /api/v1/watchlist/{id}` - Delete a watchlist item (Protected - Owner or Admin)

### Admin
- `GET /api/v1/watchlist/admin/all` - Get all watchlist items (Protected - Admin only)

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://primewatch_user:primewatch_pass@localhost:5432/primewatch_db
SECRET_KEY=primewatch_dev_secret_key_123456789_change_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
CORS_ORIGINS=["http://localhost:3000"]
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Security Considerations

### Production Deployment
- Change the `SECRET_KEY` in .env to a strong, random value
- Use environment-specific .env files
- Enable HTTPS/TLS for all connections
- Use a production-grade database with proper backups
- Implement rate limiting
- Add logging and monitoring
- Use a reverse proxy (Nginx, Traefik)
- Keep dependencies updated

### Password Requirements
- Minimum 8 characters
- Hashed using Bcrypt before storage
- Never logged or exposed in responses

### JWT Tokens
- Default expiration: 24 hours (1440 minutes)
- Stored in localStorage on frontend
- Automatically included in API requests
- Invalid tokens result in 401 redirect to login

## Database Schema

### Users Table
- `id`: UUID (Primary Key)
- `email`: String (Unique, Indexed)
- `hashed_password`: String
- `role`: Enum ('user', 'admin')
- `created_at`: Timestamp

### Watchlist Items Table
- `id`: UUID (Primary Key)
- `user_id`: UUID (Foreign Key -> users.id, Indexed)
- `token_symbol`: String
- `target_price`: Float
- `notes`: String (Nullable)
- `created_at`: Timestamp

## Project Structure

```
primewatch/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/     # API endpoints
│   │   ├── core/                 # Config, security, dependencies
│   │   ├── crud/                 # Database operations
│   │   ├── db/                   # Database session
│   │   ├── models/               # SQLAlchemy models
│   │   ├── schemas/              # Pydantic schemas
│   │   └── main.py               # FastAPI app entry point
│   ├── .env                      # Environment variables
│   ├── requirements.txt          # Python dependencies
│   └── Dockerfile                # Backend Docker config
├── frontend/
│   ├── app/                      # Next.js App Router pages
│   ├── lib/                      # API client and auth utilities
│   ├── types/                    # TypeScript types
│   ├── .env.local                # Frontend environment variables
│   └── package.json              # Node dependencies
└── docker-compose.yml            # Docker Compose configuration
```

## Testing the Application

1. Visit http://localhost:3000
2. Click "Create a new account" and register a user
3. Login with your credentials
4. Add cryptocurrency tokens to your watchlist:
   - Token Symbol: BTC
   - Target Price: 65000
   - Notes: Consider buying at this price
5. Edit or delete items as needed
6. Logout and register an admin account to see all watchlists

## License

MIT License - see LICENSE file for details

## Contributors

Built as part of the PrimeTrade.ai evaluation assignment.

