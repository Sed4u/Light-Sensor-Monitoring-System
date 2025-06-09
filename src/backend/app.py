from flask import Flask, render_template, redirect, url_for, flash, session  # Add `session` import
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.warning_routes import warning_bp
from dotenv import load_dotenv
import os
from influxdb_client import InfluxDBClient

try:
    from src.backend.routes.data_routes import data_bp
except ImportError as e:
    print(f"ImportError: {e}")
    raise

from src.backend.database import db

load_dotenv()

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')
CORS(app)

app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mds:mdspass@postgres:5432/dbmds'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(data_bp, url_prefix='/data')
app.register_blueprint(warning_bp, url_prefix='/warnings')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please log in to access the dashboard.", "error")
        return redirect(url_for('auth.login'))
    user_id = session['user_id']
    return render_template('dashboard.html', username=session.get('username'), user_id=user_id)

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)