# CI/CD Pipeline Guide

**Last Updated:** 2025-01-19
**Version:** 2.0 (Complete Redesign)

---

## Overview

The Levelith CI/CD pipeline is designed with **clarity**, **strict enforcement**, and **developer experience** in mind. It consists of three main workflows:

1. **CI Pipeline** (`ci.yml`) - Fast, comprehensive checks on every PR
2. **Golden Rules Enforcement** (`golden-rules.yml`) - Strict quality standards
3. **Deployment** (`deploy.yml`) - Automated deployment to Render.com

---

## Quick Reference

### Status Badges

Add these to your README.md:

```markdown
![CI Pipeline](https://github.com/Free-Columns/levelith-2/workflows/CI%20Pipeline/badge.svg)
![Golden Rules](https://github.com/Free-Columns/levelith-2/workflows/🏆%20Golden%20Rules%20Enforcement/badge.svg)
![Deployment](https://github.com/Free-Columns/levelith-2/workflows/🚀%20Deploy%20to%20Production/badge.svg)
```

### Local Testing

Before pushing, run these commands locally:

```bash
# Backend checks
black backend/ dev/ tests/
isort backend/ dev/ tests/
flake8 backend/ dev/ tests/
mypy backend/ dev/ --ignore-missing-imports
pytest tests/ --cov=backend --cov=dev --cov-fail-under=80

# Frontend checks
cd frontend
npx prettier --write "src/**/*.{js,jsx,ts,tsx}"
npx eslint "src/**/*.{js,jsx,ts,tsx}" --fix
npx tsc --noEmit
npm test -- --coverage --watchAll=false

# AI Agent Index
python dev/aiagent_navigator.py index
```

---

## CI Pipeline (`ci.yml`)

### Triggers
- Push to `main`, `develop`, or `claude/**` branches
- Pull requests to `main` or `develop`
- Manual dispatch

### Jobs

#### Backend Checks
1. **Lint & Format** - Black, isort, Flake8
2. **Type Checking** - MyPy with strict mode
3. **Tests** - Pytest with **≥80% coverage requirement (STRICT)**

#### Frontend Checks
1. **Lint & Format** - Prettier, ESLint
2. **Type Checking** - TypeScript compiler
3. **Tests** - Jest with coverage
4. **Build** - Production build verification

#### AI Agent Index
- Validates index is up to date
- **STRICT**: Fails if index needs updating

### Success Criteria
✅ All jobs must pass for PR to be mergeable

### Failure Handling
- Clear error messages showing which job failed
- PR comment added explaining how to fix
- No hidden failures (no `|| true` fallbacks)

---

## Golden Rules Enforcement (`golden-rules.yml`)

### Triggers
- Push to `main`, `develop`, or `claude/**` branches
- Pull requests to `main` or `develop`
- Manual dispatch

### Rules (7 out of 10 Golden Rules)

#### Rule 1: Test-First Development ✅ CRITICAL
- **Requirement:** Test coverage ≥ 80%
- **Enforcement:** STRICT - Build fails if below threshold
- **Check:** `pytest --cov-fail-under=80`
- **Fix:** Add tests for uncovered code

#### Rule 2: Documentation ✅ CRITICAL
- **Requirement:** Docstring coverage ≥ 90%
- **Enforcement:** STRICT
- **Check:** `interrogate --fail-under=90`
- **Fix:** Add docstrings to functions/classes

#### Rule 3: Security First ✅ CRITICAL
- **Checks:**
  - Bandit security scan
  - Safety vulnerability check
  - pip-audit dependency audit
  - TruffleHog secret scanning
- **Enforcement:** STRICT on high severity issues
- **Fix:** Address security vulnerabilities immediately

#### Rule 4: AI Agent Index ✅ CRITICAL
- **Requirement:** Index must be up to date
- **Enforcement:** STRICT
- **Check:** Git diff on `.aiagent-index.json`
- **Fix:** Run `python dev/aiagent_navigator.py index`

#### Rule 5: Code Quality ⚠️ ADVISORY
- **Checks:**
  - Black formatting
  - Code complexity (radon)
  - Maintainability index
  - Pylint quality score
- **Enforcement:** Advisory (warnings only)

#### Rule 6: Dependencies ✅ CRITICAL
- **Requirement:** All dependencies must be pinned
- **Enforcement:** STRICT
- **Check:** No unpinned versions in requirements.txt
- **Fix:** Pin all versions (e.g., `package==1.2.3`)

#### Rule 7: Performance ⚠️ ADVISORY
- **Checks:** Performance benchmarks
- **Enforcement:** Advisory (tracking only)

#### Rule 10: Commit Quality ⚠️ ADVISORY
- **Checks:** Conventional commit format
- **Enforcement:** Advisory

### Summary Job
- Aggregates all rule results
- **Fails build if ANY critical rule fails**
- Generates detailed summary report
- Posts PR comment on failure

