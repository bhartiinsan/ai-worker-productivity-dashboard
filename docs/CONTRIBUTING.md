# Contributing to AI Worker Productivity Dashboard

Thank you for your interest in improving the AI Worker Productivity Dashboard! This document provides guidelines and instructions for contributing to the project.

---

## 🤝 How to Contribute

### Reporting Issues

If you encounter a bug or have a feature request:

1. **Check existing issues** first: https://github.com/bhartiinsan/ai-worker-productivity-dashboard/issues
2. **Create a new issue** with:
   - Clear title describing the problem
   - Detailed description (what you expected vs. what happened)
   - Steps to reproduce (if bug)
   - Screenshots/logs (if applicable)
   - Your environment (OS, Python version, Node version)

---

### Making Changes

#### 1. Fork & Clone

```bash
git clone https://github.com/bhartiinsan/ai-worker-productivity-dashboard.git
cd ai-worker-productivity-dashboard
```

#### 2. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming convention:
- `feature/` — New feature (e.g., `feature/shift-handover-detection`)
- `bugfix/` — Bug fix (e.g., `bugfix/deduplication-issue`)
- `refactor/` — Code cleanup (e.g., `refactor/metrics-service`)
- `docs/` — Documentation (e.g., `docs/api-guide`)

#### 3. Make Changes

Follow the project structure:
- **Backend**: Place business logic in `backend/app/services/`
- **Frontend**: Use React components in `frontend/src/`
- **Tests**: Add tests alongside code (future: `backend/tests/`, `frontend/tests/`)

#### 4. Code Style

**Python (Backend)**:
- Follow [PEP 8](https://pep8.org/)
- Use type hints for all functions
- Max line length: 100 characters
- Run linter: `flake8 backend/`

**TypeScript/JavaScript (Frontend)**:
- Use ESLint configuration from `.eslintrc`
- Max line length: 100 characters
- Use TypeScript for type safety
- Run linter: `eslint frontend/src/`

#### 5. Add Documentation

- **Backend**: Add docstrings following the format in `backend/app/services/`
- **Frontend**: Add JSDoc comments for complex functions
- **Markdown**: Update relevant `.md` files (README, PROJECT_STRUCTURE, etc.)

#### 6. Test Locally

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm start
```

Access:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

#### 7. Commit & Push

```bash
git add .
git commit -m "feat: Descriptive commit message"
git push origin feature/your-feature-name
```

Commit message format:
```
<type>: <subject>

<body (optional)>

<footer (optional)>
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `perf`, `chore`

Example:
```
feat: Add shift handover detection to metrics service

- Detect productivity dips during shift transitions
- Alert when utilization drops > 10% for 15-min window
- Add ShiftHandoverMetrics schema

Closes #42
```

#### 8. Open a Pull Request

1. Go to: https://github.com/bhartiinsan/ai-worker-productivity-dashboard/pulls
2. Click "New Pull Request"
3. Select your branch
4. Fill out the PR template:
   - Type (FEATURE/BUGFIX/etc.)
   - Motivation & Context
   - Changes Made
   - Testing & Verification
   - Screenshots (if UI changes)
5. Submit for review

---

## 📋 PR Review Checklist

Your PR will be reviewed against:

- ✅ Code follows project style (PEP-8, ESLint)
- ✅ Logic is correct and handles edge cases
- ✅ Comments explain "why", not "what"
- ✅ Performance is acceptable (no N+1 queries)
- ✅ Security concerns addressed (no secrets in code)
- ✅ Tests pass (if applicable)
- ✅ Documentation updated
- ✅ No breaking API changes

---

## 🛠️ Development Workflow

### Adding a New Feature

**Example: Add worker shift analytics**

1. **Define schema** (backend/app/schemas.py):
   ```python
   class ShiftAnalytics(BaseModel):
       shift_id: str
       productivity_drop: float
       duration_minutes: int
   ```

2. **Add business logic** (backend/app/services/metrics_service.py):
   ```python
   def detect_shift_transitions(db, threshold_percent=10):
       """Detect productivity drops during shift changes."""
       # Implementation here
       return List[ShiftAnalytics]
   ```

3. **Add API endpoint** (backend/app/main.py):
   ```python
   @app.get("/api/metrics/shift-analytics")
   def get_shift_analytics(db: Session = Depends(get_db)):
       return metrics_service.detect_shift_transitions(db)
   ```

4. **Update frontend** (frontend/src/):
   - Add type in `types.ts`
   - Add API call in `services/api.ts`
   - Render in `App.tsx` or component

5. **Document**: Update README with new endpoint

6. **Test**: Manual verification + add unit tests (future)

---

## 📚 Project Structure

For detailed navigation, see [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md).

Key directories:
- `backend/app/services/` — Business logic (start here for features)
- `backend/app/crud.py` — Database operations
- `frontend/src/App.tsx` — Main dashboard component
- `frontend/src/services/api.ts` — HTTP client

---

## 🐛 Debugging Tips

### Backend
- Enable debug logging: Set `LOG_LEVEL=DEBUG` in `.env`
- Use `pdb`: Add `import pdb; pdb.set_trace()` in code
- Check database: `sqlite3 database.db` or use a SQLite browser

### Frontend
- React DevTools browser extension
- Chrome DevTools (F12)
- Console logs: `console.log(variable)`
- Network tab: Check API responses

---

## 📖 Resources

- **Architecture**: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- **API Docs**: http://localhost:8000/docs (when running locally)
- **GitHub Issues**: https://github.com/bhartiinsan/ai-worker-productivity-dashboard/issues
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Docs**: https://react.dev/

---

## ✅ Contribution Standards

To maintain quality:

1. **Test your changes** locally before submitting
2. **Document** public APIs and complex logic
3. **Keep commits focused** — one feature per PR
4. **Reference issues** in commits (e.g., "Closes #42")
5. **Be respectful** — code reviews are constructive feedback

---

## 🎉 Thank You!

Your contributions help make this project better. If you have questions, feel free to:
- Open an issue for discussion
- Comment on an existing PR
- Ask in pull request reviews

Happy coding! 🚀
