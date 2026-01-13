---
description: Best practices for using checklists in commands, agents, and skills
---

# Checklist Patterns in Agents

Checklists are powerful tools for ensuring thoroughness, consistency, and quality in AI agent workflows. This guide covers best practices for integrating checklists into your commands, agents, and skills.

## Why Use Checklists?

**Benefits:**
- ✅ **Consistency** - Every invocation follows the same process
- ✅ **Completeness** - Nothing gets forgotten
- ✅ **Auditability** - Clear record of what was checked
- ✅ **Training** - Agents learn comprehensive workflows
- ✅ **Quality** - Higher quality outputs
- ✅ **Communication** - Clear status reporting to users

**Use Cases:**
- Code reviews
- Security audits
- Deployment readiness
- Project setup
- Documentation reviews
- Testing completeness
- Refactoring safety
- Compliance verification

## Checklist Design Principles

### 1. Clear, Actionable Items

**Good:**
- [ ] SQL queries use parameterization (no string concatenation)
- [ ] All tests passing in CI/CD pipeline
- [ ] Database backup completed before migration

**Bad:**
- [ ] Check security ❌ Too vague
- [ ] Make sure everything works ❌ Not specific
- [ ] Review the code ❌ No clear criteria

### 2. Binary Outcomes

Each item should have a clear pass/fail:

```markdown
- [ ] ✅ Passed - meets criteria completely
- [ ] ⚠️ Warning - minor issue, can proceed with caution
- [ ] ❌ Failed - blocker, must fix
- [ ] N/A - not applicable to this situation
```

### 3. Appropriate Granularity

**Too Broad:**
- [ ] Code is good quality

**Too Granular:**
- [ ] Variable `userId` is named correctly
- [ ] Variable `userName` is named correctly
- [ ] Variable `userEmail` is named correctly

**Just Right:**
- [ ] Variable names are descriptive and follow conventions

### 4. Logical Grouping

Organize items into categories:

```markdown
## Security Checklist

### Authentication
- [ ] Item 1
- [ ] Item 2

### Authorization
- [ ] Item 3
- [ ] Item 4

### Data Protection
- [ ] Item 5
- [ ] Item 6
```

## Integration Patterns

### Pattern 1: Agent with Embedded Checklist

The checklist is part of the agent definition:

```markdown
---
name: code-reviewer
description: Reviews code using comprehensive checklist
tools: Read, Grep, Glob
---

# Code Reviewer Agent

## Review Checklist

### Functionality
- [ ] Code does what it's supposed to do
- [ ] Edge cases are handled
- [ ] Error handling is appropriate

### Security
- [ ] No SQL injection vulnerabilities
- [ ] Input validation present
- [ ] No hardcoded secrets

### Code Quality
- [ ] Code is readable
- [ ] No duplication
- [ ] Follows conventions

## Process

1. Read the code changes
2. Work through checklist systematically
3. Mark each item as ✅/⚠️/❌
4. Provide detailed findings
5. Generate summary report
```

**Best for:**
- Agents that always use the same checklist
- Well-defined, stable processes
- Compliance and audit scenarios

### Pattern 2: Command with Checklist Template

The command provides a checklist structure that the AI follows:

```markdown
---
description: Pre-deployment verification
---

# Deployment Readiness Check

Run through the following checklist before deploying:

## Pre-Deployment Checklist

### Testing
- [ ] All tests passing
- [ ] QA approval received
- [ ] Load testing completed

### Infrastructure
- [ ] Backup completed
- [ ] Capacity verified
- [ ] Monitoring configured

## Process

1. Check the current state of each item
2. Report status (✅/⚠️/❌)
3. Identify any blockers
4. Recommend proceed or wait
```

**Best for:**
- User-initiated workflows
- Flexible processes
- One-time or occasional checks

### Pattern 3: Referenced Checklist File

The checklist lives in a separate file and is referenced:

```markdown
---
name: security-audit-agent
description: Security audits using OWASP checklist
tools: Read, Grep, Glob
---

# Security Audit Agent

## Process

1. Read the OWASP checklist from `.claude/checklists/owasp-top-10.md`
2. For each item in the checklist:
   - Investigate the codebase
   - Test for the vulnerability
   - Document findings
3. Generate comprehensive security report
```

**Best for:**
- Large, complex checklists
- Shared checklists across agents
- Frequently updated checklists
- Industry-standard checklists (OWASP, NIST, etc.)

### Pattern 4: Dynamic Checklist Generation

The agent generates a custom checklist based on context:

