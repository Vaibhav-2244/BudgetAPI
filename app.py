from flask import Flask, request, jsonify
import pyodbc
from config import Config

app = Flask(__name__)

# Database connection
def get_db_connection():
    try:
        conn = pyodbc.connect(Config.CONNECTION_STRING)
        return conn
    except Exception as e:
        print("Connection failed:", e)
        return None

# ------------------ USERS ------------------

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (username, email, password_hash)
        VALUES (?, ?, ?)
    """, (username, email, password))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User created successfully"}), 201

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username, email FROM users")
    users = [{"id": row[0], "username": row[1], "email": row[2]} for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(users)

# ------------------ INCOME ------------------

@app.route('/income', methods=['POST'])
def add_income():
    data = request.get_json()
    user_id = data['user_id']
    amount = data['amount']
    source = data['source']
    income_date = data['income_date']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO income (user_id, amount, source, income_date)
        VALUES (?, ?, ?, ?)
    """, (user_id, amount, source, income_date))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Income added successfully"}), 201

@app.route('/income/<int:user_id>', methods=['GET'])
def get_income(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT amount, source, income_date FROM income WHERE user_id = ?", (user_id,))
    income = [{"amount": row[0], "source": row[1], "date": str(row[2])} for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(income)

# ------------------ EXPENSES ------------------

@app.route('/expenses', methods=['POST'])
def add_expense():
    data = request.get_json()
    user_id = data['user_id']
    amount = data['amount']
    category = data['category']
    description = data['description']
    expense_date = data['expense_date']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO expenses (user_id, amount, category, description, expense_date)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, amount, category, description, expense_date))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Expense added successfully"}), 201

@app.route('/expenses/<int:user_id>', methods=['GET'])
def get_expenses(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT amount, category, description, expense_date FROM expenses WHERE user_id = ?", (user_id,))
    expenses = [{
        "amount": row[0],
        "category": row[1],
        "description": row[2],
        "date": str(row[3])
    } for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(expenses)

# ------------------ SAVINGS ------------------

@app.route('/savings', methods=['POST'])
def add_saving():
    data = request.get_json()
    user_id = data['user_id']
    goal_name = data['goal_name']
    target_amount = data['target_amount']
    saved_amount = data.get('saved_amount', 0)
    start_date = data['start_date']
    end_date = data['end_date']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO savings (user_id, goal_name, target_amount, saved_amount, start_date, end_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, goal_name, target_amount, saved_amount, start_date, end_date))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Saving goal added"}), 201

@app.route('/savings/<int:user_id>', methods=['GET'])
def get_savings(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT goal_name, target_amount, saved_amount, start_date, end_date 
        FROM savings 
        WHERE user_id = ?
    """, (user_id,))
    savings = [{
        "goal": row[0],
        "target": float(row[1]),
        "saved": float(row[2]),
        "start": str(row[3]),
        "end": str(row[4])
    } for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(savings)

# ------------------ BUDGETS ------------------

@app.route('/budgets', methods=['POST'])
def add_budget():
    data = request.get_json()
    user_id = data['user_id']
    category = data['category']
    budget_amount = data['budget_amount']
    month_year = data['month_year']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO budgets (user_id, category, budget_amount, month_year)
        VALUES (?, ?, ?, ?)
    """, (user_id, category, budget_amount, month_year))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Budget set successfully"}), 201

@app.route('/budgets/<int:user_id>', methods=['GET'])
def get_budgets(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category, budget_amount, month_year FROM budgets WHERE user_id = ?", (user_id,))
    budgets = [{
        "category": row[0],
        "amount": float(row[1]),
        "month": row[2]
    } for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(budgets)

# ------------------ ALERTS ------------------

@app.route('/alerts/<int:user_id>', methods=['GET'])
def get_alerts(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT alert_type, message, triggered_on, is_read FROM alerts WHERE user_id = ?", (user_id,))
    alerts = [{
        "type": row[0],
        "message": row[1],
        "triggered_on": str(row[2]),
        "is_read": bool(row[3])
    } for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(alerts)

# ------------------ ROOT ------------------

@app.route('/')
def index():
    return "Budget Tracker API is running...."

# ------------------ RUN ------------------

if __name__ == '__main__':
    app.run()
