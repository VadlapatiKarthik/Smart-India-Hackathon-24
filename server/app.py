from flask import Flask, render_template, request, redirect, url_for, session, flash
from utils.helpers import get_user_by_credentials
import os

# Initialize Flask app with correct template path
app = Flask(
    __name__,
    template_folder='../client/templates',  # dashboard HTMLs
    static_folder='../client/static'        # if you add any CSS/JS later
)

app.secret_key = 'supersecretkey'  # Use os.environ.get("SECRET_KEY") in production

@app.route('/')
def home():
    return render_template('index.html')  # now resolved from client/

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

    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/user/dashboard')
def user_dashboard():
    if session.get('role') != 'user':
        return redirect(url_for('login'))
    return render_template('userdashboard.html', username=session['username'])

@app.route('/healthcare/dashboard')
def healthcare_dashboard():
    if session.get('role') != 'healthcare':
        return redirect(url_for('login'))
    return render_template('healthcare-dashboard.html', username=session['username'])

@app.route('/government/dashboard')
def government_dashboard():
    if session.get('role') != 'government':
        return redirect(url_for('login'))
    return render_template('government-dashboard.html', username=session['username'])

# 🟢 Bind to 0.0.0.0 so Render can expose it
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render auto-assigns this
    app.run(host='0.0.0.0', port=port)
