---
name: Standard Feature/Fix PR
about: Use this template for all pull requests to maintain consistent review standards
title: "[FEATURE/FIX/DOCS] Brief description (50 chars max)"
labels: ''
assignees: ''
---

## 📋 PR Summary

**Type**: `[FEATURE | BUGFIX | REFACTOR | DOCS | PERFORMANCE | SECURITY]`

**Brief Description**:
<!-- One-liner summary of this PR -->
<!-- e.g., "Add worker shift handover detection to identify 14% productivity dips" -->

---

## 🎯 Motivation & Context

**Why is this change needed?**
<!-- Explain the problem or feature request. Include business impact if relevant. -->
<!-- Example: "Factory managers need to identify shift transitions causing 14% utilization drops." -->

**Related Issue(s)**: #<!-- GitHub issue number(s) -->

---

## 🔧 Changes Made

**Scope of Changes**:
- [ ] Backend (FastAPI / services / database)
- [ ] Frontend (React / UI / styling)
- [ ] Configuration / DevOps
- [ ] Documentation / Comments

**Detailed Changelist**:
<!-- Summarize all files modified. Group by logical components. -->

```
Backend:
  - backend/app/services/metrics_service.py: Added shift_handover_detection() function
  - backend/app/models.py: Added ShiftEvent table for transition tracking
  - backend/app/schemas.py: Added ShiftHandoverMetrics schema

Frontend:
  - frontend/src/App.tsx: Render shift_handover_data in KPI cards
  - frontend/src/types.ts: Added ShiftHandoverMetrics interface
  - frontend/src/services/api.ts: Added getShiftHandoverAnalysis() method

Configuration:
  - docker-compose.yml: No changes
  - .env.example: Added SHIFT_HANDOVER_WINDOW_MIN=15
```

---

## 📊 Testing & Verification

**Manual Testing**:
- [ ] Tested locally with `docker-compose up`
- [ ] Verified backend API: `curl http://localhost:8000/docs`
- [ ] Tested frontend: http://localhost:3000
- [ ] Tested with production Docker build

**Test Cases Covered**:
- [ ] Happy path: Normal event flow with no handovers
- [ ] Edge case: Multiple rapid handovers within same minute
- [ ] Edge case: Missing worker events during handover window
- [ ] Edge case: Out-of-order event arrivals handled correctly

**Screenshot / Demo**:
<!-- If UI changes, attach screenshot or describe visual changes -->
<!-- Example: "Shift Handover card now shows dip percentage and affected workstations" -->

---

## 🔒 Security & Performance

**Security Checklist**:
- [ ] No hardcoded secrets in code
- [ ] Input validation enforced (Pydantic schemas)
- [ ] SQL injection risks mitigated (using ORM)
- [ ] Rate limiting still active for new endpoints

**Performance Impact**:
- [ ] Database query performance: O(n) aggregation over events (acceptable for <100K events)
- [ ] Frontend re-render optimized: memoized components
- [ ] No new dependencies added (or justified if added)
- [ ] Caching strategy: metrics cached for 60s

**Load Test Results** (if applicable):
- Query response time: ~200ms for 10K events
- Memory footprint: +2MB for new ShiftEvent table

---

## 📚 Documentation

**Updated Documentation**:
- [ ] README.md (if user-facing feature)
- [ ] CODE comments (complex algorithms explained)
- [ ] API docstrings (FastAPI route comments)
- [ ] PROJECT_STRUCTURE.md (if new modules added)

**Docstring Example**:
```python
def detect_shift_handover(db, window_minutes=15):
    """
    Detect productivity dips during shift transitions.
    
    Algorithm: Identify time windows where utilization < (baseline - 2σ)
    during known shift boundaries (e.g., 2:00 PM ± 15 min).
    
    Returns: List[ShiftHandoverEvent] with dip percentages
    """
```

---

## 🔄 Backwards Compatibility

- [ ] No breaking API changes
- [ ] Database migrations included (if schema changed)
- [ ] Existing tests still passing
- [ ] Deprecation warnings added (if removing features)

**Migration Steps** (if required):
```sql
-- For database schema changes:
ALTER TABLE ai_events ADD COLUMN shift_id VARCHAR(10) DEFAULT NULL;
CREATE INDEX idx_shift_id ON ai_events(shift_id);
```

---

## 👥 Reviewer Checklist

**For Reviewers**:
- [ ] Code follows project style (PEP-8 Python, ESLint TypeScript)
- [ ] Logic is correct and handles edge cases
- [ ] Comments explain "why", not "what"
- [ ] Performance is acceptable
- [ ] Security concerns addressed
- [ ] Tests pass and coverage adequate
- [ ] Documentation updated
- [ ] PR title and description are clear

---

## 🚀 Deployment Notes

**Deployment Steps**:
1. Merge to `main` branch
2. Trigger CI/CD pipeline
3. Run database migrations (if applicable)
4. Deploy backend: `docker build backend/ && docker push ...`
5. Deploy frontend: `docker build frontend/ && docker push ...`
6. Update docker-compose.yml if needed
7. Monitor logs for 5 minutes post-deployment

**Rollback Plan** (if issues):
```bash
git revert <commit-hash>
docker-compose down && docker-compose up -d
# Monitor metrics for 2 hours
```

**Configuration Changes**: None (or list if applicable)

---

## 📝 Additional Context

**Related PRs**: <!-- Link to related/predecessor PRs -->

**Blocked By**: <!-- Link to blocking issues or PRs -->

**Blocks**: <!-- Link to PRs waiting on this one -->

**Questions for Reviewer**:
<!-- Ask specific questions if you're unsure about approach or trade-offs -->
1. Should shift_handover_window be configurable per factory?
2. Is 14% threshold too aggressive for detection?

---

## ✅ Final Checklist

Before submitting, verify:
- [ ] Branch is up-to-date with `main`
- [ ] All commits have descriptive messages
- [ ] No merge conflicts
- [ ] Local build successful: `docker-compose up`
- [ ] Linter passes: `flake8 backend/ && eslint frontend/`
- [ ] All tests pass: `pytest backend/tests/`
- [ ] PR template filled out completely
- [ ] Assignee(s) and label(s) set

---

**Thank you for contributing to the AI Worker Productivity Dashboard!** 🎉

Your PR will be reviewed within 24 hours. If you have questions, mention @maintainers or open a discussion.
