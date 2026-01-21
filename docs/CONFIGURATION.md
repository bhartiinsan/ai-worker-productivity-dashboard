# ⚙️ Environment Variables Configuration

Both backend and frontend require environment configuration. Copy the provided `.env.example` files to `.env` and customize for your environment.

---

## Backend Configuration (`backend/.env`)

**Key Variables:**

| Variable | Example | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///./productivity.db` | SQLite database path (or PostgreSQL URL for production) |
| `API_KEY` | `your-secure-api-key-here` | API authentication key (implement for production) |
| `API_RATE_LIMIT` | `100` | Requests per minute (adjust based on load) |
| `CORS_ORIGINS` | `http://localhost:3000` | Comma-separated list of allowed frontend origins |
| `ENVIRONMENT` | `development` | `development`, `staging`, or `production` |
| `LOG_LEVEL` | `INFO` | Logging level: `DEBUG`, `INFO`, `WARNING`, `ERROR` |

**Setup:**
```bash
cd backend
cp .env.example .env
# Edit .env to configure for your environment
```

**Reference:** See [backend/.env.example](../backend/.env.example)

---

## Frontend Configuration (`frontend/.env`)

**Key Variables:**

| Variable | Example | Description |
|----------|---------|-------------|
| `REACT_APP_API_URL` | `http://localhost:8000` | Backend API endpoint (include protocol, no trailing slash) |

**Setup:**
```bash
cd frontend
cp .env.example .env
# Edit .env if needed (API_URL can also be passed via docker-compose)
```

**Reference:** See [frontend/.env.example](../frontend/.env.example)

---

## Common Configuration Scenarios

### Local Development (Default)
```env
# backend/.env
DATABASE_URL=sqlite:///./productivity.db
CORS_ORIGINS=http://localhost:3000
ENVIRONMENT=development
LOG_LEVEL=DEBUG

# frontend/.env
REACT_APP_API_URL=http://localhost:8000
```

### Docker Compose
```env
# backend/.env
DATABASE_URL=sqlite:///./productivity.db
CORS_ORIGINS=http://frontend:3000
ENVIRONMENT=production
LOG_LEVEL=INFO

# frontend/.env
REACT_APP_API_URL=http://backend:8000
```

### Production (Cloud Deployment)
```env
# backend/.env
DATABASE_URL=postgresql://user:pass@prod-db:5432/productivity
API_RATE_LIMIT=500
CORS_ORIGINS=https://yourdomain.com
ENVIRONMENT=production
LOG_LEVEL=WARNING

# frontend/.env
REACT_APP_API_URL=https://api.yourdomain.com
```

---

## Environment Variable Best Practices

1. **Never commit `.env` files** - Use `.env.example` as templates
2. **Use strong API keys** in production (minimum 32 characters)
3. **Enable HTTPS** for production CORS origins
4. **Adjust rate limits** based on expected traffic
5. **Use PostgreSQL** for production instead of SQLite
6. **Set LOG_LEVEL to WARNING** in production to reduce noise
