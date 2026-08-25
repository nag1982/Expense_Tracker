# Expense Tracker — Application Development Plan

## 1. Application Name

**Expense Tracker**

A Python-based web application that allows users to record, categorize, monitor, and analyze their daily income and expenses.

---

## 2. Problem Statement

Managing personal expenses through notebooks, spreadsheets, or multiple applications can be time-consuming and makes it difficult to understand spending patterns.

The **Expense Tracker** will provide a simple centralized application where users can:

- Record income and expenses.
- Categorize transactions.
- Track monthly spending.
- Set budgets.
- View spending summaries and charts.
- Search and filter transactions.
- Monitor remaining budget.
- Export expense data.

The application should have a clean, responsive UI and be deployable to **Vercel through GitHub**.

---

## 3. Target Users

| User | Use Case |
|---|---|
| Individuals | Track personal daily expenses |
| Students | Monitor limited monthly budgets |
| Working professionals | Track salary, bills and discretionary spending |
| Families | Monitor household expenses |
| Freelancers | Track business-related expenses |
| Small business owners | Maintain basic income/expense records |

---

## 4. Main Features

### A. Dashboard

- Total income
- Total expenses
- Current balance
- Monthly expenses
- Monthly income
- Budget utilization
- Recent transactions
- Expense category breakdown
- Monthly spending chart

### B. Expense Management

Users can:

- Add expense
- Edit expense
- Delete expense
- View expense details
- Categorize expenses
- Add notes
- Select payment method
- Select transaction date

Example categories:

- Food
- Shopping
- Transportation
- Rent
- Utilities
- Healthcare
- Education
- Entertainment
- Travel
- Insurance
- Other

### C. Income Management

Allow users to record:

- Salary
- Freelance income
- Business income
- Investments
- Other income

### D. Budget Management

Users can:

- Set monthly budget
- Set category-wise budgets
- Track budget utilization
- See remaining budget
- Receive visual warnings when approaching the limit

Example:

> Monthly Budget: ₹50,000  
> Spent: ₹37,500  
> Remaining: ₹12,500  
> Utilization: 75%

### E. Reports & Analytics

Provide:

- Monthly expense report
- Category-wise expense report
- Income vs expense
- Monthly trend
- Highest spending categories
- Payment-method analysis

Charts can be implemented using **Plotly** or **Chart.js**.

### F. Search & Filters

Users should be able to filter by:

- Date
- Category
- Transaction type
- Payment method
- Amount
- Description

### G. Export

Allow users to export transactions to:

- CSV
- Excel

---

## 5. Pages / Screens Required

### 1. Login Page

Fields:

- Email
- Password
- Login button
- Forgot password
- Register

### 2. Registration Page

Fields:

- Name
- Email
- Password
- Confirm password

### 3. Dashboard

Display:

- Total Income
- Total Expense
- Balance
- Monthly Expense Chart
- Expense by Category
- Recent Transactions

### 4. Transactions Page

Features:

- Transaction list
- Add transaction
- Edit
- Delete
- Search
- Filter
- Sort
- Pagination

### 5. Add Expense Page

Fields:

- Amount
- Category
- Date
- Payment Method
- Description
- Notes
- Save Expense

### 6. Add Income Page

Fields:

- Amount
- Income Source
- Date
- Description
- Notes
- Save Income

### 7. Budget Page

Features:

- Monthly budget
- Category budgets
- Budget utilization
- Remaining amount
- Progress indicators

### 8. Reports Page

Charts:

- Monthly expenses
- Category expenses
- Income vs expense
- Monthly trends

### 9. Categories Page

Allow users to:

- Add category
- Edit category
- Delete category
- Assign category type

### 10. Profile / Settings

Features:

- Update profile
- Currency
- Password change
- Notification preferences
- Logout

---

## 6. Technology Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| UI | Bootstrap / Tailwind CSS |
| Backend | Python |
| Web Framework | Flask |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Authentication | Flask-Login / secure session authentication |
| Validation | WTForms / server-side validation |
| Charts | Chart.js |
| API | Flask REST endpoints |
| Testing | Pytest |
| Code Quality | Ruff / Black |
| Version Control | Git |
| Repository | GitHub |
| Deployment | Vercel |
| Database Hosting | Vercel-compatible PostgreSQL provider |
| Environment Variables | Vercel Environment Variables |

### Recommended Architecture

