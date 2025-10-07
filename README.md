
# 🏭 MetalWorks Price Management System

A smart, automated pricing system for metal distributors and manufacturers. Automatically updates product prices when raw material costs change using a proportional pricing algorithm.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Option 1: SQLite Setup (Recommended for Beginners)](#option-1-sqlite-setup-recommended-for-beginners)
  - [Option 2: PostgreSQL Setup (Recommended for Production)](#option-2-postgresql-setup-recommended-for-production)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Pricing Algorithm](#pricing-algorithm)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

- **Automatic Price Calculation**: Product prices update automatically when raw material costs change
- **Proportional Pricing Algorithm**: Customizable coefficients control how much material cost affects product price
- **Multi-Category Support**: Organize products by categories (Pipes, Sheets, Bars, etc.)
- **Real-Time Updates**: Live price updates across all linked products
- **Admin Panel**: Secure admin interface for managing materials and products
- **Product Catalog**: Public-facing catalog with search and filter capabilities
- **Price History**: Track all price changes with timestamps
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Session-Based Authentication**: Secure login system for admin users

---

## 🖼️ Screenshots

### Home Dashboard
Modern landing page with feature cards and statistics.

### Admin Panel
Manage raw materials and products with real-time price updates.

### Product Catalog
Browse products with advanced filtering and search.

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

### Required Software

1. **Python 3.8 or higher**
   - Download: [python.org/downloads](https://www.python.org/downloads/)
   - ⚠️ During installation, check "Add Python to PATH"
   - Verify installation: `python --version`

2. **pip (Python Package Manager)**
   - Usually comes with Python
   - Verify: `pip --version`

3. **Git** (Optional, for cloning repository)
   - Download: [git-scm.com](https://git-scm.com/downloads)

4. **PostgreSQL** (Optional, for production database)
   - Download: [postgresql.org/download](https://www.postgresql.org/download/)
   - Version 12 or higher recommended

5. **Text Editor/IDE**
   - [VS Code](https://code.visualstudio.com/) (Recommended)
   - Or PyCharm, Sublime Text, etc.

---

## 🚀 Installation

### Step 1: Clone or Download the Project

```
# Option A: Clone with Git
git clone https://github.com/yourusername/metalworks-pms.git
cd metalworks-pms

# Option B: Download ZIP
# Extract the ZIP file and navigate to the folder
cd metalworks-pms
```

### Step 2: Create Virtual Environment

**Windows PowerShell:**
```
python -m venv venv
venv\Scripts\Activate.ps1

# If you get an execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Windows CMD:**
```
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/Mac:**
```
python3 -m venv venv
source venv/bin/activate
```

**Note:** When activated, you'll see `(venv)` before your command prompt.

### Step 3: Install Python Dependencies

```
pip install -r requirements.txt
```

**requirements.txt contents:**
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
Flask-CORS==4.0.0
Werkzeug==3.0.1
psycopg2-binary==2.9.9  # Only needed for PostgreSQL
```

---

## 💾 Database Setup

Choose one of the following database options:

---

### Option 1: SQLite Setup (Recommended for Beginners)

SQLite is a file-based database that requires no separate installation.

#### Step 1: Configure Database in app.py

Open `app.py` and ensure this line is present:

```
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pricing.db'
```

#### Step 2: Initialize Database

**Windows PowerShell:**
```
# Set Flask app environment variable
$env:FLASK_APP = "app.py"

# Initialize migrations
flask db init
flask db migrate -m "Initial database setup"
flask db upgrade
```

**Windows CMD:**
```
set FLASK_APP=app.py
flask db init
flask db migrate -m "Initial database setup"
flask db upgrade
```

**Linux/Mac:**
```
export FLASK_APP=app.py
flask db init
flask db migrate -m "Initial database setup"
flask db upgrade
```

**✅ Success:** A `pricing.db` file will be created in your project folder.

#### Step 3: Create Admin User

```
python
```

Inside Python shell:
```
from app import app, db
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    admin = User(
        username='admin',
        password_hash=generate_password_hash('admin123'),
        is_admin=True
    )
    db.session.add(admin)
    db.session.commit()
    print("✓ Admin user created successfully!")

exit()
```

**✅ SQLite setup complete! Skip to [Running the Application](#running-the-application)**

---

### Option 2: PostgreSQL Setup (Recommended for Production)

PostgreSQL is a powerful, production-ready database system.

#### Step 1: Install PostgreSQL

**Windows:**
1. Download installer from [postgresql.org/download/windows](https://www.postgresql.org/download/windows/)
2. Run installer (recommended: PostgreSQL 16)
3. During installation:
   - Set a password for `postgres` user (remember this!)
   - Default port: `5432`
   - Accept default locale
4. Verify installation:
   ```
   # Check if PostgreSQL service is running
   Get-Service | Where-Object {$_.Name -like "*postgres*"}
   ```

**Linux (Ubuntu/Debian):**
```
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**macOS:**
```
# Using Homebrew
brew install postgresql@16
brew services start postgresql@16
```

#### Step 2: Create Database

**Windows:**
```
# Navigate to PostgreSQL bin folder
cd "C:\Program Files\PostgreSQL\16\bin"

# Connect to PostgreSQL
.\psql.exe -U postgres

# Inside psql prompt:
CREATE DATABASE pricing_db;
CREATE USER pricing_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE pricing_db TO pricing_user;
\q
```

**Linux/Mac:**
```
# Switch to postgres user
sudo -u postgres psql

# Inside psql prompt:
CREATE DATABASE pricing_db;
CREATE USER pricing_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE pricing_db TO pricing_user;
\q
```

**Alternative: Using createdb command**
```
# Windows (in PostgreSQL bin folder)
.\createdb.exe -U postgres pricing_db

# Linux/Mac
sudo -u postgres createdb pricing_db
```

#### Step 3: Install PostgreSQL Python Driver

```
pip install psycopg2-binary
```

#### Step 4: Configure Database Connection in app.py

Open `app.py` and update the database URI:

```
# Replace 'username', 'password', and 'pricing_db' with your values
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pricing_user:your_secure_password@localhost:5432/pricing_db'
```

**Connection String Format:**
```
postgresql://[username]:[password]@[host]:[port]/[database_name]
```

**Example:**
```
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pricing_user:mySecurePass123@localhost:5432/pricing_db'
```

**⚠️ Special Characters in Password:**

If your password contains special characters like `@`, `%`, `:`, you need to URL-encode them:

| Character | Encoded |
|-----------|---------|
| `@`       | `%40`   |
| `:`       | `%3A`   |
| `/`       | `%2F`   |
| `%`       | `%25`   |

**Example:** Password `P@ss:123` becomes `P%40ss%3A123`

#### Step 5: Initialize Database

**Windows PowerShell:**
```
$env:FLASK_APP = "app.py"
flask db init
flask db migrate -m "Initial database setup"
flask db upgrade
```

**Linux/Mac:**
```
export FLASK_APP=app.py
flask db init
flask db migrate -m "Initial database setup"
flask db upgrade
```

#### Step 6: Create Admin User

```
python
```

Inside Python shell:
```
from app import app, db
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    admin = User(
        username='admin',
        password_hash=generate_password_hash('admin123'),
        is_admin=True
    )
    db.session.add(admin)
    db.session.commit()
    print("✓ Admin user created successfully!")

exit()
```

#### Step 7: Verify PostgreSQL Connection

```
python
```

```
from app import app, db

with app.app_context():
    # Test connection
    db.engine.connect()
    print("✓ PostgreSQL connection successful!")

exit()
```

**✅ PostgreSQL setup complete!**

---

## ▶️ Running the Application

### Start the Flask Server

```
python app.py
```

**Expected output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### Access the Application

Open your web browser and navigate to:

| Page | URL | Description |
|------|-----|-------------|
| **Home** | http://localhost:5000/ | Main dashboard with navigation |
| **Admin Panel** | http://localhost:5000/admin | Manage materials and products |
| **Product Catalog** | http://localhost:5000/products | Public product listing |

### Default Login Credentials

- **Username:** `admin`
- **Password:** `admin123`

**⚠️ Security Note:** Change these credentials after first login!

---

## 📂 Project Structure

```
metalworks-pms/
├── app.py                      # Main Flask application
├── models.py                   # Database models (SQLAlchemy)
├── utils.py                    # Helper functions (admin decorator)
├── pricing_algorithm.py        # Proportional pricing logic
├── requirements.txt            # Python dependencies
│
├── routes/                     # API route blueprints
│   ├── __init__.py
│   ├── auth.py                # Login/logout endpoints
│   ├── raw_materials.py       # Raw materials CRUD
│   └── products.py            # Products CRUD
│
├── templates/                  # HTML templates
│   ├── home.html              # Landing page
│   ├── admin.html             # Admin dashboard
│   └── products.html          # Product catalog
│
├── migrations/                 # Database migrations (auto-generated)
├── pricing.db                  # SQLite database (if using SQLite)
└── README.md                   # This file
```

---

## 🔌 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/login` | Login user | No |
| POST | `/api/logout` | Logout user | No |
| GET | `/api/check-session` | Check login status | No |

### Raw Materials

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/raw-materials` | Get all materials | No |
| GET | `/api/raw-materials/<id>` | Get specific material | No |
| POST | `/api/raw-materials` | Create new material | Yes (Admin) |
| PUT | `/api/raw-materials/<id>` | Update material price | Yes (Admin) |
| DELETE | `/api/raw-materials/<id>` | Delete material | Yes (Admin) |

### Products

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/products` | Get all products | No |
| GET | `/api/products/<id>` | Get specific product | No |
| POST | `/api/products` | Create new product | Yes (Admin) |
| PUT | `/api/products/<id>` | Update product | Yes (Admin) |
| DELETE | `/api/products/<id>` | Delete product | Yes (Admin) |

### Example API Calls

**Get all materials:**
```
curl http://localhost:5000/api/raw-materials
```

**Update material price (requires login):**
```
curl -X PUT http://localhost:5000/api/raw-materials/1 \
  -H "Content-Type: application/json" \
  -d '{"current_price": 120.0}'
```

---

## 🧮 Pricing Algorithm

### How It Works

When a raw material price changes, all linked products automatically recalculate using:

```
new_product_price = base_price + (base_price × coefficient × price_change_ratio)

where:
price_change_ratio = (new_material_price - old_material_price) / old_material_price
```

### Example

**Initial Setup:**
- Steel: $100/ton
- Steel Pipe: Base price $150, Coefficient 0.8

**Price Update:**
- Steel increases to $120/ton (20% increase)

**Calculation:**
```
price_change_ratio = (120 - 100) / 100 = 0.20
adjustment = 150 × 0.8 × 0.20 = $24
new_price = 150 + 24 = $174
```

**Result:** Steel Pipe automatically updates from $150 to $174

### Coefficient Guide

| Coefficient | Meaning | Example Use Case |
|-------------|---------|------------------|
| `1.0` | 100% pass-through | Direct material cost products |
| `0.8` | 80% pass-through | Products with moderate processing |
| `0.5` | 50% pass-through | Products with significant labor/processing |
| `0.2` | 20% pass-through | Products where material is small portion of cost |
| `0.0` | No pass-through | Fixed-price products regardless of material cost |

---

## 🎯 Usage Guide

### First-Time Setup

1. **Login to Admin Panel**
   - Go to http://localhost:5000/
   - Click "Login"
   - Enter `admin` / `admin123`

2. **Add Raw Materials**
   - Click "Admin Panel"
   - Stay on "Raw Materials" tab
   - Add materials (e.g., Steel $100, Aluminum $85, Copper $95)

3. **Add Products**
   - Click "Products" tab
   - Fill the form:
     - Product Name: "Steel Pipe 2 inch"
     - Raw Material: Select "Steel"
     - Base Price: $150
     - Coefficient: 0.8
     - Category: "Pipes"
   - Click "Add Product"

4. **Test Price Updates**
   - Go back to "Raw Materials" tab
   - Change Steel price from $100 to $120
   - Click "Update"
   - See message: "3 products affected"

5. **View Product Catalog**
   - Go to http://localhost:5000/products
   - See all products with updated prices
   - Use search and filters

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "flask: command not found"

**Cause:** Virtual environment not activated or Flask not installed.

**Solution:**
```
# Activate virtual environment
# Windows:
venv\Scripts\Activate.ps1

# Linux/Mac:
source venv/bin/activate

# Install Flask
pip install flask
```

---

#### 2. "Error: No such command 'db'"

**Cause:** Flask-Migrate not installed or FLASK_APP not set.

**Solution:**
```
pip install flask-migrate

# Windows PowerShell:
$env:FLASK_APP = "app.py"

# Linux/Mac:
export FLASK_APP=app.py
```

---

#### 3. PostgreSQL Connection Refused

**Cause:** PostgreSQL service not running.

**Solution Windows:**
```
# Check service status
Get-Service | Where-Object {$_.Name -like "*postgres*"}

# Start service
net start postgresql-x64-16
```

**Solution Linux:**
```
sudo systemctl start postgresql
sudo systemctl status postgresql
```

---

#### 4. "password authentication failed for user"

**Cause:** Wrong credentials in database URI.

**Solution:**
1. Check username and password in `app.py`
2. Reset PostgreSQL password if needed:
   ```
   # Connect as postgres
   sudo -u postgres psql
   
   # Reset password
   ALTER USER pricing_user WITH PASSWORD 'new_password';
   ```

---

#### 5. CORS Error in Browser

**Cause:** Flask-CORS not installed or not configured.

**Solution:**
```
pip install flask-cors
```

Verify in `app.py`:
```
from flask_cors import CORS
CORS(app)
```

---

#### 6. "ImportError: cannot import name 'admin_required'"

**Cause:** Missing `utils.py` file or circular import.

**Solution:**
1. Ensure `utils.py` exists with `admin_required` function
2. Check that routes import from `utils`, not `app`:
   ```
   from utils import admin_required  # ✓ Correct
   from app import admin_required    # ✗ Wrong (circular import)
   ```

---

#### 7. Database Tables Not Created

**Cause:** Migrations not run.

**Solution:**
```
flask db upgrade
```

If that fails, reset migrations:
```
# Delete migrations folder and database
rm -rf migrations
rm pricing.db  # or drop PostgreSQL database

# Reinitialize
flask db init
flask db migrate -m "Initial setup"
flask db upgrade
```

---

## 🔐 Security Best Practices

### For Development

1. **Change Default Credentials**
   ```
   # Create new admin user with strong password
   admin = User(username='your_admin', password_hash=generate_password_hash('Strong_Pass_123!'), is_admin=True)
   ```

2. **Update Secret Key**
   ```
   # In app.py, generate a random secret key
   import secrets
   app.config['SECRET_KEY'] = secrets.token_hex(32)
   ```

### For Production

1. **Use Environment Variables**
   ```
   import os
   app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
   app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
   ```

2. **Disable Debug Mode**
   ```
   if __name__ == '__main__':
       app.run(debug=False)  # Never use debug=True in production
   ```

3. **Use HTTPS**
   - Deploy behind a reverse proxy (Nginx, Apache)
   - Use SSL certificates (Let's Encrypt)

4. **Use Production WSGI Server**
   ```
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

---

## 📊 Database Backup

### SQLite Backup

```
# Simple file copy
cp pricing.db pricing_backup_$(date +%Y%m%d).db
```

### PostgreSQL Backup

```
# Backup
pg_dump -U pricing_user -d pricing_db > backup_$(date +%Y%m%d).sql

# Restore
psql -U pricing_user -d pricing_db < backup_20251007.sql
```

---

## 🚢 Deployment

### Deploy to Production Server

1. **Set up production database (PostgreSQL recommended)**
2. **Configure environment variables**
3. **Use Gunicorn as WSGI server**
   ```
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```
4. **Set up Nginx as reverse proxy**
5. **Enable SSL with Let's Encrypt**
6. **Set up systemd service for auto-start**

### Deploy to Cloud Platforms

- **Heroku**: Use `Procfile` with `gunicorn`
- **AWS Elastic Beanstalk**: Deploy with `eb deploy`
- **DigitalOcean App Platform**: Connect GitHub repo
- **Railway**: One-click deployment

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- Flask documentation and community
- SQLAlchemy for excellent ORM
- All contributors to open-source libraries used

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Search existing [GitHub Issues](https://github.com/yourusername/metalworks-pms/issues)
3. Open a new issue with detailed information

---

## 🗺️ Roadmap

### Upcoming Features

- [ ] Price history graphs and analytics
- [ ] Export data to Excel/CSV
- [ ] Multi-user support with roles
- [ ] Inventory tracking integration
- [ ] Customer quote generation
- [ ] Email notifications for price changes
- [ ] REST API documentation (Swagger)
- [ ] Mobile app (React Native)

---

## ⭐ Star This Project

If you find this project useful, please consider giving it a star on GitHub!

```
⭐ Star the project to show your support!
```

---

**Built with ❤️ using Flask and Python**
