---
description: Identify and eliminate code duplication (DRY principle)
args:
  - name: file-path
    description: File or directory to analyze for duplication
    required: false
  - name: threshold
    description: Minimum number of duplicated lines to report (default 5)
    required: false
---

# Remove Code Duplication

Apply the DRY (Don't Repeat Yourself) principle to eliminate code duplication.

## Detection Process

### 1. Find Duplication

{{#if file-path}}
Analyze `{{file-path}}` for duplicated code blocks (minimum {{threshold}} lines or 5 if not specified).
{{else}}
Search the codebase for:
- **Exact duplicates:** Identical code blocks
- **Structural duplicates:** Same logic, different variables
- **Semantic duplicates:** Different code, same purpose
{{/if}}

### 2. Categorize Duplication Types

**Type 1: Exact Copy-Paste**
```python
# File A
result = data.strip().lower().replace('-', '_')

# File B
result = data.strip().lower().replace('-', '_')  # Exact duplicate
```

**Type 2: Parameterized Duplication**
```javascript
// Only differs by values
function getAdminUsers() {
    return db.query('SELECT * FROM users WHERE role = "admin"');
}
function getModeratorUsers() {
    return db.query('SELECT * FROM users WHERE role = "moderator"');
}
```

**Type 3: Structural Duplication**
```java
// Same structure, different details
if (user.isAdmin()) {
    logger.log("Admin access granted");
    grantAccess(user);
} else {
    logger.log("Admin access denied");
    denyAccess(user);
}

if (user.isModerator()) {
    logger.log("Moderator access granted");
    grantAccess(user);
} else {
    logger.log("Moderator access denied");
    denyAccess(user);
}
```

## Refactoring Strategies

### Strategy 1: Extract Function

For exact duplicates:
```python
# Before: Duplicated in 3 places
formatted = data.strip().lower().replace('-', '_')

# After: Single function
def normalize_identifier(data):
    return data.strip().lower().replace('-', '_')
```

### Strategy 2: Parameterize

For parameterized duplication:
```javascript
// Before: Multiple similar functions
function getAdminUsers() {
    return db.query('SELECT * FROM users WHERE role = "admin"');
}
function getModeratorUsers() {
    return db.query('SELECT * FROM users WHERE role = "moderator"');
}

// After: Single parameterized function
function getUsersByRole(role) {
    return db.query('SELECT * FROM users WHERE role = ?', [role]);
}
```

### Strategy 3: Extract Common Pattern

For structural duplication:
```java
// Before: Repeated structure
if (user.isAdmin()) {
    logger.log("Admin access granted");
    grantAccess(user);
} else {
    logger.log("Admin access denied");
    denyAccess(user);
}

// After: Extract pattern
void checkRoleAccess(User user, String role, Predicate<User> hasRole) {
    if (hasRole.test(user)) {
        logger.log(role + " access granted");
        grantAccess(user);
    } else {
        logger.log(role + " access denied");
        denyAccess(user);
    }
}

// Usage
checkRoleAccess(user, "Admin", User::isAdmin);
checkRoleAccess(user, "Moderator", User::isModerator);
```

### Strategy 4: Use Inheritance/Composition

For duplicated methods across classes:
```python
# Before: Duplicated in multiple classes
class AdminReport:
    def generate_header(self):
        return f"Report Generated: {datetime.now()}\n{'='*50}\n"

class UserReport:
    def generate_header(self):
        return f"Report Generated: {datetime.now()}\n{'='*50}\n"

# After: Extract to base class
class BaseReport:
    def generate_header(self):
        return f"Report Generated: {datetime.now()}\n{'='*50}\n"

class AdminReport(BaseReport):
    pass

class UserReport(BaseReport):
    pass
```

### Strategy 5: Configuration Over Code

For similar code with different values:
```javascript
// Before: Duplicated with different configs
function validateAdminEmail(email) {
    const minLength = 5;
    const domain = '@admin.company.com';
    if (email.length < minLength || !email.endsWith(domain)) {
        throw new Error('Invalid admin email');
    }
}

function validateUserEmail(email) {
    const minLength = 5;
    const domain = '@company.com';
    if (email.length < minLength || !email.endsWith(domain)) {
        throw new Error('Invalid user email');
    }
}

// After: Configuration-driven
const emailRules = {
    admin: { minLength: 5, domain: '@admin.company.com' },
    user: { minLength: 5, domain: '@company.com' }
};

function validateEmail(email, type) {
    const rules = emailRules[type];
    if (email.length < rules.minLength || !email.endsWith(rules.domain)) {
        throw new Error(`Invalid ${type} email`);
    }
}
```

## Analysis Checklist

When you find duplication, ask:

- [ ] Is this truly duplicated, or just coincidentally similar?
- [ ] How many times does this code appear? (2x, 3x, 5x+?)
- [ ] Would extracting this make the code clearer or more complex?
- [ ] Are the duplicates likely to evolve together or independently?
- [ ] Is there a common abstraction that makes sense?
- [ ] What would be a good name for the extracted code?

## DRY Principles

### Rule of Three

Wait until code is duplicated **3 times** before extracting:
- **1st time:** Write it
- **2nd time:** Wince at the duplication, but leave it
- **3rd time:** Refactor

**Why?** Premature abstraction can be worse than duplication. Wait until the pattern is clear.

### Appropriate Abstraction Level

```python
# ❌ Too abstract - obscures intent
def process(x, y, fn):
    return fn(x, y)

result = process(a, b, lambda x, y: x + y)

# ✅ Right level - clear intent
def add(a, b):
    return a + b

result = add(a, b)
```

### Knowledge Duplication vs Code Duplication

Sometimes similar code represents different knowledge:

```java
// Both calculate 20%, but represent DIFFERENT concepts
double salesTax = price * 0.20;        // Tax rate (legal requirement)
double earlyBirdDiscount = price * 0.20;  // Marketing decision

// DON'T combine these - they may change independently!
```

## Tools for Detection

**Python:**
```bash
# Use pylint to detect duplication
pylint --disable=all --enable=duplicate-code your_file.py

# Or use CPD (Copy-Paste Detector)
pip install cpd
cpd --minimum-tokens 50 --files your_directory/
```

**JavaScript:**
```bash
# Use jscpd
npm install -g jscpd
jscpd --min-lines 5 --min-tokens 50 src/
```

**General (any language):**
```bash
# PMD's CPD works for many languages
pmd cpd --minimum-tokens 50 --files src/ --language javascript
```

## Refactoring Process

1. **Identify duplication** (manually or with tools)
2. **Verify it's truly duplicate** (not just coincidence)
3. **Apply rule of three** (3+ instances before extracting)
4. **Choose refactoring strategy** (function, parameter, config, etc.)
5. **Extract with good name** (clear, descriptive)
6. **Replace all instances** (search carefully)
7. **Run tests** (ensure behavior unchanged)
8. **Review** (is it clearer now?)

## Output Format

Provide duplication analysis as:

```markdown
## Duplication Report

### Summary
- Files analyzed: [number]
- Duplicate blocks found: [number]
- Total duplicated lines: [number]
- Estimated effort to fix: [time]

### Duplicate Block 1 (Priority: High)
**Appears in:**
- `file1.py:45-52`
- `file2.py:123-130`
- `file3.py:89-96`

**Code:**
```python
[duplicated code block]
```

**Recommendation:**
Extract to function `calculate_discount(price, customer_type)` in `utils/pricing.py`

**Impact:**
- Removes 24 duplicated lines
- Creates single source of truth for discount logic
- Estimated effort: 15 minutes

### Duplicate Block 2 (Priority: Medium)
...
```

## When NOT to Remove Duplication

❌ **Different domains:** Code that looks similar but represents different concepts
❌ **Independent evolution:** Parts that will change for different reasons
❌ **Accidental duplication:** Coincidentally similar, no real relationship
❌ **Over-abstraction risk:** Making code harder to understand
❌ **Performance critical:** Sometimes duplication is faster

## Success Criteria

After removing duplication:
- ✅ Code is more maintainable
- ✅ Intent is clearer
- ✅ Changes only need to be made in one place
- ✅ Tests still pass
- ✅ No new complexity introduced
