from flask import Flask, render_template, request, redirect, url_for, session, flash
from utils.helpers import get_user_by_credentials  # 🔁 imported helper function
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace with env var in production


@app.route('/')
def home():
    return render_template('../client/index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form['role']
        username = request.form['username']
        password = request.form['password']

        user = get_user_by_credentials(username, password, role)

        if user:
            session['username'] = username
            session['role'] = role
            if role == 'user':
                return redirect(url_for('user_dashboard'))
            elif role == 'healthcare':
                return redirect(url_for('healthcare_dashboard'))
            elif role == 'government':
                return redirect(url_for('government_dashboard'))
        else:
            flash("Invalid credentials or role.")
            return redirect(url_for('login'))

    return render_template('../client/index.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/user/dashboard')
def user_dashboard():
    if session.get('role') != 'user':
        return redirect(url_for('login'))
    return render_template('../client/templates/userdashboard.html', username=session['username'])


@app.route('/healthcare/dashboard')
def healthcare_dashboard():
    if session.get('role') != 'healthcare':
        return redirect(url_for('login'))
    return render_template('../client/templates/healthcare-dashboard.html', username=session['username'])


@app.route('/government/dashboard')
def government_dashboard():
    if session.get('role') != 'government':
        return redirect(url_for('login'))
    return render_template('../client/templates/government-dashboard.html', username=session['username'])


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
