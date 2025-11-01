# Exodus Trading System

A quantitative algorithmic trading platform for the Korean stock market, integrating with Korea Investment & Securities OpenAPI.

## Overview

Exodus Trading System is a comprehensive automated trading platform that:
- Generates Buy/Sell/Hold signals using quantitative investment strategies
- Executes automated trading through Korea Investment & Securities API
- Provides backtesting capabilities to validate strategies
- Offers a modern web interface for monitoring and management

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15+
- **Cache**: Redis 7+
- **ORM**: SQLAlchemy 2.0+ with Alembic
- **Authentication**: JWT (PyJWT)
- **Data Processing**: pandas, numpy, TA-Lib

### Frontend
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **State Management**: Zustand
- **Data Fetching**: TanStack Query

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Reverse Proxy**: Nginx
- **API Integration**: Korea Investment OpenAPI

## Project Structure

```
exodus-trading-system/
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Trading engine core
│   │   ├── services/       # Business logic services
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── db/             # Database configuration
│   │   ├── utils/          # Utility functions
│   │   └── middleware/     # Middleware components
│   ├── alembic/            # Database migrations
│   ├── tests/              # Test files
│   └── requirements.txt    # Python dependencies
│
├── frontend/               # Next.js frontend application
│   ├── src/
│   │   ├── app/           # App router pages
│   │   ├── components/    # React components
│   │   ├── lib/           # Utilities and helpers
│   │   └── styles/        # Global styles
│   └── package.json       # Node dependencies
│
├── diagrams/              # Architecture diagrams
├── docker-compose.yml     # Docker orchestration
├── nginx.conf            # Nginx configuration
└── .env.example          # Environment variables template
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Korea Investment & Securities account and API credentials
- Minimum system requirements:
  - CPU: 2 cores
  - RAM: 4GB
  - Storage: 20GB free space

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd exodus-trading-system
```

2. Copy the environment template and configure:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Generate a secure secret key:
```bash
openssl rand -hex 32
```
Add this to your `.env` file as `SECRET_KEY`.

4. Configure Korea Investment API credentials in `.env`:
```env
KIS_APP_KEY=your_app_key
KIS_APP_SECRET=your_app_secret
KIS_ACCOUNT_NUMBER=your_account_number
KIS_ACCOUNT_CODE=your_account_code
```

### Running with Docker Compose

1. Build and start all services:
```bash
docker-compose up -d
```

2. Check service status:
```bash
docker-compose ps
```

3. View logs:
```bash
docker-compose logs -f
```

4. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs

### Development Setup (Local)

#### Backend

1. Create a virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run database migrations:
```bash
alembic upgrade head
```

4. Start the development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run the development server:
```bash
npm run dev
```

3. Access at http://localhost:3000

## MVP Features (Phase 1)

The current MVP includes:

- ✅ Docker-based infrastructure setup
- ✅ PostgreSQL and Redis configuration
- ✅ JWT authentication system
- ✅ User registration and login
- ✅ Korea Investment API integration (authentication)
- ✅ Basic market data collection
- ✅ Simple momentum strategy (Moving Average Crossover)
- ✅ Backtest engine with performance metrics
- ✅ Basic frontend with authentication pages

## Planned Features

### Phase 2: Core Trading
- Automated trading signal generation
- Order execution and management
- Real-time portfolio tracking
- WebSocket real-time updates
- Risk management (stop-loss, position sizing)

### Phase 3: Advanced Features
- Multiple advanced strategies
- Real-time monitoring dashboard
- Analytics and reporting
- Email/push notifications
- Dark mode support

## API Documentation

Once the backend is running, access the interactive API documentation:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## Database Migrations

Create a new migration:
```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback:
```bash
alembic downgrade -1
```

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Security Considerations

- Never commit `.env` files or sensitive credentials
- Use strong passwords for database and secret keys
- Keep API keys secure and rotate regularly
- Enable HTTPS in production
- Regular security audits and updates

## Troubleshooting

### Container Issues
```bash
# Rebuild containers
docker-compose up --build

# Reset everything
docker-compose down -v
docker-compose up -d
```

### Database Connection Issues
- Verify PostgreSQL is running: `docker-compose ps postgres`
- Check logs: `docker-compose logs postgres`
- Verify DATABASE_URL in `.env`

### Frontend Connection Issues
- Verify NEXT_PUBLIC_API_URL matches backend address
- Check CORS settings in backend/app/config.py

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Specify your license here]

## Support

For issues and questions, please create an issue in the repository.

## Acknowledgments

- Korea Investment & Securities for API access
- FastAPI and Next.js communities
- All contributors to this project