```markdown
---
name: custom-review-agent
description: Generates custom review checklist based on code type
---

# Custom Review Agent

## Process

1. Analyze the code being reviewed
2. Determine the code type (frontend, backend, database, etc.)
3. Generate appropriate checklist:
   - Frontend: Accessibility, performance, browser compat
   - Backend: Security, scalability, error handling
   - Database: Indexes, migrations, query performance
4. Execute review using generated checklist
5. Report findings
```

**Best for:**
- Context-dependent workflows
- Multi-purpose agents
- Adaptive processes

## Checklist Output Formats

### Format 1: Summary + Details

```markdown
# Review Summary

✅ Passed: 12 items
⚠️ Warnings: 3 items
❌ Failed: 2 items

## Checklist Results

### ✅ Passed
- Functionality: All features work as expected
- Testing: Good test coverage (85%)
- Documentation: Well documented

### ⚠️ Warnings
- Performance: One query could be optimized
- Code Quality: Minor duplication in utils.js
- Security: Consider adding rate limiting

### ❌ Failed
- Security: SQL injection vulnerability in user search
- Error Handling: Missing try/catch in async functions

## Detailed Findings
[Full details for each warning and failure]
```

**Best for:** Most use cases, provides good overview and detail

### Format 2: Inline Checklist

```markdown
# Code Review

## Checklist

### Functionality
- ✅ Code does what it's supposed to do
- ✅ Edge cases are handled
- ⚠️ Error handling is appropriate (missing in 2 places)

### Security
- ❌ SQL injection vulnerability found (user.controller.js:45)
- ✅ No hardcoded secrets
- ✅ Input validation present

### Code Quality
- ✅ Code is readable
- ⚠️ Minor duplication in utils.js
- ✅ Follows conventions

## Summary
Overall: Needs Changes (1 critical issue)
```

**Best for:** Quick reviews, progress tracking

### Format 3: Scorecard

```markdown
# Security Audit Scorecard

| Category | Items | Passed | Failed | Score |
|----------|-------|--------|--------|-------|
| OWASP A01 | 10 | 8 | 2 | 80% |
| OWASP A02 | 8 | 8 | 0 | 100% |
| OWASP A03 | 12 | 9 | 3 | 75% |
| **Total** | **30** | **25** | **5** | **83%** |

**Overall Grade:** B (Good)
**Recommendation:** Fix 5 failing items before deployment
```

**Best for:** Compliance, metrics tracking, executive summaries

## Best Practices

### Do's ✅

**Be Specific**
```markdown
✅ Good: "Database queries use parameterized statements (no string concatenation)"
❌ Bad: "Database is secure"
```

**Provide Context**
```markdown
- [ ] Password length ≥ 12 characters
      ↑ Clear threshold
- [ ] Tests pass in CI/CD
      ↑ Clear location
```

**Group Logically**
```markdown
## Authentication
- [ ] Item 1
- [ ] Item 2

## Authorization
- [ ] Item 3
- [ ] Item 4
```

**Include Why**
```markdown
- [ ] Session timeout configured (prevents session hijacking)
- [ ] HTTPS enforced (protects data in transit)
```

**Make It Scannable**
```markdown
✅ Use bullet points
✅ Use consistent formatting
✅ Use visual indicators (✅/⚠️/❌)
✅ Group related items
```

### Don'ts ❌

**Don't Be Vague**
```markdown
❌ - [ ] Make sure security is good
❌ - [ ] Check performance
❌ - [ ] Verify quality
```

**Don't Overlap**
```markdown
❌ - [ ] Tests pass
❌ - [ ] All tests are green (duplicate)
❌ - [ ] No failing tests (duplicate)
```

**Don't Mix Levels**
```markdown
❌ Security Checklist:
   - [ ] Check OWASP Top 10 (too high-level)
   - [ ] Verify password has uppercase letter (too granular)
```

**Don't Make It Too Long**
```markdown
❌ 200-item checklist (too overwhelming)
✅ 20-30 items grouped into categories (manageable)
```

## Example Checklists by Use Case

### Code Review Checklist
```markdown
## Functionality
- [ ] Code does what it's supposed to do
- [ ] Edge cases handled
- [ ] Error handling appropriate

## Code Quality
- [ ] Readable and well-structured
- [ ] Functions small and focused
- [ ] No duplication

## Security
- [ ] Input validation present
- [ ] No hardcoded secrets
- [ ] SQL queries parameterized

## Testing
- [ ] Tests cover new code
- [ ] Tests pass
- [ ] Edge cases tested
```

