from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
transactions = []
balance = 0.0

@app.route('/')
def index():
    total_income = sum(t['amount'] for t in transactions if t['type'] == 'Income')
    total_expense = sum(t['amount'] for t in transactions if t['type'] == 'Expense')
    return render_template("index.html", transactions=transactions, balance=balance, income=total_income, expense=total_expense)

@app.route('/add', methods=['POST'])
def add_transaction():
    global balance
    amount = float(request.form['amount'])
    category = request.form['category'].lower()
    ttype = request.form['type']

    if ttype == 'Income':
        balance += amount
    elif ttype == 'Expense':
        if amount > balance:
            return redirect(url_for('index'))  # Optional: add error message
        balance -= amount

    transactions.append({
        "type": ttype,
        "amount": amount,
        "category": category
    })
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