---

## Deployment Pipeline (`deploy.yml`)

### Triggers
- Automatically after CI + Golden Rules pass on `main`
- Manual dispatch with environment selection

### Pre-Deployment
1. Verify CI passed
2. Verify on `main` branch
3. Build backend package
4. Build frontend bundle

### Deployment to Render.com

#### Backend Deployment
- Triggers Render API
- Waits for deployment completion
- Runs health checks

#### Frontend Deployment
- Triggers Render API
- Waits for deployment completion
- Runs health checks

### Post-Deployment Verification
1. **Health Checks:**
   - Backend API: `https://levlith.online/api/health`
   - Frontend: `https://levlith.online`

2. **Smoke Tests:**
   - API version endpoint
   - NAICS search endpoint
   - Basic functionality tests

3. **Rollback on Failure:**
   - Creates GitHub issue
   - Notifies team
   - Manual rollback required

### Required Secrets

Configure these in GitHub Settings → Secrets:

```
RENDER_API_KEY                    # Render.com API key
RENDER_BACKEND_SERVICE_ID        # Backend service ID
RENDER_FRONTEND_SERVICE_ID       # Frontend service ID
```

To get these:
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Settings → API Keys → Create new key
3. Copy service IDs from service URLs

---

## Common Issues & Solutions

### Issue: "Test coverage below 80%"

**Solution:**
```bash
# Check coverage report
pytest --cov=backend --cov=dev --cov-report=html
open htmlcov/index.html

# Identify uncovered lines
# Add tests for those lines
# Re-run tests
pytest --cov=backend --cov=dev --cov-fail-under=80
```

### Issue: "AI Agent index out of date"

**Solution:**
```bash
# Update index
python dev/aiagent_navigator.py index

# Commit changes
git add .aiagent-index.json
git commit -m "chore: Update AI agent index"
git push
```

### Issue: "Code formatting failed"

**Solution:**
```bash
# Format Python code
black backend/ dev/ tests/
isort backend/ dev/ tests/

# Format TypeScript/JavaScript
cd frontend
npx prettier --write "src/**/*.{js,jsx,ts,tsx}"

# Commit changes
git add .
git commit -m "style: Format code"
git push
```

### Issue: "Unpinned dependencies"

**Solution:**
```bash
# Pin all dependencies
pip freeze > backend/requirements.txt

# Or manually pin in requirements.txt
# Before: requests
# After:  requests==2.31.0

git add backend/requirements.txt
git commit -m "chore: Pin dependency versions"
git push
```

### Issue: "Security vulnerabilities found"

**Solution:**
```bash
# Check vulnerabilities
bandit -r backend/ dev/
safety check

# Fix specific issues shown in report
# Update vulnerable dependencies
pip install --upgrade <package>
pip freeze | grep <package> >> backend/requirements.txt

# Re-run security scan
bandit -r backend/ dev/
```

### Issue: "Deployment failed"

**Solution:**
1. Check Render dashboard for logs
2. Verify environment variables are set
3. Check health endpoints manually
4. Review deployment summary in Actions tab
5. Create issue if persistent failure

---

## Branch Protection Rules

Recommended settings for `main` and `develop` branches:

### Required Status Checks
- ✅ CI Success
- ✅ Golden Rules Summary
- ✅ Backend Lint & Format
- ✅ Backend Tests
- ✅ Frontend Build
- ✅ AI Agent Index

### Additional Settings
- ✅ Require branches to be up to date
- ✅ Require pull request reviews (1 minimum)
- ✅ Dismiss stale reviews
- ✅ Require review from code owners
- ✅ Require status checks to pass
- ✅ Require conversation resolution
- ❌ Allow force pushes
- ❌ Allow deletions

To configure:
1. Go to Settings → Branches
2. Add rule for `main` and `develop`
3. Enable settings above

---

## Performance Optimization

### Caching Strategy

**Python dependencies:**
```yaml
- uses: actions/setup-python@v5
  with:
    cache: 'pip'
```

**Node dependencies:**
```yaml
- uses: actions/setup-node@v4
  with:
    cache: 'npm'
```

### Concurrency Control

Automatically cancels in-progress runs:
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

### Job Parallelization

Jobs run in parallel when possible:
- Backend lint + typecheck + test (parallel)
- Frontend lint + typecheck + test + build (parallel)
- AI index validation (parallel)

---

## Monitoring & Alerts

### GitHub Actions Dashboard
- View all workflow runs: Actions tab
- Filter by workflow, branch, status
- Download logs and artifacts

### Deployment Monitoring
- Render dashboard: https://dashboard.render.com/
- Health endpoint: https://levlith.online/api/health
- Logs: Render service logs

### Failure Notifications
- PR comments on CI failure
- GitHub issues created on deployment failure
- Email notifications (configure in GitHub settings)

---

## Best Practices

### For Developers

