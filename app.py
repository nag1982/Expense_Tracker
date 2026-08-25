import os
import sqlite3
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from functools import wraps
from pathlib import Path

from flask import Flask, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = Path(__file__).parent
DEFAULT_DATABASE = Path("/tmp/expense_tracker.db") if os.environ.get("VERCEL") else BASE_DIR / "expense_tracker.db"
DATABASE = Path(os.environ.get("DATABASE_PATH", DEFAULT_DATABASE))
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")
app.config["DATABASE"] = str(DATABASE)

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, currency TEXT NOT NULL DEFAULT 'INR', created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, name TEXT NOT NULL, type TEXT NOT NULL CHECK(type IN ('EXPENSE','INCOME')), FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE, UNIQUE(user_id, name, type));
CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, type TEXT NOT NULL CHECK(type IN ('EXPENSE','INCOME')), amount NUMERIC NOT NULL CHECK(amount > 0), category_id INTEGER, transaction_date TEXT NOT NULL, payment_method TEXT, description TEXT NOT NULL, notes TEXT, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE, FOREIGN KEY(category_id) REFERENCES categories(id) ON DELETE SET NULL);
CREATE TABLE IF NOT EXISTS budgets (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, category_id INTEGER, amount NUMERIC NOT NULL CHECK(amount > 0), month INTEGER NOT NULL CHECK(month BETWEEN 1 AND 12), year INTEGER NOT NULL, UNIQUE(user_id, category_id, month, year), FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE, FOREIGN KEY(category_id) REFERENCES categories(id) ON DELETE SET NULL);
CREATE INDEX IF NOT EXISTS idx_transactions_user_date ON transactions(user_id, transaction_date);
"""
DEFAULT_CATEGORIES = [("Food", "EXPENSE"), ("Housing", "EXPENSE"), ("Transport", "EXPENSE"), ("Bills", "EXPENSE"), ("Shopping", "EXPENSE"), ("Health", "EXPENSE"), ("Entertainment", "EXPENSE"), ("Salary", "INCOME"), ("Freelance", "INCOME"), ("Other income", "INCOME")]


def db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.before_request
def setup():
    db().executescript(SCHEMA)
    g.user = None
    if session.get("user_id"):
        g.user = db().execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()


@app.teardown_appcontext
def close_db(_error):
    connection = g.pop("db", None)
    if connection:
        connection.close()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not g.user:
            flash("Please sign in to continue.", "error")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


def money(value):
    return f"{Decimal(str(value or 0)):,.2f}"


def parse_amount(value):
    try:
        amount = Decimal(value).quantize(Decimal("0.01"))
        if amount <= 0:
            raise InvalidOperation
        return amount
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("Enter an amount greater than zero.")


@app.template_filter("money")
def money_filter(value):
    return money(value)


@app.context_processor
def inject_globals():
    return {"current_user": g.get("user"), "today": date.today().isoformat()}


@app.route("/")
def index():
    return redirect(url_for("dashboard" if g.user else "login"))


@app.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        name, email, password = request.form.get("name", "").strip(), request.form.get("email", "").strip().lower(), request.form.get("password", "")
        if len(name) < 2 or "@" not in email or len(password) < 8:
            flash("Use a name, a valid email, and a password with at least 8 characters.", "error")
        else:
            try:
                cursor = db().execute("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)", (name, email, generate_password_hash(password)))
                user_id = cursor.lastrowid
                db().executemany("INSERT INTO categories (user_id, name, type) VALUES (?, ?, ?)", [(user_id, *category) for category in DEFAULT_CATEGORIES])
                db().commit()
                flash("Account created. Welcome to Ledgerly.", "success")
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                flash("That email is already registered.", "error")
    return render_template("auth.html", mode="register")


@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        user = db().execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if not user or not check_password_hash(user["password_hash"], request.form.get("password", "")):
            flash("Email or password is incorrect.", "error")
        else:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("dashboard"))
    return render_template("auth.html", mode="login")


@app.get("/logout")
def logout():
    session.clear()
    flash("You have been signed out.", "success")
    return redirect(url_for("login"))


@app.get("/dashboard")
@login_required
def dashboard():
    month = date.today().strftime("%Y-%m")
    totals = db().execute("SELECT type, COALESCE(SUM(amount), 0) total FROM transactions WHERE user_id = ? GROUP BY type", (g.user["id"],)).fetchall()
    total = {row["type"]: row["total"] for row in totals}
    monthly = db().execute("SELECT type, COALESCE(SUM(amount), 0) total FROM transactions WHERE user_id = ? AND transaction_date LIKE ? GROUP BY type", (g.user["id"], month + "%")).fetchall()
    month_total = {row["type"]: row["total"] for row in monthly}
    budget = db().execute("SELECT COALESCE(SUM(amount), 0) FROM budgets WHERE user_id = ? AND month = ? AND year = ? AND category_id IS NULL", (g.user["id"], date.today().month, date.today().year)).fetchone()[0]
    spent = month_total.get("EXPENSE", 0)
    recent = db().execute("SELECT t.*, c.name category FROM transactions t LEFT JOIN categories c ON c.id = t.category_id WHERE t.user_id = ? ORDER BY transaction_date DESC, id DESC LIMIT 6", (g.user["id"],)).fetchall()
    categories = db().execute("SELECT c.name, COALESCE(SUM(t.amount), 0) total FROM categories c LEFT JOIN transactions t ON t.category_id = c.id AND t.user_id = ? AND t.type = 'EXPENSE' AND t.transaction_date LIKE ? WHERE c.user_id = ? AND c.type = 'EXPENSE' GROUP BY c.id ORDER BY total DESC LIMIT 5", (g.user["id"], month + "%", g.user["id"])).fetchall()
    return render_template("dashboard.html", total_income=total.get("INCOME", 0), total_expense=total.get("EXPENSE", 0), balance=total.get("INCOME", 0) - total.get("EXPENSE", 0), month_income=month_total.get("INCOME", 0), month_expense=spent, budget=budget, budget_percent=min(round((spent / budget) * 100) if budget else 0, 100), recent=recent, categories=categories)


@app.route("/transactions")
@login_required
def transactions():
    filters = ["t.user_id = ?"]
    values = [g.user["id"]]
    for field in ("type", "payment_method"):
        if request.args.get(field):
            filters.append(f"t.{field} = ?")
            values.append(request.args[field])
    if request.args.get("search"):
        filters.append("(t.description LIKE ? OR t.notes LIKE ?)")
        values.extend([f"%{request.args['search']}%"] * 2)
    rows = db().execute(f"SELECT t.*, c.name category FROM transactions t LEFT JOIN categories c ON c.id = t.category_id WHERE {' AND '.join(filters)} ORDER BY transaction_date DESC, id DESC", values).fetchall()
    return render_template("transactions.html", transactions=rows)


@app.route("/transactions/new", methods=("GET", "POST"))
@login_required
def new_transaction():
    if request.method == "POST":
        try:
            amount = parse_amount(request.form.get("amount", ""))
            description = request.form.get("description", "").strip()
            if not description:
                raise ValueError("Add a short description for this transaction.")
            db().execute("INSERT INTO transactions (user_id, type, amount, category_id, transaction_date, payment_method, description, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (g.user["id"], request.form["type"], str(amount), request.form.get("category_id") or None, request.form.get("transaction_date") or date.today().isoformat(), request.form.get("payment_method"), description, request.form.get("notes", "").strip()))
            db().commit()
            flash("Transaction saved successfully.", "success")
            return redirect(url_for("transactions"))
        except (ValueError, KeyError):
            flash("Check the transaction type, amount, date, and description.", "error")
    categories = db().execute("SELECT * FROM categories WHERE user_id = ? ORDER BY type, name", (g.user["id"],)).fetchall()
    return render_template("transaction_form.html", categories=categories, transaction=None)


@app.post("/transactions/<int:transaction_id>/delete")
@login_required
def delete_transaction(transaction_id):
    db().execute("DELETE FROM transactions WHERE id = ? AND user_id = ?", (transaction_id, g.user["id"]))
    db().commit()
    flash("Transaction deleted.", "success")
    return redirect(request.referrer or url_for("transactions"))

@app.route("/transactions/<int:transaction_id>/edit", methods=("GET", "POST"))
@login_required
def edit_transaction(transaction_id):
    transaction = db().execute("SELECT * FROM transactions WHERE id = ? AND user_id = ?", (transaction_id, g.user["id"])).fetchone()
    if not transaction:
        flash("Transaction not found.", "error")
        return redirect(url_for("transactions"))
    if request.method == "POST":
        try:
            amount = parse_amount(request.form.get("amount", ""))
            description = request.form.get("description", "").strip()
            if not description:
                raise ValueError("Description is required.")
            db().execute("UPDATE transactions SET type = ?, amount = ?, category_id = ?, transaction_date = ?, payment_method = ?, description = ?, notes = ? WHERE id = ? AND user_id = ?", (request.form["type"], str(amount), request.form.get("category_id") or None, request.form.get("transaction_date"), request.form.get("payment_method"), description, request.form.get("notes", "").strip(), transaction_id, g.user["id"]))
            db().commit()
            flash("Transaction updated successfully.", "success")
            return redirect(url_for("transactions"))
        except (ValueError, KeyError):
            flash("Check the transaction type, amount, date, and description.", "error")
    categories = db().execute("SELECT * FROM categories WHERE user_id = ? ORDER BY type, name", (g.user["id"],)).fetchall()
    return render_template("transaction_form.html", categories=categories, transaction=transaction)


@app.route("/budgets", methods=("GET", "POST"))
@login_required
def budgets():
    if request.method == "POST":
        try:
            amount = parse_amount(request.form.get("amount", ""))
            month, year = int(request.form["month"]), int(request.form["year"])
            category_id = request.form.get("category_id") or None
            db().execute("INSERT INTO budgets (user_id, category_id, amount, month, year) VALUES (?, ?, ?, ?, ?) ON CONFLICT(user_id, category_id, month, year) DO UPDATE SET amount = excluded.amount", (g.user["id"], category_id, str(amount), month, year))
            db().commit()
            flash("Budget updated successfully.", "success")
            return redirect(url_for("budgets"))
        except (ValueError, KeyError):
            flash("Enter a valid positive budget amount.", "error")
    month, year = date.today().month, date.today().year
    rows = db().execute("SELECT b.*, c.name category, COALESCE((SELECT SUM(t.amount) FROM transactions t WHERE t.user_id = b.user_id AND t.category_id = b.category_id AND t.type = 'EXPENSE' AND strftime('%m', t.transaction_date) = printf('%02d', b.month) AND strftime('%Y', t.transaction_date) = CAST(b.year AS TEXT)), 0) spent FROM budgets b LEFT JOIN categories c ON c.id = b.category_id WHERE b.user_id = ? ORDER BY b.category_id IS NOT NULL, b.amount DESC", (g.user["id"],)).fetchall()
    categories = db().execute("SELECT * FROM categories WHERE user_id = ? AND type = 'EXPENSE' ORDER BY name", (g.user["id"],)).fetchall()
    return render_template("budgets.html", budgets=rows, categories=categories, month=month, year=year)


@app.get("/reports")
@login_required
def reports():
    month = date.today().strftime("%Y-%m")
    category_rows = db().execute("SELECT COALESCE(c.name, 'Uncategorized') name, SUM(t.amount) total FROM transactions t LEFT JOIN categories c ON c.id = t.category_id WHERE t.user_id = ? AND t.type = 'EXPENSE' AND t.transaction_date LIKE ? GROUP BY c.name ORDER BY total DESC", (g.user["id"], month + "%")).fetchall()
    trend = db().execute("SELECT substr(transaction_date, 1, 7) month, SUM(CASE WHEN type='INCOME' THEN amount ELSE 0 END) income, SUM(CASE WHEN type='EXPENSE' THEN amount ELSE 0 END) expense FROM transactions WHERE user_id = ? GROUP BY month ORDER BY month DESC LIMIT 6", (g.user["id"],)).fetchall()
    return render_template("reports.html", category_rows=category_rows, trend=list(reversed(trend)))


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