### Deployment Checklist
```markdown
## Pre-Deployment
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Staging tested
- [ ] Backup completed

## Deployment
- [ ] Monitoring configured
- [ ] Rollback plan ready
- [ ] Team notified

## Post-Deployment
- [ ] Smoke tests pass
- [ ] Metrics normal
- [ ] No errors in logs
```

### Security Audit Checklist
```markdown
## Authentication
- [ ] Strong password policy
- [ ] MFA available
- [ ] Account lockout configured

## Authorization
- [ ] Access control on all endpoints
- [ ] Least privilege enforced
- [ ] No IDOR vulnerabilities

## Data Protection
- [ ] HTTPS enforced
- [ ] Sensitive data encrypted
- [ ] PII properly handled
```

### Refactoring Safety Checklist
```markdown
## Before Refactoring
- [ ] Tests exist and pass
- [ ] Understand current behavior
- [ ] Identify all usages

## During Refactoring
- [ ] Change one thing at a time
- [ ] Tests still pass
- [ ] No behavior changes

## After Refactoring
- [ ] All tests pass
- [ ] No regressions
- [ ] Code is clearer
```

## Checklist Maintenance

### Keep Checklists Current

**Review Regularly:**
- After each use, note any missing items
- Quarterly review for outdated items
- Update when standards change

**Version Control:**
```markdown
# Security Checklist v2.1

**Changelog:**
- v2.1 (2024-01-15): Added GraphQL security items
- v2.0 (2023-12-01): Updated for OWASP Top 10 2021
- v1.0 (2023-01-01): Initial version
```

**Track Improvements:**
```markdown
## Recently Added
- [ ] New item based on recent incident
- [ ] New best practice from team retrospective

## Deprecated
- [x] ~~Old item that's automated now~~
```

### Measure Effectiveness

**Track Metrics:**
- Items that frequently fail (need process improvement)
- Items never applicable (remove or make conditional)
- Time to complete checklist (optimize if too long)
- Issues caught by checklist (validate value)

## Advanced Patterns

### Conditional Checklist Items

```markdown
## Database Changes
{{#if hasDatabaseChanges}}
- [ ] Migration tested in staging
- [ ] Backup completed
- [ ] Rollback script ready
{{else}}
- N/A No database changes
{{/if}}
```

### Weighted Checklists

```markdown
## Security Audit (Score: X/100)

Critical Items (50 points)
- [ ] [25pts] SQL injection prevention
- [ ] [25pts] Authentication required

High Priority (30 points)
- [ ] [10pts] HTTPS enforced
- [ ] [10pts] Input validation
- [ ] [10pts] CSRF protection

Medium Priority (20 points)
- [ ] [10pts] Security headers
- [ ] [10pts] Rate limiting
```

### Progressive Checklists

```markdown
## Level 1: Basic (Required)
- [ ] Tests pass
- [ ] Code reviewed
- [ ] No critical bugs

## Level 2: Standard (Recommended)
- [ ] Performance tested
- [ ] Security reviewed
- [ ] Documentation updated

## Level 3: Excellent (Aspirational)
- [ ] Load tested
- [ ] Accessibility tested
- [ ] A/B test ready
```

## Tools and Automation

### Automated Checklist Population

Use tools to automatically check items:

```bash
# Check if tests pass
npm test && echo "✅ Tests pass" || echo "❌ Tests fail"

# Check for hardcoded secrets
git secrets --scan && echo "✅ No secrets" || echo "❌ Secrets found"

# Check dependencies
npm audit --audit-level=high && echo "✅ No vulnerabilities" || echo "❌ Vulnerabilities found"
```

### Integration with CI/CD

```yaml
# .github/workflows/deployment-checklist.yml
name: Deployment Readiness

on: [pull_request]

jobs:
  checklist:
    runs-on: ubuntu-latest
    steps:
      - name: Tests Pass
        run: npm test
      - name: Security Scan
        run: npm audit
      - name: Linting
        run: npm run lint
      # Post checklist results as PR comment
```

## Summary

Checklists in agents provide:
- **Structure** for complex workflows
- **Consistency** across invocations
- **Quality** through thoroughness
- **Auditability** through clear records
- **Training** for comprehensive processes

**Key Takeaways:**
1. Make items specific and actionable
2. Group logically for scannability
3. Use visual indicators (✅/⚠️/❌)
4. Provide context and rationale
5. Keep checklists focused (20-30 items)
6. Update based on learnings
7. Integrate with tools where possible

Start with simple checklists and refine based on experience. The best checklist is one that's actually used!