1. **Run checks locally before pushing**
   ```bash
   # Quick pre-push check
   black . && flake8 . && pytest --cov=backend --cov-fail-under=80
   ```

2. **Keep PRs small and focused**
   - Easier to review
   - Faster CI runs
   - Lower chance of conflicts

3. **Write meaningful commit messages**
   - Use conventional commits format
   - Be descriptive about changes

4. **Update tests with code changes**
   - Maintain 80%+ coverage
   - Test edge cases

5. **Keep dependencies up to date**
   - Regular security updates
   - Review dependency changes

### For AI Agents

1. **Always update AI index after code changes**
   ```bash
   python dev/aiagent_navigator.py index
   ```

2. **Follow Golden Rules strictly**
   - No exceptions
   - Tests before code
   - Document everything

3. **Run full CI locally before pushing**
   - Catch issues early
   - Faster iteration

---

## Troubleshooting CI

### Debug Mode

Enable debug logging:
```yaml
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

### Re-running Jobs

1. Go to Actions tab
2. Click failed workflow run
3. Click "Re-run failed jobs"
4. Or "Re-run all jobs" for clean slate

### Viewing Logs

1. Actions tab → Workflow run
2. Click job name
3. Expand step to see logs
4. Download logs for offline analysis

### Common CI Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError` | Missing dependency | Add to requirements.txt |
| `SyntaxError` | Python syntax error | Fix syntax |
| `AssertionError` | Test failure | Fix failing test |
| `Coverage too low` | Missing tests | Add tests |
| `Black would reformat` | Code not formatted | Run `black .` |
| `No such file` | Wrong path | Check file path |

---

## Workflow Diagrams

### CI Pipeline Flow

```
Push/PR → CI Pipeline
├─ Backend Lint ✓
├─ Backend TypeCheck ✓
├─ Backend Tests (≥80%) ✓
├─ Frontend Lint ✓
├─ Frontend TypeCheck ✓
├─ Frontend Tests ✓
├─ Frontend Build ✓
└─ AI Index ✓
   │
   └─→ CI Success ✅
```

### Golden Rules Flow

```
Push/PR → Golden Rules
├─ Rule 1: Tests ≥80% ✅ CRITICAL
├─ Rule 2: Docs ≥90% ✅ CRITICAL
├─ Rule 3: Security ✅ CRITICAL
├─ Rule 4: AI Index ✅ CRITICAL
├─ Rule 5: Quality ⚠️ ADVISORY
├─ Rule 6: Dependencies ✅ CRITICAL
└─ Rule 7: Performance ⚠️ ADVISORY
   │
   └─→ Summary (fails on any critical failure)
```

### Deployment Flow

```
CI + Golden Rules Pass on main
   │
   ├─→ Pre-Deploy Checks
   │   └─→ Build Artifacts
   │
   ├─→ Deploy Backend → Health Check
   │
   ├─→ Deploy Frontend → Health Check
   │
   └─→ Smoke Tests
       │
       ├─→ Success ✅ → Done
       └─→ Failure ❌ → Create Issue + Rollback
```

---

## Migration from Old CI

### What Changed

**Before:**
- 4 separate workflow files
- Many `|| true` fallbacks hiding failures
- Unclear failure messages
- No strict enforcement
- References to non-existent scripts

**After:**
- 3 clear, focused workflows
- Strict enforcement (no hidden failures)
- Clear error messages and fix instructions
- Dedicated Golden Rules section
- Automated deployment
- PR comments and summaries

### Migration Steps

Old workflows are backed up:
- `main-ci.yml.old`
- `backend-ci.yml.old`
- `frontend-ci.yml.old`
- `enforce-golden-rules.yml.old`

New workflows are active:
- `ci.yml` (main CI)
- `golden-rules.yml` (quality enforcement)
- `deploy.yml` (deployment)

---

## FAQs

**Q: Why did my PR fail CI?**
A: Check the Actions tab for detailed logs. Common causes: test coverage below 80%, code not formatted, AI index out of date.

**Q: Can I skip CI checks?**
A: No. All checks are required for merge. This maintains code quality.

**Q: How do I test CI changes?**
A: Create a PR with your changes. CI will run automatically.

**Q: What if CI is wrong about coverage?**
A: Coverage calculation is accurate. If you believe it's wrong, check `htmlcov/index.html` for details.

**Q: Can I deploy to staging?**
A: Yes. Use workflow dispatch and select "staging" environment.

**Q: How long does CI take?**
A: Typically 5-10 minutes. Optimized with caching and parallelization.

---

## Support

- **Documentation:** `/docs/dev/`
- **Issues:** [GitHub Issues](https://github.com/Free-Columns/levelith-2/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Free-Columns/levelith-2/discussions)

---

**Last Updated:** 2025-01-19
**Maintained By:** DevOps Team
**Version:** 2.0

---

**End of CI/CD Guide**
