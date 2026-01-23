# Security Policy

## Supported Versions

We actively maintain security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.1.x   | :white_check_mark: |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

**Please DO NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them responsibly by:

1. **Email**: Send details to `security@[your-domain].com` (or use GitHub private vulnerability reporting)
2. **Subject Line**: `[SECURITY] AI Worker Dashboard - [Brief Description]`
3. **Include**:
   - Type of vulnerability (e.g., SQL injection, XSS, authentication bypass)
   - Full paths of source file(s) related to the vulnerability
   - Step-by-step instructions to reproduce the issue
   - Proof-of-concept or exploit code (if possible)
   - Potential impact of the vulnerability

### What to Expect

- **Initial Response**: Within 48 hours
- **Status Updates**: Every 5 business days until resolution
- **Fix Timeline**: Critical vulnerabilities patched within 7 days, moderate within 30 days
- **Public Disclosure**: After fix is deployed (coordinated disclosure)

## Security Best Practices for Deployment

### Production Recommendations

#### 1. **Environment Variables**
```bash
# NEVER commit these to version control
DATABASE_URL=postgresql://secure_user:strong_password@localhost/factory_db
SECRET_KEY=generate-with-openssl-rand-base64-32
ALLOWED_ORIGINS=https://dashboard.yourcompany.com
```

#### 2. **CORS Configuration**
```python
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://dashboard.yourcompany.com"],  # NO wildcards in prod!
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

#### 3. **Rate Limiting**
Current: 100 requests/minute per IP
```python
# Adjust in backend/app/main.py if needed
limiter = Limiter(key_func=get_remote_address, default_limits=["100 per minute"])
```

#### 4. **HTTPS Enforcement**
```nginx
# frontend/nginx.conf (add for production)
server {
    listen 80;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
}
```

#### 5. **Database Security**
- **Development**: SQLite is acceptable
- **Production**: Migrate to PostgreSQL with:
  - SSL connections
  - Strong passwords (min 16 characters, mixed case + symbols)
  - Restricted network access (VPN/private subnet)
  - Regular backups with encryption

#### 6. **Dependency Scanning**
```bash
# Scan for known vulnerabilities
pip install safety
safety check --file backend/requirements.txt

npm audit --prefix frontend
```

---

## Known Security Considerations

### Current Limitations (Development Mode)

| Issue | Risk Level | Mitigation |
|-------|-----------|------------|
| SQLite for persistence | Low (dev only) | Use PostgreSQL in production |
| No authentication | **High** | Add OAuth2/JWT before production |
| CORS wildcard in dev | Medium | Restrict to specific origins |
| No input sanitization | Medium | Pydantic schemas validate types |
| No rate limiting per user | Low | Currently IP-based |

### Mitigations in Place

✅ **SQL Injection**: Protected by SQLAlchemy ORM parameterized queries  
✅ **XSS**: React auto-escapes output by default  
✅ **CSRF**: Stateless API (no cookies for auth)  
✅ **Duplicate Events**: Composite UNIQUE constraint prevents duplicates  
✅ **Out-of-Order Events**: Sorted by timestamp during aggregation  

---

## Security Headers

**Recommended nginx configuration** (add to `frontend/nginx.conf`):

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
```

---

## Audit Log

Track security-relevant events:

| Date       | Version | Change |
|------------|---------|--------|
| 2026-01-21 | 1.1.0   | Added rate limiting (100 req/min) |
| 2026-01-20 | 1.0.0   | Initial release with CORS middleware |

---

## Responsible Disclosure

We follow coordinated vulnerability disclosure:

1. **Report received** → Acknowledged within 48 hours
2. **Validation** → Reproduce and confirm the issue
3. **Fix developed** → Create patch and test
4. **Security advisory** → Published after fix is deployed
5. **Public disclosure** → 90 days after fix (or sooner with reporter's consent)

**Credit**: Security researchers who responsibly disclose vulnerabilities will be credited in:
- CHANGELOG.md
- GitHub Security Advisory
- README.md acknowledgments

---

## Security Contact

- **Primary**: `security@[your-domain].com`
- **GitHub**: Use [Private Vulnerability Reporting](https://github.com/bhartiinsan/ai-worker-productivity-dashboard/security/advisories/new)
- **PGP Key**: [Available upon request]

---

## Compliance

This project is designed for:
- ✅ GDPR compliance (no PII collected by default)
- ✅ OWASP Top 10 awareness
- ✅ Industry-standard security practices

**Note**: This is a demonstration/educational project. For production use in regulated industries (healthcare, finance), consult security professionals for:
- HIPAA compliance
- PCI-DSS requirements
- SOC 2 Type II controls

---

**Last Updated**: 2026-01-21  
**Next Review**: 2026-04-21