```text
                 ┌─────────────────┐
                 │      User       │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │     Vercel      │
                 │    Web App      │
                 └────────┬────────┘
                          │
                 ┌────────▼────────┐
                 │ Python / Flask  │
                 │   Application   │
                 └────────┬────────┘
                          │
              ┌───────────▼───────────┐
              │      SQLAlchemy       │
              └───────────┬───────────┘
                          │
                 ┌────────▼────────┐
                 │   PostgreSQL    │
                 │    Database     │
                 └─────────────────┘
```

---

## 7. Project Folder Structure

```text
expense-tracker/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── transaction.py
│   │   ├── category.py
│   │   └── budget.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── transactions.py
│   │   ├── budgets.py
│   │   └── reports.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── transaction_service.py
│   │   ├── budget_service.py
│   │   └── report_service.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── transactions.html
│   │   ├── add_expense.html
│   │   ├── add_income.html
│   │   ├── budgets.html
│   │   ├── reports.html
│   │   └── settings.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css
│       ├── js/
│       │   ├── dashboard.js
│       │   ├── transactions.js
│       │   └── charts.js
│       └── images/
│
├── tests/
│   ├── test_auth.py
│   ├── test_transactions.py
│   ├── test_budget.py
│   └── test_reports.py
│
├── migrations/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── vercel.json
├── run.py
├── README.md
├── PLAN.md
└── LICENSE
```

---

## 8. Data That Needs to Be Stored

### Users

```text
User
----------------
id
name
email
password_hash
currency
created_at
updated_at
```

### Transactions

A single transaction table can handle both income and expenses.

```text
Transaction
----------------
id
user_id
type
amount
category_id
transaction_date
payment_method
description
notes
created_at
updated_at
```

`type`:

```text
INCOME
EXPENSE
```

### Categories

```text
Category
----------------
id
user_id
name
type
description
created_at
```

### Budgets

```text
Budget
----------------
id
user_id
category_id
amount
month
year
created_at
updated_at
```

### Payment Methods

Possible values:

```text
Cash
Credit Card
Debit Card
UPI
Bank Transfer
Net Banking
Other
```

---

## 9. Development Steps

### Phase 1 — Requirement & Architecture

- Define application requirements.
- Define user journeys.
- Design database schema.
- Define application architecture.
- Define UI wireframes.
- Define API requirements.
- Define security requirements.

**Deliverable:** Architecture + database design.

### Phase 2 — Project Setup

Set up:

```text
Python
Flask
SQLAlchemy
PostgreSQL
Pytest
Git
```

Create:

```text
requirements.txt
.env.example
.gitignore
README.md
```

### Phase 3 — Database Development

Implement:

- User model
- Transaction model
- Category model
- Budget model

Create database migrations and relationships.

### Phase 4 — Authentication

Implement:

- Registration
- Login
- Logout
- Password hashing
- Session management
- Authentication middleware
- Authorization

Security requirements:

- Never store plain-text passwords.
- Validate all user input.
- Protect authenticated routes.
- Use environment variables for secrets.
- Avoid exposing database credentials.

### Phase 5 — Expense & Income Module

Implement CRUD operations for:

- Expenses
- Income
- Categories

Add:

- Validation
- Search
- Filtering
- Sorting
- Pagination

### Phase 6 — Dashboard

Calculate:

```text
Total Income
Total Expense
Balance
Current Month Expense
Current Month Income
Budget Utilization
```

Display the results using dashboard cards and charts.

### Phase 7 — Budget Module

Implement:

- Create budget
- Edit budget
- Delete budget
- Category budget
- Monthly budget
- Budget utilization

### Phase 8 — Reports

Create:

- Expense by Category
- Income vs Expense
- Spending Trend
- Monthly comparison

### Phase 9 — UI/UX

Make the application:

- Responsive
- Mobile-friendly
- Desktop-friendly
- Simple to navigate
- Accessible
- Consistent

Recommended navigation:

```text
Dashboard
Transactions
Add Expense
Add Income
Budget
Reports
Categories
Settings
Logout
```

### Phase 10 — Testing

#### Unit Testing

Use Pytest to test:

- Authentication
- Transaction calculations
- Budget calculations
- Category operations
- Report calculations

#### API Testing

Test:

- GET
- POST
- PUT
- DELETE

#### UI Testing

Test:

- Login
- Registration
- Add expense
- Edit expense
- Delete expense
- Add income
- Budget creation
- Reports
- Logout

#### Security Testing

