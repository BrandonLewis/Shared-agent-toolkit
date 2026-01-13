---
description: Simplify complex code to improve readability and maintainability
args:
  - name: file-path
    description: Path to file containing complex code
    required: false
  - name: focus
    description: What to simplify (conditionals, loops, functions, naming)
    required: false
---

# Simplify Code

Make complex code simpler and more readable without changing behavior.

## What to Simplify

{{#if focus}}
Focus on simplifying: **{{focus}}**
{{else}}
Look for opportunities to simplify:
- Complex conditional logic
- Nested loops and branches
- Long functions
- Unclear variable names
- Magic numbers and strings
- Complicated expressions
{{/if}}

## Simplification Techniques

### 1. Simplify Conditionals

#### Early Returns
```python
# Before: Nested conditions
def process_order(order):
    if order is not None:
        if order.is_valid():
            if order.total > 0:
                return calculate_shipping(order)
            else:
                return 0
        else:
            return None
    else:
        return None

# After: Early returns
def process_order(order):
    if order is None or not order.is_valid():
        return None
    if order.total <= 0:
        return 0
    return calculate_shipping(order)
```

#### Extract Boolean Variables
```javascript
// Before: Complex condition
if ((user.role === 'admin' || user.role === 'moderator') &&
    user.status === 'active' &&
    !user.isSuspended &&
    (user.hasPermission('EDIT') || user.isOwner)) {
    // ...
}

// After: Named booleans
const isPrivilegedUser = user.role === 'admin' || user.role === 'moderator';
const isActiveUser = user.status === 'active' && !user.isSuspended;
const canEdit = user.hasPermission('EDIT') || user.isOwner;

if (isPrivilegedUser && isActiveUser && canEdit) {
    // ...
}
```

#### Replace Nested with Guard Clauses
```java
// Before: Deeply nested
public void processPayment(Payment payment) {
    if (payment != null) {
        if (payment.isValid()) {
            if (payment.amount > 0) {
                if (hasBalance(payment.amount)) {
                    chargeCard(payment);
                } else {
                    throw new InsufficientFundsException();
                }
            } else {
                throw new InvalidAmountException();
            }
        } else {
            throw new InvalidPaymentException();
        }
    } else {
        throw new NullPaymentException();
    }
}

// After: Guard clauses
public void processPayment(Payment payment) {
    if (payment == null) {
        throw new NullPaymentException();
    }
    if (!payment.isValid()) {
        throw new InvalidPaymentException();
    }
    if (payment.amount <= 0) {
        throw new InvalidAmountException();
    }
    if (!hasBalance(payment.amount)) {
        throw new InsufficientFundsException();
    }

    chargeCard(payment);
}
```

### 2. Simplify Loops

#### Use Higher-Order Functions
```python
# Before: Manual loop
results = []
for item in items:
    if item.is_active:
        results.append(item.name.upper())

# After: List comprehension
results = [item.name.upper() for item in items if item.is_active]

# Or using map/filter
results = [name.upper() for name in map(lambda i: i.name, filter(lambda i: i.is_active, items))]
```

#### Replace Loop with Built-in
```javascript
// Before: Manual sum
let total = 0;
for (let i = 0; i < prices.length; i++) {
    total += prices[i];
}

// After: reduce
const total = prices.reduce((sum, price) => sum + price, 0);
```

### 3. Simplify Functions

#### Break Down Long Functions
```python
# Before: One long function (50+ lines)
def process_user_registration(data):
    # Validate email
    email = data.get('email')
    if not email or '@' not in email:
        raise ValueError('Invalid email')

    # Validate password
    password = data.get('password')
    if not password or len(password) < 8:
        raise ValueError('Invalid password')

    # Hash password
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)

    # Create user
    user = User(email=email, password_hash=key, salt=salt)

    # Send welcome email
    subject = 'Welcome!'
    body = f'Thanks for joining, {email}'
    send_email(email, subject, body)

    # Log registration
    logger.info(f'User registered: {email}')

    return user

# After: Broken into focused functions
def process_user_registration(data):
    validate_registration_data(data)
    user = create_user(data)
    send_welcome_email(user)
    log_registration(user)
    return user

def validate_registration_data(data):
    validate_email(data.get('email'))
    validate_password(data.get('password'))

def validate_email(email):
    if not email or '@' not in email:
        raise ValueError('Invalid email')

def validate_password(password):
    if not password or len(password) < 8:
        raise ValueError('Invalid password')

def create_user(data):
    password_hash, salt = hash_password(data['password'])
    return User(email=data['email'], password_hash=password_hash, salt=salt)

def hash_password(password):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return key, salt

def send_welcome_email(user):
    send_email(user.email, 'Welcome!', f'Thanks for joining, {user.email}')

def log_registration(user):
    logger.info(f'User registered: {user.email}')
```

#### Reduce Parameters
```java
// Before: Too many parameters
public Order createOrder(String customerId, String productId, int quantity,
                        String shippingAddress, String billingAddress,
                        String paymentMethod, String couponCode,
                        boolean giftWrap, String giftMessage) {
    // ...
}

// After: Use object
public class OrderRequest {
    private String customerId;
    private String productId;
    private int quantity;
    private Address shipping;
    private Address billing;
    private Payment payment;
    private GiftOptions giftOptions;
}

public Order createOrder(OrderRequest request) {
    // ...
}
```

### 4. Simplify Naming

#### Replace Magic Numbers
```javascript
// Before: Magic numbers
setTimeout(fetchData, 86400000);
if (user.age >= 21) { /* ... */ }

// After: Named constants
const ONE_DAY_MS = 24 * 60 * 60 * 1000;
const LEGAL_DRINKING_AGE = 21;

setTimeout(fetchData, ONE_DAY_MS);
if (user.age >= LEGAL_DRINKING_AGE) { /* ... */ }
```

#### Use Descriptive Names
```python
# Before: Unclear names
def f(x, y, z):
    a = x * y
    b = a * z
    return b * 0.2

# After: Clear names
def calculate_sales_tax(price, quantity, tax_rate):
    subtotal = price * quantity
    total = subtotal * tax_rate
    return total * 0.2
```

### 5. Simplify Expressions

#### De-Morgan's Laws
```javascript
// Before: Complex negation
if (!(isAdmin || isModerator)) { /* ... */ }

// After: Simplified
if (!isAdmin && !isModerator) { /* ... */ }

// Before: Double negative
if (!(!user.isActive)) { /* ... */ }

// After: Positive
if (user.isActive) { /* ... */ }
```

#### Extract Complex Calculations
```python
# Before: Inline complex calculation
total = (base_price * quantity * (1 - discount_rate)) * (1 + tax_rate) + shipping_cost

# After: Step-by-step
subtotal = base_price * quantity
discounted = subtotal * (1 - discount_rate)
with_tax = discounted * (1 + tax_rate)
total = with_tax + shipping_cost
```

## Simplification Checklist

When simplifying code, verify:

- [ ] **Behavior unchanged:** Tests still pass
- [ ] **Readability improved:** Code is easier to understand
- [ ] **Complexity reduced:** Cyclomatic complexity lower
- [ ] **Names clearer:** Variables/functions have descriptive names
- [ ] **Logic flattened:** Fewer nested conditions
- [ ] **Functions focused:** Each function does one thing
- [ ] **No magic values:** Constants are named
- [ ] **DRY applied:** Duplication removed

## Complexity Metrics

### Cyclomatic Complexity
Counts independent paths through code:
- **1-10:** Simple, easy to test
- **11-20:** Moderate, needs attention
- **21+:** Complex, should refactor

```python
# High complexity (6 paths)
def calculate_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

# Lower complexity with data structure
GRADE_THRESHOLDS = [(90, 'A'), (80, 'B'), (70, 'C'), (60, 'D')]

def calculate_grade(score):
    for threshold, grade in GRADE_THRESHOLDS:
        if score >= threshold:
            return grade
    return 'F'
```

### Nesting Depth
Limit nesting to 3 levels:
```javascript
// ❌ Too deep (4 levels)
if (a) {
    if (b) {
        if (c) {
            if (d) {
                // ...
            }
        }
    }
}

// ✅ Flattened
if (!a) return;
if (!b) return;
if (!c) return;
if (!d) return;
// ...
```

## Tools for Analysis

**Python:**
```bash
# Radon for complexity metrics
pip install radon
radon cc your_file.py -s

# McCabe complexity checker
flake8 --max-complexity=10 your_file.py
```

**JavaScript:**
```bash
# ESLint complexity rules
npm install eslint
eslint --rule 'complexity: [error, 10]' your_file.js
```

## Refactoring Priority

Prioritize simplifying code that is:
1. **High complexity + frequently changed** 🔴 Critical
2. **High complexity + stable** 🟡 Medium
3. **Low complexity + frequently changed** 🟢 Low priority
4. **Low complexity + stable** ⚪ Leave alone

## Best Practices

✅ **One thing at a time:** Don't mix simplification with feature changes
✅ **Small steps:** Make incremental improvements
✅ **Test after each change:** Ensure behavior unchanged
✅ **Name things well:** Good names reduce need for comments
✅ **Prefer composition:** Build complex from simple parts
✅ **Limit scope:** Small functions, focused classes
✅ **Use language idioms:** Leverage built-in patterns

## Anti-Patterns to Avoid

❌ **Over-simplification:** Breaking code into too-tiny pieces
❌ **Premature optimization:** Simplify for readability first
❌ **Clever code:** Simple doesn't mean clever/terse
❌ **Cargo cult:** Don't apply patterns blindly

## Success Metrics

Code is simpler when:
- ✅ Junior developers can understand it
- ✅ Cyclomatic complexity is reduced
- ✅ Nesting depth is minimal
- ✅ Function length is reasonable (< 30 lines)
- ✅ Names explain intent
- ✅ Tests are easier to write
- ✅ Bugs are easier to find
