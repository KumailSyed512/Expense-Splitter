from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Database connection
DB_PATH = 'expenses.db'

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# API Endpoints

# Get all expenses
@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

# Add a new expense with equal or custom split
@app.route('/api/expenses', methods=['POST'])
def add_expense():
    data = request.json
    total_amount = data['totalAmount']
    participants = data['participants']
    split_type = data.get('splitType', 'equal')  # Default to 'equal' if not provided

    if split_type == 'equal':
        split_amount = total_amount / len(participants)
        split_amounts = [split_amount] * len(participants)
    elif split_type == 'custom':
        percentages = data['percentages']
        if len(percentages) != len(participants):
            return jsonify({'message': 'Number of percentages must match the number of participants'}), 400
        if sum(percentages) != 100:
            return jsonify({'message': 'Total percentage must equal 100'}), 400
        split_amounts = [(total_amount * (percentage / 100)) for percentage in percentages]
    else:
        return jsonify({'message': 'Invalid split type'}), 400

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (total_amount, participants, split_amount) VALUES (?, ?, ?)",
        (total_amount, ','.join(participants), ','.join(map(str, split_amounts)))
    )
    conn.commit()
    conn.close()

    return jsonify({
        'message': 'Expense added successfully',
        'totalAmount': total_amount,
        'splitAmounts': split_amounts,
        'participants': participants
    }), 201

# Delete an expense by ID
@app.route('/api/expenses/<int:id>', methods=['DELETE'])
def delete_expense(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': f'Expense with ID {id} deleted successfully'}), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