Test:

- Invalid login
- Unauthorized access
- SQL injection
- XSS
- Session handling
- Input validation
- Password security

---

## 10. GitHub Development Workflow

Recommended workflow:

```text
Developer
   │
   ▼
Local Development
   │
   ▼
Git
   │
   ▼
GitHub
   │
   ▼
Pull Request
   │
   ▼
Code Review
   │
   ▼
Merge to main
   │
   ▼
Vercel Deployment
```

Recommended branches:

```text
main
develop
feature/authentication
feature/transactions
feature/dashboard
feature/budget
feature/reports
```

---

## 11. Deployment Approach

### Step 1 — Create GitHub Repository

Create:

```text
expense-tracker
```

Push the application:

```bash
git init
git add .
git commit -m "Initial Expense Tracker application"
git branch -M main
git remote add origin <github-repository>
git push -u origin main
```

### Step 2 — Configure Vercel

Connect the GitHub repository to Vercel.

Configure:

```text
Framework: Python
Repository: expense-tracker
Branch: main
```

Vercel should automatically trigger deployments when changes are pushed to the repository.

### Step 3 — Environment Variables

Do **not** commit `.env` to GitHub.

Local:

```text
DATABASE_URL=
SECRET_KEY=
```

Configure the same variables securely in Vercel.

### Step 4 — Configure Python Application

Create the required Vercel configuration and Python entry point appropriate for the chosen Flask deployment structure.

For example:

```text
vercel.json
```

and expose the Flask application through the deployment entry point.

### Step 5 — PostgreSQL

Use a production PostgreSQL database rather than SQLite.

Recommended architecture:

```text
Vercel
   │
   ├── Flask Application
   │
   └── Environment Variables
             │
             ▼
        PostgreSQL
```

The database connection string should be stored as a Vercel environment variable.

### Step 6 — Production Testing

After deployment, test:

```text
✓ Application loads
✓ Registration works
✓ Login works
✓ Add expense works
✓ Edit expense works
✓ Delete expense works
✓ Add income works
✓ Dashboard calculations work
✓ Budget calculations work
✓ Reports work
✓ Database persistence works
✓ Logout works
✓ Mobile UI works
```

---

## 12. CI/CD Pipeline

A production-ready implementation can use:

```text
GitHub
   │
   ▼
Pull Request
   │
   ▼
Automated Tests
   │
   ├── Pytest
   ├── Linting
   └── Security checks
   │
   ▼
Merge
   │
   ▼
Vercel
   │
   ▼
Production Deployment
```

GitHub Actions can be added under:

```text
.github/
└── workflows/
    └── ci.yml
```

The pipeline can execute:

```bash
pip install -r requirements.txt
pytest
ruff check .
```

before allowing production changes to be merged.

Use Playwright, Python, Pytest for testing the application


---

## 13. Recommended MVP

For the first version, implement:

```text
1. Registration/Login
2. Dashboard
3. Add Expense
4. Add Income
5. Transaction List
6. Edit/Delete Transaction
7. Categories
8. Monthly Budget
9. Basic Reports
10. PostgreSQL
11. GitHub
12. Vercel deployment
```

### Version 2

```text
13. Excel/CSV export
14. Advanced reports
15. Recurring expenses
16. Budget alerts
17. Multiple currencies
18. Mobile optimization
19. Email notifications
20. Advanced analytics
```

### Version 3 — AI Features

```text
AI Expense Categorization
AI Spending Analysis
AI Budget Recommendations
AI Monthly Financial Summary
Natural-language expense search
Anomaly detection
```

---

## 14. Final Architecture

```text
                         USER
                           │
                           ▼
                  ┌─────────────────┐
                  │  Expense Tracker │
                  │   Web Interface  │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │      Flask      │
                  │ Python Backend  │
                  └────────┬────────┘
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
        Authentication Transactions   Reports
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                    ┌─────────────┐
                    │ SQLAlchemy  │
                    └──────┬──────┘
                           ▼
                    ┌─────────────┐
                    │ PostgreSQL  │
                    └─────────────┘

             SOURCE CONTROL / DEPLOYMENT

                    ┌─────────────┐
                    │   GitHub    │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Vercel    │
                    └─────────────┘
```

## Recommended Development Sequence

**Requirements → UI → Database → Flask Backend → Authentication → Transactions → Dashboard → Budget → Reports → Testing → GitHub → Vercel → Production Testing**
