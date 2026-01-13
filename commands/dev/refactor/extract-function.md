---
description: Extract duplicated or complex code into a reusable function
args:
  - name: file-path
    description: Path to file containing code to refactor
    required: false
  - name: start-line
    description: Starting line number of code to extract
    required: false
  - name: end-line
    description: Ending line number of code to extract
    required: false
---

# Extract Function Refactoring

Extract duplicated or overly complex code into a well-named, reusable function.

## Process

### 1. Identify Code to Extract

{{#if file-path}}
Analyze the code in `{{file-path}}`{{#if start-line}} from line {{start-line}} to {{end-line}}{{/if}}.
{{else}}
Identify code that:
- Is duplicated in multiple places
- Is complex and hard to understand
- Performs a single, clear responsibility
- Would benefit from a descriptive name
{{/if}}

### 2. Analyze Dependencies

Before extracting, identify:
- **Input parameters:** What variables does this code need?
- **Return values:** What does it produce?
- **Side effects:** Does it modify external state?
- **Scope issues:** Are there closure dependencies?

### 3. Create the New Function

```
function descriptiveName(param1, param2) {
    // Extracted code here
    return result;
}
```

**Naming Guidelines:**
- Use verbs for actions: `calculateTotal`, `validateInput`, `formatDate`
- Be specific: `getUsersByRole` not `getUsers`
- Avoid generic names: `process`, `handle`, `doStuff`

### 4. Replace Original Code

Replace all instances with function call:
```
// Before
let total = 0;
for (let item of items) {
    total += item.price * item.quantity;
}

// After
let total = calculateOrderTotal(items);
```

### 5. Validate

- [ ] All duplications replaced
- [ ] Tests still pass
- [ ] No new bugs introduced
- [ ] Function name is clear
- [ ] Parameters are well-named
- [ ] Return value is obvious

## Examples

### Example 1: Extract Calculation

**Before:**
```python
# Appears in multiple places
discount = 0
if customer.is_premium:
    discount = price * 0.20
elif customer.years > 5:
    discount = price * 0.10
total = price - discount
```

**After:**
```python
def calculate_customer_discount(customer, price):
    """Calculate discount based on customer status and tenure."""
    if customer.is_premium:
        return price * 0.20
    elif customer.years > 5:
        return price * 0.10
    return 0

# Usage
total = price - calculate_customer_discount(customer, price)
```

### Example 2: Extract Validation

**Before:**
```javascript
// Duplicated validation logic
if (!email || !email.includes('@') || email.length < 5) {
    throw new Error('Invalid email');
}
if (!password || password.length < 8 || !/\d/.test(password)) {
    throw new Error('Invalid password');
}
```

**After:**
```javascript
function validateEmail(email) {
    if (!email || !email.includes('@') || email.length < 5) {
        throw new Error('Invalid email');
    }
}

function validatePassword(password) {
    if (!password || password.length < 8 || !/\d/.test(password)) {
        throw new Error('Invalid password');
    }
}

// Usage
validateEmail(email);
validatePassword(password);
```

### Example 3: Extract Complex Logic

**Before:**
```java
// Hard to understand what this does
if ((user.role == 'admin' || user.role == 'moderator') &&
    user.status == 'active' &&
    !user.isSuspended &&
    (user.permissions.contains('EDIT') || user.isOwner)) {
    // Allow edit
}
```

**After:**
```java
boolean canEditContent(User user) {
    boolean hasAdminRole = user.role == 'admin' || user.role == 'moderator';
    boolean isActiveUser = user.status == 'active' && !user.isSuspended;
    boolean hasEditPermission = user.permissions.contains('EDIT') || user.isOwner;

    return hasAdminRole && isActiveUser && hasEditPermission;
}

// Usage - much clearer intent
if (canEditContent(user)) {
    // Allow edit
}
```

## When NOT to Extract

- **One-time use:** Code that truly only appears once
- **Too simple:** `sum = a + b` doesn't need `calculateSum(a, b)`
- **Context-dependent:** Code that requires too much context to be portable
- **Premature abstraction:** Wait until you have 2-3 duplicates before extracting

## Anti-Patterns to Avoid

❌ **Over-extraction**
```javascript
function add(a, b) { return a + b; }  // Too simple
function getFirst(arr) { return arr[0]; }  // Too trivial
```

❌ **Poor naming**
```python
def do_stuff(x, y):  # What does this do?
def process(data):   # Process how?
```

❌ **Too many parameters**
```java
// If you need this many params, reconsider the design
calculatePrice(item, discount, tax, shipping, coupon, memberLevel, season)
```

## Best Practices

✅ **Single Responsibility:** Each function does one thing well
✅ **Pure when possible:** Same inputs = same outputs, no side effects
✅ **Clear contracts:** Obvious what goes in and what comes out
✅ **Appropriate level:** Not too high-level, not too low-level
✅ **Self-documenting:** Name and signature explain the purpose

## Follow-up Actions

After extracting:
1. Look for other opportunities to use the new function
2. Add unit tests for the extracted function
3. Update documentation if needed
4. Consider if related functions should be grouped in a module/class
